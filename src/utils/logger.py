from loguru import logger

def setup_logger(log_level="INFO"):
    logger.remove()
    logger.add(
        sink=lambda msg: print(msg, end=""),
        level=log_level.upper(),
        format="<green>[{time:YYYY-MM-DD HH:mm:ss}]</green> <level>{level}</level> | <cyan>{message}</cyan>\n"
    )
    return logger