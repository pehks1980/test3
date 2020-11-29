import logging

import aiohttp_jinja2
import jinja2

from aiohttp import web

from routes import setup_routes

from settings import PACKAGE_NAME, TEMPLATES_ROOT, LOG_TO, LOG_ROTATE, LOG_NAME
from _logging import create_logger
import os,sys

log = create_logger(path=sys.path[0], handler=LOG_TO, rotate=LOG_ROTATE)

pid = os.getpid()
prog_log = f'{sys.argv[0]} [{pid}]:'

logging.basicConfig(level=logging.DEBUG)


def setup_jinja(app):
    loader = jinja2.FileSystemLoader(str(TEMPLATES_ROOT))
    jinja_env = aiohttp_jinja2.setup(app, loader=loader)
    log.debug(f' {prog_log} Отладочная информация: загрузка шаблона')
    return jinja_env

async def init_app(config):
    log.debug(f' {prog_log} Отладочная информация: Инициализация')

    app = web.Application()

    app['config'] = config

    setup_routes(app)

    setup_jinja(app)

    log.debug(app['config'])

    return app


def main():


    config = ''

    app = init_app(config)

    web.run_app(app)

if __name__ == '__main__':
    log.debug(f' {prog_log} Отладочная информация: Старт')
    main()
