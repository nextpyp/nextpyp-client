
# invoke with:
# tox run -e dev -- python -m testlib

import asyncio
import time

from nextpyp.client import Client
from nextpyp.client.credentials import Credentials
from nextpyp.client.gen import RealTimeC2SListenToProject, RealTimeS2CProjectStatus


client = Client(
    url_base='http://192.168.56.5:8080',
    #credentials=None
    credentials=Credentials(
        userid='jeff',
        token='3fsn8zZTi5dS0Z58dmn4AEQPT7FHXun6OU2sBLJYzXh'
    )
)


def request() -> None:

    token_data = client.services.apps.request_token(
        user_id='jeff',
        app_name='Tester',
        app_permission_ids=[
            'project_list', 'project_listen'
        ]
    )
    print(f'token data: {token_data}')


def call() -> None:

    projects = client.services.projects.list('jeff')
    for project in projects:
       print(f'project = {project}')


async def ws() -> None:

    async with client.realtime_services.project as project:
        await project.send_listen_to_project(RealTimeC2SListenToProject(
            user_id='jeff',
            project_id='SPA_Test-79TUrqvTRuG'
        ))
        msg = await project.recv()
        if type(msg) is RealTimeS2CProjectStatus:
            print(f'project status: {msg}')
        else:
            print(f'received other msg: {msg}')


def sessions() -> None:
    client.services.projects


async def listen_to_stuff(msg: str) -> None:
    print(f'listen to stuff! msg={msg}')
    while True:
        try:
            print(f'sleeping ... msg={msg}')
            await asyncio.sleep(1)
        except asyncio.CancelledError:
            print(f'canceled! msg={msg}')
            break


async def asyncio_tests_async() -> None:

    print('start task')
    coro = listen_to_stuff('foo')
    task = asyncio.create_task(coro)

    print('sleeping ...')
    await asyncio.sleep(6)

    task.cancel()


def asyncio_tests_sync() -> None:

    loop = asyncio.new_event_loop()

    print('start task')
    coro = listen_to_stuff('foo')
    task = loop.create_task(coro)

    for _ in range(6):
        print('polling ...')
        loop.run_until_complete(asyncio.sleep(1))

    task.cancel()
    loop.stop()
    loop.run_until_complete(task)
    loop.close()


async def main() -> None:
    #request()
    #call()
    #await ws()
    #sessions()
    await asyncio_tests_async()


#asyncio.run(main())
asyncio_tests_sync()
