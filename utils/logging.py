import logging
from logging.handlers import RotatingFileHandler
import os


def configure_logging(app):
    log_level = logging.DEBUG if app.config.get("DEBUG") else logging.INFO

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    os.makedirs("logs", exist_ok=True)
    file_handler = RotatingFileHandler(
        "logs/app.log",
        maxBytes=5_000_000,
        backupCount=5
    )
    file_handler.setFormatter(formatter)

    app.logger.setLevel(log_level)
    app.logger.addHandler(console_handler)
    app.logger.addHandler(file_handler)
    app.logger.info("Logging system initialized")
