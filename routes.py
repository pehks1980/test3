from views import index, startDaemon, stopDaemon, checkDaemon, restartDaemon, saveFlag
import logging
import os, sys
pid = os.getpid()
prog_log = f'{sys.argv[0]} [{pid}]:'

log = logging.getLogger('aiohttp.access')

def setup_routes(app):
    app.router.add_get('/', index, name='index')
    app.router.add_post('/startDaemon', startDaemon, name='startDaemon')
    app.router.add_post('/stopDaemon', stopDaemon, name='stopDaemon')
    app.router.add_post('/restartDaemon', restartDaemon, name='restartDaemon')
    app.router.add_get('/checkDaemon', checkDaemon, name='checkDaemon')
    app.router.add_post('/saveFlag', saveFlag, name='saveFlag')

    log.debug(f' {prog_log} Отладочная информация: загрузка веб путей контроллеров вьюх')

