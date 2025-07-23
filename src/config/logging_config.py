import logging
import logging.config
from pathlib import Path

# Criar diretório de logs
LOG_DIR = Path("log")
LOG_DIR.mkdir(exist_ok=True)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "file": {"format": "%(asctime)s [%(levelname)s] %(name)s:%(funcName)s:%(lineno)d: %(message)s"},
    },
    "handlers": {
        "file_handler": {
            "level": "INFO",
            "formatter": "file",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "log/app.log",
            "maxBytes": 10 * 1024 * 1024,  # 10 MB
            "backupCount": 5,
        },
        "error_handler": {
            "level": "ERROR",
            "formatter": "file",
            "class": "logging.FileHandler",
            "filename": "log/error.log",
        },
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["file_handler", "error_handler"],
            "level": "INFO",
            "propagate": False,
        }
    },
}


def setup_logging():
    """Configurar o sistema de logging apenas para arquivos"""
    logging.config.dictConfig(LOGGING_CONFIG)
