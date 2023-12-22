
import pytest

from nextpyp.client.gen import RealTimeC2S, RealTimeS2C, ProjectRunData, JobRunData, ClusterJobData, RunStatus, Block
from nextpyp.client.realtime import RealtimeServiceError

from testlib import MockClient


pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
async def test_send_listen() -> None:
    client = MockClient()
    async with client.realtime_services.project as srv:
        await srv.send_listen_to_project(RealTimeC2S.ListenToProject(
            user_id='foo',
            project_id='bar'
        ))
    assert client.last_sent_message() == {
        'type': RealTimeC2S.ListenToProject.TYPE_ID,
        'userId': 'foo',
        'projectId': 'bar'
    }


@pytest.mark.asyncio
async def test_recv_error() -> None:
    client = MockClient()
    client.next_recv_message({
        'type': RealTimeS2C.Error.TYPE_ID,
        'name': 'Foo',
        'msg': 'bar'
    })
    async with client.realtime_services.project as srv:
        with pytest.raises(RealtimeServiceError) as ex_info:
            await srv.recv()
        assert ex_info.value.e.name == 'Foo'
        assert ex_info.value.e.msg == 'bar'


@pytest.mark.asyncio
async def test_recv_status() -> None:
    client = MockClient()
    client.next_recv_message({
        'type': RealTimeS2C.ProjectStatus.TYPE_ID,
        'recentRuns': [
            {
                'runId': 97,
                'timestamp': 1702487772312,
                'status': 'Failed',
                'jobs': [
                    {
                        'jobId': 'eS9Zgu1YqpZK7q8X',
                        'status': 'Failed',
                        'clusterJobs': [
                            {
                                'clusterJobId': 'eqKNO4qeWcIckPZm',
                                'webName': 'Check gain reference',
                                'clusterName': 'pyp_gainref',
                                'status': 'Failed',
                                'arrayInfo': None
                            }
                        ]
                    }
                ]
            },
            {
                'runId': 98,
                'timestamp': 1702487935516,
                'status': 'Failed',
                'jobs': [
                    {
                        'jobId': 'eS9Zgu1YqpZK7q8X',
                        'status': 'Failed',
                        'clusterJobs': [
                            {
                                'clusterJobId': 'eqKOJpOY68jVMwpp',
                                'webName': 'Check gain reference',
                                'clusterName': 'pyp_gainref',
                                'status': 'Failed',
                                'arrayInfo': None
                            }
                        ]
                    }
                ]
            }
        ],
        'hasOlderRuns': True,
        'blocks': [
            {
                'blockId': 'spr_import_raw',
                'name': 'SPA import raw',
                'description': 'Data Import for SPA',
                'groupIds': ['data', 'gain', 'scope']
            },
            {
                'blockId': 'spr_import',
                'name': 'SPA import',
                'description': 'CLI Import for SPA',
                'groupIds': ['data', 'movie', 'ctf', 'detect', 'detect_nn2d', 'slurm']
            }
        ]
    })
    async with client.realtime_services.project as srv:
        msg = await srv.recv()
        assert msg == RealTimeS2C.ProjectStatus(
            recent_runs=[
                ProjectRunData(
                    run_id=97,
                    timestamp=1702487772312,
                    status=RunStatus.Failed,
                    jobs=[
                        JobRunData(
                            job_id='eS9Zgu1YqpZK7q8X',
                            status=RunStatus.Failed,
                            cluster_jobs=[
                                ClusterJobData(
                                    cluster_job_id='eqKNO4qeWcIckPZm',
                                    web_name='Check gain reference',
                                    cluster_name='pyp_gainref',
                                    status=RunStatus.Failed,
                                    array_info=None
                                )
                            ]
                        )
                    ]
                ),
                ProjectRunData(
                    run_id=98,
                    timestamp=1702487935516,
                    status=RunStatus.Failed,
                    jobs=[
                        JobRunData(
                            job_id='eS9Zgu1YqpZK7q8X',
                            status=RunStatus.Failed,
                            cluster_jobs=[
                                ClusterJobData(
                                    cluster_job_id='eqKOJpOY68jVMwpp',
                                    web_name='Check gain reference',
                                    cluster_name='pyp_gainref',
                                    status=RunStatus.Failed,
                                    array_info=None
                                )
                            ]
                        )
                    ]
                ),
            ],
            has_older_runs=True,
            blocks=[
                Block(
                    block_id='spr_import_raw',
                    name='SPA import raw',
                    description='Data Import for SPA',
                    group_ids=['data', 'gain', 'scope']
                ),
                Block(
                    block_id='spr_import',
                    name='SPA import',
                    description='CLI Import for SPA',
                    group_ids=['data', 'movie', 'ctf', 'detect', 'detect_nn2d', 'slurm']
                )
            ]
        )
