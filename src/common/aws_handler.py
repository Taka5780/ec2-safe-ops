from functools import wraps

from botocore.exceptions import ClientError

from common.logger_config import setup_logger

logger = setup_logger(__name__)


def handle_ec2_action(func):
    # A decorator for common validation and exception handling of EC2 instance operations
    @wraps(func)
    def wrapper(self, instance_ids: list[str], *args, **kwargs):
        logger.info(f"START: {func.__name__} for instances: {instance_ids}")
        if not instance_ids:
            return True, None

        try:
            func(self, instance_ids, *args, **kwargs)
            logger.info(f"SUCCESS: {func.__name__} completed for: {instance_ids}")
            return True, None
        except ClientError as e:
            response = e.response
            error_info = response.get("Error", {})
            error_code = error_info.get("Code", "UnknownError")
            error_message = error_info.get("Message", "No message provided")
            logger.error(
                f"FAILURE: {func.__name__} failed for {instance_ids}. "
                f"Code: {error_code}, Message: {error_message}"
            )

            # If the caller has a `handle_error` function, use it
            if hasattr(self, "handle_error"):
                return False, self.handle_error(e)

            return False, error_code

    return wrapper
