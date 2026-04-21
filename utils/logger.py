from loguru import logger

logger.add("logs/app.log", rotation="1 MB")

def log_info(message):
    logger.info(message)