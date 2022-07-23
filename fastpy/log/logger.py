from .formatter import *
from datetime import datetime


class Logger:
    logger = logging.getLogger(APP_NAME)
    logger.setLevel(LEVEL)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(LEVEL)
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

    @staticmethod
    def print_raw(raw: any, raw_name: any):
        if Logger.logger.level == logging.DEBUG:
            print(colorama.Fore.WHITE, end='')
            print(raw_name)
            print('+--------------------------------------------------------+')
            print(raw)
            print('+--------------------------------------------------------+')
            print(colorama.Style.RESET_ALL, end='')

    @staticmethod
    def info(*msg: any, sep: str = ' ', pattern: str = None, ending_message: str = None):
        def deco(func):
            def wrapper(*args, **kwargs):
                if pattern:
                    Logger.log_info(pattern.format(**kwargs), sep=sep)
                else:
                    Logger.log_info(*msg, sep=sep)

                start = datetime.now()
                out = func(*args, **kwargs)
                end = datetime.now()
                lead_time = end - start

                if ending_message:
                    if '{time}' in ending_message:
                        Logger.log_info(ending_message.format(time=lead_time))
                    else:
                        Logger.log_info(ending_message)

                return out

            return wrapper

        return deco

    @staticmethod
    def catch_errors():
        def deco(func):
            def wrapper(*args, **kwargs):
                try:
                    out = func(*args, **kwargs)
                except Exception as e:
                    Logger.log_critical(e)
                    os.system('pause')
                    exit(-1)

                return out

            return wrapper

        return deco
