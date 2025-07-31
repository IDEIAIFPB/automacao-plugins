import logging
import logging.config
import os
from pathlib import Path

from rich.console import Console
from rich.logging import RichHandler
from rich.theme import Theme

# Criar diretório de logs
LOG_DIR = Path("log")
LOG_DIR.mkdir(exist_ok=True)

custom_theme = Theme(
    {
        "debug": "dim",  # Cinza
        "info": "green",  # Verde
        "warning": "yellow",  # Amarelo
        "error": "red",  # Vermelho
        "critical": "magenta",  # Magenta
        "exception": "red",  # Vermelho
    }
)

console = Console(theme=custom_theme)

# Detectar ambiente
ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()
DEBUG_MODE = ENVIRONMENT == "development"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "rich": {
            "format": "%(message)s",
        },
        "file": {"format": "%(asctime)s [%(levelname)s] %(name)s:%(funcName)s:%(lineno)d: %(message)s"},
    },
    "handlers": {
        "rich_console": {
            "()": RichHandler,
            "level": "DEBUG" if DEBUG_MODE else "INFO",
            "formatter": "rich",
            "console": console,
            "show_time": True,
            "show_path": True,
            "rich_tracebacks": True,
            "tracebacks_show_locals": True,
            "markup": True,  # Permite marcação de texto
        },
        "file_handler": {
            "level": "INFO",
            "formatter": "file",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "log/app.log",
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
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
            "handlers": ["rich_console", "file_handler", "error_handler"],
            "level": "DEBUG" if DEBUG_MODE else "INFO",
            "propagate": False,
        }
    },
}


def setup_logging():
    """Configurar o sistema de logging apenas para arquivos"""
    logging.config.dictConfig(LOGGING_CONFIG)
