from .formatter import *


class Logger:
    logger = logging.getLogger(APP_NAME)
    logger.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(CustomFormatter())

    logger.addHandler(stream_handler)

    @staticmethod
    def log_debug(*msg: any, sep: str = ' '):
        Logger.logger.debug(sep.join(map(str, msg)))

    @staticmethod
    def log_info(*msg: any, sep: str = ' '):
        Logger.logger.info(sep.join(map(str, msg)))

    @staticmethod
    def log_waring(*msg: any, sep: str = ' '):
        Logger.logger.info(sep.join(map(str, msg)))

    @staticmethod
    def log_error(*msg: any, sep: str = ' '):
        Logger.logger.error(sep.join(map(str, msg)))

    @staticmethod
    def log_critical(*msg: any, sep: str = ' '):
        Logger.logger.critical(sep.join(map(str, msg)))
