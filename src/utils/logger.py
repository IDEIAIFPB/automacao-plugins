import logging

from src.config.logging_config import setup_logging

setup_logging()


def get_logger(name: str) -> logging.Logger:
    """
    Retorna um logger configurado com o nome especificado.

    :param name: Nome do logger.
    :return: Logger configurado.
    """
    return logging.getLogger(name)


def log_info(message: str, *args, **kwargs):
    """
    Registra uma mensagem de informação.

    :param message: Mensagem a ser registrada.
    :param args: Argumentos adicionais para formatação da mensagem.
    :param kwargs: Argumentos adicionais para o logger.
    """
    logger = get_logger(__name__)
    logger.info(message, *args, **kwargs)


def log_error(message: str, *args, **kwargs):
    """
    Registra uma mensagem de erro.

    :param message: Mensagem a ser registrada.
    :param args: Argumentos adicionais para formatação da mensagem.
    :param kwargs: Argumentos adicionais para o logger.
    """
    logger = get_logger(__name__)
    logger.error(message, *args, **kwargs)


def log_warning(message: str, *args, **kwargs):
    """
    Registra uma mensagem de aviso.

    :param message: Mensagem a ser registrada.
    :param args: Argumentos adicionais para formatação da mensagem.
    :param kwargs: Argumentos adicionais para o logger.
    """
    logger = get_logger(__name__)
    logger.warning(message, *args, **kwargs)


def log_debug(message: str, *args, **kwargs):
    """
    Registra uma mensagem de depuração.

    :param message: Mensagem a ser registrada.
    :param args: Argumentos adicionais para formatação da mensagem.
    :param kwargs: Argumentos adicionais para o logger.
    """
    logger = get_logger(__name__)
    logger.debug(message, *args, **kwargs)


def log_critical(message: str, *args, **kwargs):
    """
    Registra uma mensagem crítica.

    :param message: Mensagem a ser registrada.
    :param args: Argumentos adicionais para formatação da mensagem.
    :param kwargs: Argumentos adicionais para o logger.
    """
    logger = get_logger(__name__)
    logger.critical(message, *args, **kwargs)


def log_exception(exc: Exception, message: str = "An error occurred", *args, **kwargs):
    """
    Registra uma exceção com uma mensagem personalizada.

    :param exc: Exceção a ser registrada.
    :param message: Mensagem personalizada para o log.
    :param args: Argumentos adicionais para formatação da mensagem.
    :param kwargs: Argumentos adicionais para o logger.
    """
    logger = get_logger(__name__)
    logger.exception(f"{message}: {exc}", *args, **kwargs)


logger = get_logger(__name__)
