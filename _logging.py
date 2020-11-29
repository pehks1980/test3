import logging, sys
import logging.handlers

from settings import LOG_TO, LOG_ROTATE,LOG_NAME

def create_logger(path, handler = 'FILE', rotate = 0 ):
    # create logger
    APP_LOG = logging.getLogger('aiohttp.access')
    #APP_LOG = logging.getLogger('aiohttp.web')
    # set level to deb
    APP_LOG.setLevel(logging.DEBUG)

    # обработчик выводит сообщения с уровнем CRITICAL/INFO в поток stderr
    STREAM_HANDLER = logging.StreamHandler(sys.stderr)
    STREAM_HANDLER.setLevel(logging.INFO)

    if (handler == 'FILE'):
        # обработчик который выводит сообщения в файл
        if rotate == 0: #0-client 1-server with day rotating log setting
            FILE_HANDLER = logging.FileHandler(f'{path}/log/{LOG_NAME}')
        else:
            FILE_HANDLER = logging.handlers.TimedRotatingFileHandler(f'{path}/log/{LOG_NAME}', encoding='utf8', interval=1, when='D')

        FILE_HANDLER.setLevel(logging.DEBUG)

    if (handler == 'SYSLOG'):
        SYSLOG_HANDLER = logging.handlers.SysLogHandler(address='/dev/log')

        SYSLOG_HANDLER.setLevel(logging.DEBUG)

    # Создать объект Formatter
    # Определить формат сообщений
    FORMATTER = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s ")

    # подключить объект Formatter к обработчикам
    STREAM_HANDLER.setFormatter(FORMATTER)

    if (handler == 'FILE'):
        FILE_HANDLER.setFormatter(FORMATTER)

    if (handler == 'SYSLOG'):
        FORMATTER = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s ")
        SYSLOG_HANDLER.setFormatter(FORMATTER)

    #attach each module to destination

    # Добавить обработчики к регистратору
    APP_LOG.addHandler(STREAM_HANDLER)

    if (handler == 'FILE'):
        APP_LOG.addHandler(FILE_HANDLER)

    if (handler == 'SYSLOG'):
        SYSLOG_HANDLER = logging.handlers.SysLogHandler(address='/dev/log')
        APP_LOG.addHandler(SYSLOG_HANDLER)

    return APP_LOG


def main():
    import os
    #log in log folder
    #srv_log = create_logger(path=sys.path[0], handler = LOG_TO, rotate = LOG_ROTATE )

    srv_log = create_logger(path=sys.path[0], handler= 'FILE')

    pid = os.getpid()
    prog_log = f'{sys.argv[0]} [{pid}]:'

    srv_log.critical(f' {prog_log} Критическая ошибка')
    srv_log.error(f' {prog_log} Ошибка')
    srv_log.debug(f' {prog_log} Отладочная информация')

if __name__ == '__main__':

    main()
