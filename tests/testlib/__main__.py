
# invoke with:
# tox run -e dev -- python -m testlib

import asyncio

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


async def main() -> None:
    #request()
    call()
    await ws()


asyncio.run(main())
