import sys

from common.constants import VAL_ERROR
from common.logger_config import setup_logger
from common.reporter import CSVReporter
from services.ec2_service import Ec2Service

logger = setup_logger(__name__)


def main():
    logger.info("Starting EC2 inventory export.")
    print("--- [Safety Gate 1] EC2 Inventory Export ---")

    ec2 = Ec2Service()
    if ec2.status == VAL_ERROR:
        logger.error("AWS Connection Failed.")
        print("AWS Connection Failed.")
        sys.exit(1)

    logger.info("AWS Connection established.")

    instances = ec2.get_instance()

    if ec2.status == VAL_ERROR:
        logger.error("API Error during instance retrieval.")
        print("AWS API Error during instance retrieval.")
        sys.exit(1)

    if not instances:
        logger.info("No instances found.")
        print("\n[Notice] No target instances found in this region.")
        return

    # CSV Export
    try:
        reporter = CSVReporter()
        file_path = reporter.export(instances, prefix="ec2_inventory")

        if file_path:
            logger.info(f"Inventory exported: {file_path}")
            print("\nSUCCESS: Inventory has been generated.")
            print(f"File Path: {file_path}")
            print(
                "Next: Open in Excel, add 'HumanCheck' column, and mark 'OK' for execution."
            )
        else:
            sys.exit(1)

    except Exception as e:
        logger.exception(f"Unexpected error during report generation: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
