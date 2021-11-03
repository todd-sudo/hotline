from loguru import logger


logger.add(
    "logs/parser.log",
    format="{time:DD:hh:mm!UTC} {level} {message}",
    level="DEBUG",
    rotation="2 MB",
    compression="zip",
    serialize=False,
    encoding="UTF8",
)
