import csv
from typing import List

from common.constants import PROD_KEYWORDS, TARGET_KEYWORDS
from common.logger_config import setup_logger

logger = setup_logger("csv_handler")


def get_verified_ids(
    file_path: str, target_action: str, id_column: str = "instance_id"
) -> List[str]:
    verified_ids: List[str] = []
    t_action_upper = target_action.strip().upper()

    try:
        with open(file_path, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)

            if "HumanCheck" not in (reader.fieldnames or []):
                logger.warning(f"The HumanCheck column was not found in {file_path}.")
                return []

            for row in reader:
                instance_id = row.get(id_column, "UNKNOWN_ID")
                env_raw = row.get("env", "").strip()
                env_lower = env_raw.lower()

                h_check = row.get("HumanCheck", "").strip().upper()

                if h_check != t_action_upper:
                    logger.debug(
                        f"Skipped {instance_id}: Not approved for {t_action_upper} (HumanCheck: {h_check})"
                    )
                    continue

                is_safe_env = any(kw in env_lower for kw in TARGET_KEYWORDS)
                is_production = any(p in env_lower for p in PROD_KEYWORDS)

                if not is_safe_env or is_production:
                    if env_raw:
                        logger.warning(
                            f"[Defense] Blocked execution on suspicious environment: {env_raw} ({instance_id})"
                        )
                    continue

                resource_id = row.get(id_column)
                if resource_id:
                    verified_ids.append(resource_id)
                    logger.info(f"Verified target found: {resource_id} (Env:{env_raw})")

            return verified_ids

    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
    except Exception as e:
        logger.error(f"Unexpected Error during CSV reading: {e}", exc_info=True)

    return []
