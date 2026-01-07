from datetime import datetime
import logging

logger = logging.getLogger("TimeTools")

def get_current_time() -> str:
    """
    Returns the current local time in ISO 8601 format.
    """
    now = datetime.now()
    time_str = now.isoformat()
    logger.debug(f"Time requested: {time_str}")
    return time_str
