from asyncio import create_subprocess_shell, subprocess
import time

import aiohttp_jinja2
from aiohttp import web

import logging

from settings import DAEMON_CMD_CHECK, DAEMON_CMD_RUN, DAEMON_CMD_STOP, DAEMON_STATE, DAEMON_CMD_RESTART, DUMP_FILE
import os,sys
pid = os.getpid()
prog_log = f'{sys.argv[0]} [{pid}]:'

log = logging.getLogger('aiohttp.access')

async def check_daemon(cmd):
    proc = await create_subprocess_shell(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    # Read 3 lines of output.
    for _ in range(2):
        await proc.stdout.readline()
    data = await proc.stdout.readline()
    #res '-1' means no string found
    res = data.decode('ascii').rfind('dead')

    # Wait for the subprocess exit.
    await proc.wait()

    return res

async def run(cmd):

    proc = await create_subprocess_shell(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    print(f'[{cmd!r} exited with {proc.returncode}]')

    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')

    return proc.returncode


@aiohttp_jinja2.template('index.html')
async def index(request):
    #nothing .... on /
    log.debug(f' {prog_log} Отладочная информация: Вызов /')
    return


async def startDaemon(request):
    print ('pressed start')

    res = await run(DAEMON_CMD_RUN)

    log.debug(f' {prog_log} Отладочная информация: Вызов /startDaemon - запуск {DAEMON_CMD_RUN} exit:{res}')

    print (f'exit code {res}')
    return web.json_response({'is_up': 1})


async def stopDaemon(request):

    print ('pressed stop')

    res = await run(DAEMON_CMD_STOP)

    log.debug(f' {prog_log} Отладочная информация: Вызов /stopDaemon - запуск {DAEMON_CMD_STOP} exit:{res}')

    print(f'exit code {res}')

    return web.json_response({'is_up': 0})

async def restartDaemon(request):
    #data = await request.json()
    print ('pressed restart')

    res = await run(DAEMON_CMD_RESTART)

    log.debug(f' {prog_log} Отладочная информация: Вызов /restartDaemon - запуск {DAEMON_CMD_RESTART} exit:{res}')

    print(f'exit code {res}')

    return web.json_response({'is_up': 2})


async def checkDaemon(request):

    res = await check_daemon(DAEMON_CMD_CHECK)

    if res > 0:
        #daemon is dead
        DAEMON_STATE = 0
        is_up = 0
        log.debug(f' {prog_log} Отладочная информация: checkDaemon {is_up} - down')
        print('checked: down')
    else:
        #daemon running
        is_up = 1
        DAEMON_STATE = 1
        log.debug(f' {prog_log} Отладочная информация: checkDaemon {is_up} - up')
        print('checked: up')


    return web.json_response({'is_up' : is_up})

async def saveFlag(request):
    import json
    data = await request.json()
    print (f'received chekbox {data}')

    #rewrite state of the flag to json obj array + timestamp  - dumps.json

    #read file
    try:
        with open(DUMP_FILE, 'r') as data_file:
            json_data = data_file.read()

        dump_data = json.loads(json_data)
    except:
        log.info(f' {prog_log} Отладочная информация: ошибка с file {DUMP_FILE}, создан новый файл')
        dump_data = []

    elem = {'ctrlFlag': data['ctrlFlag'],
            'time': time.time()}

    dump_data.append(elem)  # add new elem

    #dump it
    with open('dumps.json', 'w') as f_n:
        json.dump(dump_data, f_n, indent=4)

    f_n.close()

    log.debug(f' {prog_log} Отладочная информация: запись флажка в файл {DUMP_FILE}')

    return web.json_response({})


