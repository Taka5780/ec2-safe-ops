import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path

from common.constants import ACTION_START, VAL_ERROR
from common.csv_handler import get_verified_ids
from common.logger_config import setup_logger
from services.ec2_service import Ec2Service

logger = setup_logger("ec2_start")

BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "executions"
OLD_DIR = INPUT_DIR / "old"


def main():
    parser = argparse.ArgumentParser(description="EC2 Start Script Based on CSV")
    parser.add_argument(
        "--execute", action="store_true", help="Execute the actual start process"
    )
    parser.add_argument(
        "--file", type=str, help="Specific CSV file name in executions directory"
    )
    args = parser.parse_args()

    if args.file:
        target_csv = INPUT_DIR / args.file
        if not target_csv.exists():
            logger.error(f"Specified file not found: {args.file}")
            return
    else:
        csv_files = list(INPUT_DIR.glob("*.csv"))
        if not csv_files:
            logger.info("The CSV file to be processed cannot be found.")
            return

        target_csv = max(csv_files, key=lambda f: f.stat().st_mtime)

    logger.info(f"Loading...: {target_csv.name}")

    ec2_service = Ec2Service()
    if ec2_service.status == VAL_ERROR:
        logger.error(
            "Failed to initialize Ec2Service. Please check AWS credentials/region."
        )
        return

    start_ids = get_verified_ids(str(target_csv), target_action=ACTION_START)

    if not start_ids:
        logger.info("There were no instances to START.")
        return

    logger.info(f"Target extraction complete: {len(start_ids)} items.")
    for iid in start_ids:
        logger.info(f" [TARGET] {iid}")

    if args.execute:
        logger.info("Starting instances...")
        try:
            ec2_service.instance_start(start_ids)
            OLD_DIR.mkdir(exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            dest_path = OLD_DIR / f"executed_{timestamp}_{target_csv.name}"
            shutil.move(str(target_csv), str(dest_path))

            logger.info(
                f"The START process completed successfully, and the file has been archived.: {dest_path.name}"
            )

        except Exception as e:
            logger.error(
                f"An error occurred during the START process: {e}", exc_info=True
            )
            sys.exit(1)
    else:
        logger.info("This is dry-run mode. No actual START will occur.")
        logger.info("TIP: Use --execute to perform actual START.")


if __name__ == "__main__":
    main()
