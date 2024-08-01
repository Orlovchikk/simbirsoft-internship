import os
import logging.config

log_file_path = os.path.join(os.path.dirname(__file__), "logs", "python_script.log")

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(asctime)s - %(levelname)s: %(message)s",
            "datefmt": "%d/%m/%Y %I:%M:%S",
        },
        "detailed": {
            "format": "[%(levelname)s|%(module)s|L%(lineno)d] %(asctime)s: %(message)s",
            "datefmt": "%d/%m/%Y %I:%M:%S",
        },
    },
    "handlers": {
        "stderr": {
            "class": "logging.StreamHandler",
            "level": "ERROR",
            "formatter": "simple",
            "stream": "ext://sys.stderr",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": log_file_path,
            "maxBytes": 1000,
            "encoding": "utf-8",
        },
        "stdout": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "root": {
            "level": "DEBUG",
            "handlers": ["stdout", "file"],
        }
    },
}


logger = logging.getLogger("python_script")

logging.config.dictConfig(config=logging_config)
