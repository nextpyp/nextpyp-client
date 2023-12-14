
from nextpyp.client.gen import ProjectData, ProjectPermission, UserData

from testlib import MockClient


user_examples = [
    {'id': 'jeff', 'name': 'Jeff'}
]

project_examples = [
    {
        'owner': user_examples[0],
        'permissions': ['Read', 'Write'],
        'projectId': 'Tomo_Workflow-2GKAzf48o3GYWXCjAd',
        'projectNumber': 1,
        'projectName': 'Tomo Workflow',
        'created': 1693419608511,
        'images': [
            '/kv/jobs/ecq6mPesXW2Rdgzs/gainCorrectedImage/small',
            'kv/reconstructions/ecq6mPesXW2Rdgzv/1/2/images/map/small'
        ],
        'path': '/home/jeff/streamPYP/shared/users/jeff/projects/Tomo_Workflow-2GKAzf48o3GYWXCjAd'
    },
    {
        'owner': user_examples[0],
        'permissions': ['Read'],
        'projectId': 'Lotta_Blocks-UlR8AmaVTaRog1AJ',
        'projectNumber': None,
        'projectName': 'Lotta Blocks',
        'created': 1689713296127,
        'images': [],
        'path': '/home/jeff/streamPYP/shared/users/jeff/projects/Lotta_Blocks-UlR8AmaVTaRog1AJ'
    }
]


def test_list_params() -> None:
    client = MockClient()
    client.next_response = []
    client.services.projects.list('userid')
    assert client.last_params == ['userid']


def test_list_response_none() -> None:
    client = MockClient()
    client.next_response = []
    projects = client.services.projects.list('userid')
    assert projects == []


def test_list_response_two() -> None:
    client = MockClient()
    client.next_response = project_examples
    projects = client.services.projects.list('userid')
    assert client.last_params == ['userid']
    assert len(projects) == 2
    jeff = UserData(
        id='jeff',
        name='Jeff'
    )
    assert len(projects) == 2
    assert projects[0] == ProjectData(
        owner=jeff,
        permissions={ProjectPermission.Write, ProjectPermission.Read},
        project_id='Tomo_Workflow-2GKAzf48o3GYWXCjAd',
        project_number=1,
        project_name='Tomo Workflow',
        created=1693419608511,
        images=[
            '/kv/jobs/ecq6mPesXW2Rdgzs/gainCorrectedImage/small',
            'kv/reconstructions/ecq6mPesXW2Rdgzv/1/2/images/map/small'
        ],
        path='/home/jeff/streamPYP/shared/users/jeff/projects/Tomo_Workflow-2GKAzf48o3GYWXCjAd'
    )
    assert projects[1] == ProjectData(
        owner=jeff,
        permissions={ProjectPermission.Read},
        project_id='Lotta_Blocks-UlR8AmaVTaRog1AJ',
        project_number=None,
        project_name='Lotta Blocks',
        created=1689713296127,
        images=[],
        path='/home/jeff/streamPYP/shared/users/jeff/projects/Lotta_Blocks-UlR8AmaVTaRog1AJ'
    )
