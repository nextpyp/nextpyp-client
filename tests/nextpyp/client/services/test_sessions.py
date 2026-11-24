
from nextpyp.client.args import block_args, PypArgValues, PypBlock
from nextpyp.client.gen import (
    AvgRotData,
    CtfTiltValues,
    DriftMetadata,
    DriftXY,
    Group,
    MotionData,
    PreprocessingFilter,
    PreprocessingFilterType,
    PreprocessingPropRange,
    RemoteOption,
    RunStatus,
    RunningSessions,
    SessionDaemon,
    SessionExportRequestFilter,
    SessionJobLogData,
    SessionJobsLogs,
    SessionLogs,
    SessionPermission,
    SessionSpeeds,
    SingleParticleSessionArgs,
    SingleParticleSessionData,
    TomographySessionArgs,
    TomographySessionData
)
from nextpyp.client.ids import SessionTypes

from testlib import MockTransport


def test_spa_list() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.next_response = [
        {
            "userId": "jeff",
            "sessionId": "eQMBiHKJK5YsOLdQ",
            "sessionNumber": None,
            "created": 1685027585526,
            "permissions": ["Write", "Read"],
            "path": "/home/jeff/streamPYP/shared/sessions/eQMBiHKJK5YsOLdQ",
            "args": {
                "finished": {
                    "name": "Single-particle",
                    "path": "/home/jeff/streamPYP/shared/sessions/eQMBiHKJK5YsOLdQ",
                    "groupId": "eaNh61SZ9DmeeCjD",
                    "values": "data_path = \"/media/pyp/tests/spr/raw/*.tif\"\ngain_reference = \"/media/pyp/tests/spr/raw/K3_gain.mrc\"\nscope_pixel = 1\nscope_voltage = 300\ndetect_rad = 75\ndetect_method = \"all\"\nclass2d_min = 10\ndata_invert = true\nslurm_memory_per_task = 2\nslurm_class2d_memory_per_task = 2\n"
                }
            },
            "display": {
                "finished": {
                    "groupName": "Bartesaghi Lab"
                }
            },
            "numMicrographs": 2,
            "numFrames": 120,
            "images": ["/kv/sessions/eQMBiHKJK5YsOLdQ/data/20201009_1138_NBtest_A007_G001_H079_D007/image"],
            "slurmLogin": "jeff",
            "slurmLoginName": "Jeff"
        }
    ]
    sessions = client.services.single_particle_sessions.list()

    assert len(sessions) == 1

    # check the session data
    assert type(sessions[0]) is SingleParticleSessionData
    assert sessions[0].user_id == 'jeff'
    assert sessions[0].session_id == 'eQMBiHKJK5YsOLdQ'
    assert sessions[0].session_number is None
    assert sessions[0].created == 1685027585526
    assert sessions[0].permissions == {SessionPermission.Read, SessionPermission.Write}
    assert sessions[0].path == "/home/jeff/streamPYP/shared/sessions/eQMBiHKJK5YsOLdQ"
    assert sessions[0].args.finished is not None
    assert sessions[0].args.finished.name == "Single-particle"
    assert sessions[0].args.finished.path == "/home/jeff/streamPYP/shared/sessions/eQMBiHKJK5YsOLdQ"
    assert sessions[0].args.finished.group_id == "eaNh61SZ9DmeeCjD"
    assert sessions[0].args.finished.values.startswith('data_path = ')
    assert sessions[0].args.next is None
    assert sessions[0].display.finished is not None
    assert sessions[0].display.finished.group_name == 'Bartesaghi Lab'
    assert sessions[0].display.next is None
    assert sessions[0].num_micrographs == 2
    assert sessions[0].num_frames == 120
    assert sessions[0].images == ['/kv/sessions/eQMBiHKJK5YsOLdQ/data/20201009_1138_NBtest_A007_G001_H079_D007/image']
    assert sessions[0].slurm_login == 'jeff'
    assert sessions[0].slurm_login_name == 'Jeff'

    # check the pyp args
    arg_values = PypArgValues.from_toml(block_args(PypBlock.SESSION_SINGLE_PARTICLE), sessions[0].args.finished.values)
    assert arg_values.data_path == '/media/pyp/tests/spr/raw/*.tif'
    assert arg_values.gain_reference == '/media/pyp/tests/spr/raw/K3_gain.mrc'
    assert arg_values.scope_pixel == 1.0
    assert arg_values.scope_voltage == 300
    assert arg_values.detect_rad == 75.0
    assert arg_values.detect_method == 'all'
    assert arg_values.class2d_min == 10
    assert arg_values.data_invert is True
    assert arg_values.slurm_memory_per_task == 2
    assert arg_values.slurm_class2d_memory_per_task == 2


def test_spa_create() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.next_response = {
        "userId": "jeff",
        "sessionId": "sid",
        "sessionNumber": 42,
        "created": 5,
        "permissions": ["Write", "Read"],
        "path": "/sessions/sid",
        "args": {
            "next": {
                "name": "My new session",
                "path": "/path/to/session",
                "groupId": "groupid",
                "values": "data_path = \"/foo/bar\"\nscope_pixel = 1.0\ndata_invert = true\nslurm_memory_per_task = 2\n"
            }
        },
        "display": {
            "next": {
                "groupName": "Bob"
            }
        },
        "numMicrographs": 0,
        "numFrames": 0,
        "images": [],
        "slurmLogin": None,
        "slurmLoginName": None
    }

    pyp_args = PypArgValues(block_args(PypBlock.SESSION_SINGLE_PARTICLE))
    pyp_args.data_path = '/foo/bar'
    pyp_args.scope_pixel = 1
    pyp_args.data_invert = True
    pyp_args.slurm_memory_per_task = 2
    args = SingleParticleSessionArgs(
        'My new session',
        '/path/to/session',
        'groupid',
        pyp_args.write()
    )
    session = client.services.single_particle_sessions.create(args)

    assert transport.last_params == [
        {
            'name': 'My new session',
            'path': '/path/to/session',
            'groupId': 'groupid',
            'values': 'data_path = \"/foo/bar\"\nscope_pixel = 1.0\ndata_invert = true\nslurm_memory_per_task = 2\n'
        }
    ]

    # check returned session data
    assert type(session) is SingleParticleSessionData
    assert session.user_id == 'jeff'
    assert session.session_id == 'sid'
    assert session.session_number == 42
    assert session.created == 5
    assert session.permissions == {SessionPermission.Read, SessionPermission.Write}
    assert session.path == "/sessions/sid"
    assert session.args.finished is None
    assert session.args.next is not None
    assert session.args.next.name == 'My new session'
    assert session.args.next.path == '/path/to/session'
    assert session.args.next.group_id == 'groupid'
    assert session.args.next.values == "data_path = \"/foo/bar\"\nscope_pixel = 1.0\ndata_invert = true\nslurm_memory_per_task = 2\n"
    assert session.display.finished is None
    assert session.display.next is not None
    assert session.display.next.group_name == 'Bob'
    assert session.num_micrographs == 0
    assert session.num_frames == 0
    assert session.images == []
    assert session.slurm_login is None
    assert session.slurm_login_name is None


def test_spa_edit() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.next_response = {
        "userId": "jeff",
        "sessionId": "sid",
        "sessionNumber": 42,
        "created": 5,
        "permissions": ["Write", "Read"],
        "path": "/sessions/sid",
        "args": {
            "next": {
                "name": "My new session",
                "path": "/path/to/session",
                "groupId": "groupid",
                "values": "data_path = \"/foo/bar\"\n"
            }
        },
        "display": {
            "next": {
                "groupName": "Bob"
            }
        },
        "numMicrographs": 0,
        "numFrames": 0,
        "images": [],
        "slurmLogin": None,
        "slurmLoginName": None
    }

    pyp_args = PypArgValues(block_args(PypBlock.SESSION_SINGLE_PARTICLE))
    pyp_args.data_path = '/foo/bar'
    args = SingleParticleSessionArgs(
        'My new session',
        '/path/to/session',
        'groupid',
        pyp_args.write()
    )
    session = client.services.single_particle_sessions.edit('sid', args)

    assert transport.last_params == [
        'sid',
        {
            'name': 'My new session',
            'path': '/path/to/session',
            'groupId': 'groupid',
            'values': 'data_path = \"/foo/bar\"\n'
        }
    ]

    # spot-check the returned session data
    assert type(session) is SingleParticleSessionData
    assert session.session_id == 'sid'


def test_spa_get() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.next_response = {
        "userId": "jeff",
        "sessionId": "sid",
        "sessionNumber": 42,
        "created": 5,
        "permissions": ["Write", "Read"],
        "path": "/sessions/sid",
        "args": {
            "next": {
                "name": "My new session",
                "path": "/path/to/session",
                "groupId": "groupid",
                "values": "data_path = \"/foo/bar\"\n"
            }
        },
        "display": {
            "next": {
                "groupName": "Bob"
            }
        },
        "numMicrographs": 0,
        "numFrames": 0,
        "images": [],
        "slurmLogin": None,
        "slurmLoginName": None
    }

    session = client.services.single_particle_sessions.get('sid')

    assert transport.last_params == ['sid']

    # spot-check the returned session data
    assert type(session) is SingleParticleSessionData
    assert session.session_id == 'sid'


def test_spa_delete() -> None:

    transport = MockTransport()
    client = transport.client()

    client.services.single_particle_sessions.delete('sid')

    assert transport.last_params == ['sid']


def test_tomo_list() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.next_response = [
        {
            "userId": "jeff",
            "sessionId": "eEgGsN7MoPWaDzqt",
            "sessionNumber": None,
            "created": 1677177744809,
            "permissions": ["Read", "Write"],
            "path": "/home/jeff/streamPYP/shared/sessions/eEgGsN7MoPWaDzqt",
            "args": {
                "finished": {
                    "name": "New Tomography Session",
                    "path": "/home/jeff/streamPYP/shared/sessions/eEgGsN7MoPWaDzqt",
                    "groupId": "drGkM99qI3bEpLmo",
                    "values": "data_path = \"/media/pyp/tests/tomo/raw/tilt*.mrc\"\nscope_pixel = 1\nscope_voltage = 300\nstream_transfer_fileset = \".order,.rawtlt\"\nmovie_no_frames = true\n"
                },
                "next": {
                    "name": "New Tomography Session",
                    "path": "/home/jeff/streamPYP/shared/sessions/eEgGsN7MoPWaDzqt",
                    "groupId": "eaNh61SZ9DmeeCjD",
                    "values": "data_path = \"/media/pyp/tests/tomo/raw/tilt*.mrc\"\nscope_pixel = 1\nscope_voltage = 300\nstream_transfer_fileset = \".order,.rawtlt\"\nmovie_no_frames = true\n"
                }
            },
            "display": {
                "finished": {
                    "groupName": "(unknown group)"
                },
                "next": {
                    "groupName": "Bartesaghi Lab"
                }
            },
            "numTiltSeries": 1,
            "numTilts": 10,
            "images": [],
            "slurmLogin": "jeff",
            "slurmLoginName": "Jeff"
        }
    ]
    sessions = client.services.tomography_sessions.list()

    assert len(sessions) == 1

    # check the session data
    assert type(sessions[0]) is TomographySessionData
    assert sessions[0].user_id == 'jeff'
    assert sessions[0].session_id == 'eEgGsN7MoPWaDzqt'
    assert sessions[0].session_number is None
    assert sessions[0].created == 1677177744809
    assert sessions[0].permissions == {SessionPermission.Read, SessionPermission.Write}
    assert sessions[0].path == "/home/jeff/streamPYP/shared/sessions/eEgGsN7MoPWaDzqt"
    assert sessions[0].args.finished is not None
    assert sessions[0].args.finished.name == "New Tomography Session"
    assert sessions[0].args.finished.path == "/home/jeff/streamPYP/shared/sessions/eEgGsN7MoPWaDzqt"
    assert sessions[0].args.finished.group_id == "drGkM99qI3bEpLmo"
    assert sessions[0].args.finished.values.startswith('data_path = ')
    assert sessions[0].args.next is not None
    assert sessions[0].args.next.name == "New Tomography Session"
    assert sessions[0].args.next.path == "/home/jeff/streamPYP/shared/sessions/eEgGsN7MoPWaDzqt"
    assert sessions[0].args.next.group_id == "eaNh61SZ9DmeeCjD"
    assert sessions[0].args.next.values.startswith('data_path = ')
    assert sessions[0].display.finished is not None
    assert sessions[0].display.finished.group_name == '(unknown group)'
    assert sessions[0].display.next is not None
    assert sessions[0].display.next.group_name == 'Bartesaghi Lab'
    assert sessions[0].num_tilt_series == 1
    assert sessions[0].num_tilts == 10
    assert sessions[0].images == []
    assert sessions[0].slurm_login == 'jeff'
    assert sessions[0].slurm_login_name == 'Jeff'

    # check the pyp args
    arg_values = PypArgValues.from_toml(block_args(PypBlock.SESSION_TOMOGRAPHY), sessions[0].args.finished.values)
    assert arg_values.data_path == '/media/pyp/tests/tomo/raw/tilt*.mrc'
    assert arg_values.scope_pixel == 1.0
    assert arg_values.scope_voltage == 300
    assert arg_values.stream_transfer_fileset == '.order,.rawtlt'
    assert arg_values.movie_no_frames is True


def test_tomo_create() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.next_response = {
        "userId": "jeff",
        "sessionId": "sid",
        "sessionNumber": 42,
        "created": 5,
        "permissions": ["Write", "Read"],
        "path": "/sessions/sid",
        "args": {
            "next": {
                "name": "My new session",
                "path": "/path/to/session",
                "groupId": "groupid",
                "values": "data_path = \"/foo/bar\"\nscope_pixel = 1.0\ndata_invert = true\nslurm_memory_per_task = 2\n"
            }
        },
        "display": {
            "next": {
                "groupName": "Bob"
            }
        },
        "numTiltSeries": 0,
        "numTilts": 0,
        "images": [],
        "slurmLogin": None,
        "slurmLoginName": None
    }

    pyp_args = PypArgValues(block_args(PypBlock.SESSION_TOMOGRAPHY))
    pyp_args.data_path = '/foo/bar'
    pyp_args.scope_pixel = 1
    pyp_args.data_invert = True
    pyp_args.slurm_memory_per_task = 2
    args = TomographySessionArgs(
        'My new session',
        '/path/to/session',
        'groupid',
        pyp_args.write()
    )
    session = client.services.tomography_sessions.create(args)

    assert transport.last_params == [
        {
            'name': 'My new session',
            'path': '/path/to/session',
            'groupId': 'groupid',
            'values': 'data_path = \"/foo/bar\"\nscope_pixel = 1.0\ndata_invert = true\nslurm_memory_per_task = 2\n'
        }
    ]

    # check returned session data
    assert type(session) is TomographySessionData
    assert session.user_id == 'jeff'
    assert session.session_id == 'sid'
    assert session.session_number == 42
    assert session.created == 5
    assert session.permissions == {SessionPermission.Read, SessionPermission.Write}
    assert session.path == "/sessions/sid"
    assert session.args.finished is None
    assert session.args.next is not None
    assert session.args.next.name == 'My new session'
    assert session.args.next.path == '/path/to/session'
    assert session.args.next.group_id == 'groupid'
    assert session.args.next.values == "data_path = \"/foo/bar\"\nscope_pixel = 1.0\ndata_invert = true\nslurm_memory_per_task = 2\n"
    assert session.display.finished is None
    assert session.display.next is not None
    assert session.display.next.group_name == 'Bob'
    assert session.num_tilt_series == 0
    assert session.num_tilts == 0
    assert session.images == []
    assert session.slurm_login is None
    assert session.slurm_login_name is None


def test_tomo_edit() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.next_response = {
        "userId": "jeff",
        "sessionId": "sid",
        "sessionNumber": 42,
        "created": 5,
        "permissions": ["Write", "Read"],
        "path": "/sessions/sid",
        "args": {
            "next": {
                "name": "My new session",
                "path": "/path/to/session",
                "groupId": "groupid",
                "values": "data_path = \"/foo/bar\"\n"
            }
        },
        "display": {
            "next": {
                "groupName": "Bob"
            }
        },
        "numTiltSeries": 0,
        "numTilts": 0,
        "images": [],
        "slurmLogin": None,
        "slurmLoginName": None
    }

    pyp_args = PypArgValues(block_args(PypBlock.SESSION_TOMOGRAPHY))
    pyp_args.data_path = '/foo/bar'
    args = TomographySessionArgs(
        'My new session',
        '/path/to/session',
        'groupid',
        pyp_args.write()
    )
    session = client.services.tomography_sessions.edit('sid', args)

    assert transport.last_params == [
        'sid',
        {
            'name': 'My new session',
            'path': '/path/to/session',
            'groupId': 'groupid',
            'values': 'data_path = \"/foo/bar\"\n'
        }
    ]

    # spot-check the returned session data
    assert type(session) is TomographySessionData
    assert session.session_id == 'sid'


def test_tomo_get() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.next_response = {
        "userId": "jeff",
        "sessionId": "sid",
        "sessionNumber": 42,
        "created": 5,
        "permissions": ["Write", "Read"],
        "path": "/sessions/sid",
        "args": {
            "next": {
                "name": "My new session",
                "path": "/path/to/session",
                "groupId": "groupid",
                "values": "data_path = \"/foo/bar\"\n"
            }
        },
        "display": {
            "next": {
                "groupName": "Bob"
            }
        },
        "numTiltSeries": 0,
        "numTilts": 0,
        "images": [],
        "slurmLogin": None,
        "slurmLoginName": None
    }

    session = client.services.tomography_sessions.get('sid')

    assert transport.last_params == ['sid']

    # spot-check the returned session data
    assert type(session) is TomographySessionData
    assert session.session_id == 'sid'


def test_tomo_delete() -> None:

    transport = MockTransport()
    client = transport.client()

    client.services.tomography_sessions.delete('sid')

    assert transport.last_params == ['sid']


def test_tomo_get_drift_metadata() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.next_response = [
        {
            "tilts": [-6.0, 6.0],
            "drifts": [
                [{"x": 1.2, "y": 3.4}],
                [{"x": 5.6, "y": 7.8}]
            ],
            "ctfValues": [
                {
                    "index":  0,
                    "defocus1": 8244.6484375,
                    "defocus2": 7961.07958984375,
                    "astigmatism": 9.464014053344727,
                    "cc": 0.014696000143885612,
                    "resolution": 718.0
                },
                {
                    "index": 1,
                    "defocus1": 7412.55908203125,
                    "defocus2": 7163.65478515625,
                    "astigmatism": -7.342753887176514,
                    "cc": 0.027507999911904335,
                    "resolution": 5.092198848724365
                }
            ],
            "ctfProfiles": [
                {
                    "spatialFreq": [0.0, 0.001393, 0.002786],
                    "avgRot": [0.030491, 0.030491, 0.030491],
                    "ctfFit": [0.07, 0.07097, 0.073878],
                    "crossCorrelation": [1.0, -0.09739, -0.09739],
                    "minRes": 50.0
                },
                {
                    "spatialFreq": [0.0, 0.001393, 0.002786],
                    "avgRot": [-0.021156, 3.86222, 3.814014],
                    "ctfFit": [0.07, 0.070872, 0.073488],
                    "crossCorrelation": [1.0, 0.018553, 0.018553],
                    "minRes": 52.0
                }
            ],
            "tiltAxisAngle": -90.0
        }
    ]

    dmd = client.services.tomography_sessions.get_drift_metadata('sid', 'tsid')

    assert transport.last_params == [
        'sid',
        'tsid'
    ]

    assert dmd is not None
    assert type(dmd) is DriftMetadata

    assert dmd.tilts == [-6.0, 6.0]
    assert dmd.drifts == [
        [DriftXY(1.2, 3.4)],
        [DriftXY(5.6, 7.8)]
    ]
    assert dmd.ctf_values == [
        CtfTiltValues(
            0,
            8244.6484375,
            7961.07958984375,
            9.464014053344727,
            0.014696000143885612,
            718.0
        ),
        CtfTiltValues(
            1,
            7412.55908203125,
            7163.65478515625,
            -7.342753887176514,
            0.027507999911904335,
            5.092198848724365
        )
    ]
    assert dmd.ctf_profiles == [
        AvgRotData(
            [0.0, 0.001393, 0.002786],
            [0.030491, 0.030491, 0.030491],
            [0.07, 0.07097, 0.073878],
            [1.0, -0.09739, -0.09739],
            50.0
        ),
        AvgRotData(
            [0.0, 0.001393, 0.002786],
            [-0.021156, 3.86222, 3.814014],
            [0.07, 0.070872, 0.073488],
            [1.0, 0.018553, 0.018553],
            52.0
        )
    ]
    assert dmd.tilt_axis_angle == -90.0


def test_session_options() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.next_response = [
        {
            "value": "eQMBiHKJK5YsOLdQ",
            "text": "Single-particle"
        },
        {
            "value": "evKcXLQz3JlrDgV6",
            "text": "S2-Test blank"
        }
    ]

    options = client.services.sessions.session_options('a', None, SessionTypes.SINGLE_PARTICLE)

    assert transport.last_params == [
        'a',
        None,
        SessionTypes.SINGLE_PARTICLE
    ]

    assert len(options) == 2

    assert type(options[0]) is RemoteOption
    assert options[0].value == 'eQMBiHKJK5YsOLdQ'
    assert options[0].text == 'Single-particle'

    assert type(options[1]) is RemoteOption
    assert options[1].value == 'evKcXLQz3JlrDgV6'
    assert options[1].text == 'S2-Test blank'


def test_groups() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.next_response = [
        {
            "name": "Borgnia Lab",
            "id": "drH2MH7WXtfvhxam"
        },
        {
            "name": "Bartesaghi Lab",
            "id": "eaNh61SZ9DmeeCjD"
        }
    ]

    groups = client.services.sessions.groups()

    assert len(groups) == 2

    assert type(groups[0]) is Group
    assert groups[0].name == 'Borgnia Lab'
    assert groups[0].id == 'drH2MH7WXtfvhxam'

    assert type(groups[1]) is Group
    assert groups[1].name == 'Bartesaghi Lab'
    assert groups[1].id == 'eaNh61SZ9DmeeCjD'


def test_group_options() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.next_response = [
        {
            "value": "drH2MH7WXtfvhxam",
            "text": "Borgnia Lab"
        },
        {
            "value": "eaNh61SZ9DmeeCjD",
            "text": "Bartesaghi Lab"
        }
    ]

    options = client.services.sessions.group_options('a', None, None)

    assert transport.last_params == [
        'a',
        None,
        None
    ]

    assert len(options) == 2

    assert type(options[0]) is RemoteOption
    assert options[0].value == 'drH2MH7WXtfvhxam'
    assert options[0].text == 'Borgnia Lab'

    assert type(options[1]) is RemoteOption
    assert options[1].value == 'eaNh61SZ9DmeeCjD'
    assert options[1].text == 'Bartesaghi Lab'


def test_running() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.next_response = {
        "singleParticle": [],
        "tomography": []
    }

    sessions = client.services.sessions.running()

    assert type(sessions) is RunningSessions
    assert len(sessions.single_particle) == 0
    assert len(sessions.tomography) == 0
    # NOTE: don't need to test actual session data here
    # we've already tested that many times above


def test_is_running() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.next_response = True

    is_running = client.services.sessions.is_running('sid', SessionDaemon.Pypd)

    assert transport.last_params == [
        'sid',
        'Pypd'
    ]

    assert is_running is True


def test_start() -> None:

    transport = MockTransport()
    client = transport.client()

    client.services.sessions.start('sid', SessionDaemon.Pypd)

    assert transport.last_params == [
        'sid',
        'Pypd'
    ]


def test_restart() -> None:

    transport = MockTransport()
    client = transport.client()

    client.services.sessions.restart('sid', SessionDaemon.Pypd)

    assert transport.last_params == [
        'sid',
        'Pypd'
    ]


def test_clear() -> None:

    transport = MockTransport()
    client = transport.client()

    client.services.sessions.clear('sid', SessionDaemon.Pypd, True)

    assert transport.last_params == [
        'sid',
        'Pypd',
        True
    ]


def test_stop() -> None:

    transport = MockTransport()
    client = transport.client()

    client.services.sessions.stop('sid', SessionDaemon.Pypd)

    assert transport.last_params == [
        'sid',
        'Pypd'
    ]


def test_cancel() -> None:

    transport = MockTransport()
    client = transport.client()

    client.services.sessions.cancel('sid')

    assert transport.last_params == [
        'sid'
    ]


def test_logs() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.next_response = {
        "logs": [
            {
                "clusterJobId": "evKcsy8aLkqvKxCr",
                "daemon": "Streampyp",
                "timestamp": 1705851989949,
                "status": "Succeeded",
                "launchedTimestamp": 1705851990012,
                "finishedTimestamp": 1705852400000
            },
            {
                "clusterJobId": "evKfHWH0O8mHydhy",
                "daemon": "Streampyp",
                "timestamp": 1705852408097,
                "status": "Running",
                "launchedTimestamp": 1705852408150,
                "finishedTimestamp": None
            }
        ]
    }

    logs = client.services.sessions.logs('sid', SessionDaemon.Streampyp)

    assert transport.last_params == [
        'sid',
        'Streampyp'
    ]

    assert type(logs) is SessionLogs
    assert len(logs.logs) == 2

    assert logs.logs[0].cluster_job_id == 'evKcsy8aLkqvKxCr'
    assert logs.logs[0].daemon == SessionDaemon.Streampyp
    assert logs.logs[0].timestamp == 1705851989949
    assert logs.logs[0].status == RunStatus.Succeeded
    assert logs.logs[0].launched_timestamp == 1705851990012
    assert logs.logs[0].finished_timestamp == 1705852400000

    assert logs.logs[1].cluster_job_id == 'evKfHWH0O8mHydhy'
    assert logs.logs[1].daemon == SessionDaemon.Streampyp
    assert logs.logs[1].timestamp == 1705852408097
    assert logs.logs[1].status == RunStatus.Running
    assert logs.logs[1].launched_timestamp == 1705852408150
    assert logs.logs[1].finished_timestamp is None


def test_speeds() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.next_response = {
        "transfers": [13479.877999374827, 15856.886869345744]
    }

    speeds = client.services.sessions.speeds('sid')

    assert transport.last_params == [
        'sid'
    ]

    assert type(speeds) is SessionSpeeds
    assert speeds.transfers == [13479.877999374827, 15856.886869345744]


def test_jobs_logs() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.next_response = {
        "jobs": [
            {
                "clusterJobId": "evKcwVvPBZ1uzmjZ",
                "name": "spr_session",
                "timestamp": 1705852077023,
                "size": 1,
                "status": "Succeeded",
                "arrayInfo": None,
                "launchedTimestamp": 1705852077100,
                "finishedTimestamp": 1705852090000,
                "submittedTimestamp": 1705852077023
            },
            {
                "clusterJobId": "evKfKi58wMwBTBgQ",
                "name": "spr_session",
                "timestamp": 1705852585659,
                "size": 4,
                "status": "Waiting",
                "arrayInfo": None,
                "launchedTimestamp": None,
                "finishedTimestamp": None,
                "submittedTimestamp": 1705852585659
            }
        ]
    }

    logs = client.services.sessions.jobs_logs('sid')

    assert transport.last_params == [
        'sid'
    ]

    assert type(logs) is SessionJobsLogs
    assert len(logs.jobs) == 2

    assert type(logs.jobs[0]) is SessionJobLogData
    assert logs.jobs[0].cluster_job_id == 'evKcwVvPBZ1uzmjZ'
    assert logs.jobs[0].name == 'spr_session'
    assert logs.jobs[0].timestamp == 1705852077023
    assert logs.jobs[0].size == 1
    assert logs.jobs[0].status == RunStatus.Succeeded
    assert logs.jobs[0].array_info is None
    assert logs.jobs[0].launched_timestamp == 1705852077100
    assert logs.jobs[0].finished_timestamp == 1705852090000
    assert logs.jobs[0].submitted_timestamp == 1705852077023

    assert type(logs.jobs[1]) is SessionJobLogData
    assert logs.jobs[1].cluster_job_id == 'evKfKi58wMwBTBgQ'
    assert logs.jobs[1].name == 'spr_session'
    assert logs.jobs[1].timestamp == 1705852585659
    assert logs.jobs[1].size == 4
    assert logs.jobs[1].status == RunStatus.Waiting
    assert logs.jobs[1].array_info is None
    assert logs.jobs[1].launched_timestamp is None
    assert logs.jobs[1].finished_timestamp is None
    assert logs.jobs[1].submitted_timestamp == 1705852585659


def test_get_avg_rot() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.next_response = [
        {
            "spatialFreq": [0.0, 0.001393, 0.002786, 0.504178],
            "avgRot": [1.990037, -0.006064, -1.29E-4, 4.78E-4, 0.067398],
            "ctfFit": [0.07, 0.07263, 0.865495, 0.958357, 0.90474],
            "crossCorrelation": [1.0, 0.940056, -0.128977, 0.228127, 0.250241],
            "minRes": 50.0
        }
    ]

    avgrot = client.services.sessions.get_avg_rot('sid', 'did')

    assert transport.last_params == [
        'sid',
        'did'
    ]

    assert avgrot is not None
    assert type(avgrot) is AvgRotData
    assert avgrot.spatial_freq == [0.0, 0.001393, 0.002786, 0.504178]
    assert avgrot.avg_rot == [1.990037, -0.006064, -1.29E-4, 4.78E-4, 0.067398]
    assert avgrot.ctf_fit == [0.07, 0.07263, 0.865495, 0.958357, 0.90474]
    assert avgrot.cross_correlation == [1.0, 0.940056, -0.128977, 0.228127, 0.250241]
    assert avgrot.min_res == 50.0


def test_get_motion() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.next_response = [
        {
            "x": [-0.75364, 0.0, 0.21537],
            "y": [3.10289, -0.24007, -1.07419]
        }
    ]

    motion = client.services.sessions.get_motion('sid', 'did')

    assert transport.last_params == [
        'sid',
        'did'
    ]

    assert motion is not None
    assert type(motion) is MotionData
    assert motion.x == [-0.75364, 0.0, 0.21537]
    assert motion.y == [3.10289, -0.24007, -1.07419]


def test_data_log() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.next_response = "2024-01-21 10:53:44 [\u001b[32mINFO\u001b[0m] \u001b[1mpyp_main.py\u001b[0m:3260 | Job 20076339058923981_1 (v0.6.0) launching on streampyp using 1 task(s) \n"

    log = client.services.sessions.data_log('sid', 'did')

    assert transport.last_params == [
        'sid',
        'did'
    ]

    assert type(log) is str
    assert log == "2024-01-21 10:53:44 [\u001b[32mINFO\u001b[0m] \u001b[1mpyp_main.py\u001b[0m:3260 | Job 20076339058923981_1 (v0.6.0) launching on streampyp using 1 task(s) \n"


def test_list_filters() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.next_response = ['a', 'b']

    filters = client.services.sessions.list_filters('sid', PreprocessingFilterType.TABLE)

    assert transport.last_params == [
        'sid',
        'TABLE'
    ]

    assert type(filters) is list
    assert len(filters) == 2

    assert filters[0] == 'a'
    assert filters[1] == 'b'


def test_get_filter() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.next_response = {
        "name": "Cheese",
        "ranges": [
            {
                "propId": "micrograph/cccc",
                "min": 3.62,
                "max": 4.48
            },
            {
                "propId": "micrograph/time",
                "min": 1.7058525800541E12,
                "max": 1.70585258005461E12
            }
        ],
        "excludedIds": [],
        "selectedClasses": None,
        "selectedClassesReal": None,
        "selectedClassesFourier": None,
        "includedIds": None,
        "xPropId": None,
        "yPropId": None,
        "tableFilterNames": None,
        "plotFilterNames": None
    }

    filter = client.services.sessions.get_filter('sid', 'fid', PreprocessingFilterType.TABLE)

    assert transport.last_params == [
        'sid',
        'fid',
        'TABLE'
    ]

    assert type(filter) is PreprocessingFilter
    assert filter.name == 'Cheese'
    assert type(filter.ranges) is list
    assert len(filter.ranges) == 2

    assert type(filter.ranges[0]) is PreprocessingPropRange
    assert filter.ranges[0].prop_id == 'micrograph/cccc'
    assert filter.ranges[0].min == 3.62
    assert filter.ranges[0].max == 4.48

    assert type(filter.ranges[1]) is PreprocessingPropRange
    assert filter.ranges[1].prop_id == 'micrograph/time'
    assert filter.ranges[1].min == 1.7058525800541E12
    assert filter.ranges[1].max == 1.70585258005461E12

    assert filter.excluded_ids == []
    assert filter.selected_classes is None
    assert filter.selected_classes_real is None
    assert filter.selected_classes_fourier is None
    assert filter.included_ids is None
    assert filter.x_prop_id is None
    assert filter.y_prop_id is None
    assert filter.table_filter_names is None
    assert filter.plot_filter_names is None


def test_save_filter() -> None:

    transport = MockTransport()
    client = transport.client()

    filter = PreprocessingFilter(
        'Filter',
        [
            PreprocessingPropRange('micrograph/cccc', 1.2, 3.4),
            PreprocessingPropRange('micrograph/time', 5, 42)
        ],
        ['a', 'b'],
        None,
        [1, 3],
        None,
        ['c', 'd'],
        'micrograph/cccc',
        'micrograph/time',
        None,
        None
    )
    client.services.sessions.save_filter('sid', filter, PreprocessingFilterType.PLOT)

    assert transport.last_params == [
        'sid',
        {
            "name": "Filter",
            "ranges": [
                {
                    "propId": "micrograph/cccc",
                    "min": 1.2,
                    "max": 3.4
                },
                {
                    "propId": "micrograph/time",
                    "min": 5,
                    "max": 42
                }
            ],
            "excludedIds": ['a', 'b'],
            "selectedClasses": None,
            "selectedClassesReal": [1, 3],
            "selectedClassesFourier": None,
            "includedIds": ['c', 'd'],
            "xPropId": 'micrograph/cccc',
            "yPropId": 'micrograph/time',
            "tableFilterNames": None,
            "plotFilterNames": None
        },
        'PLOT'
    ]


def test_delete_filter() -> None:

    transport = MockTransport()
    client = transport.client()

    client.services.sessions.delete_filter('sid', 'fid', PreprocessingFilterType.TABLE)

    assert transport.last_params == [
        'sid',
        'fid',
        'TABLE'
    ]


def test_filter_options() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.next_response = [
        {
            "value": "__NONE__",
            "text": "(None)"
        },
        {
            "divider": True
        },
        {
            "value": "Filter A"
        }
    ]

    filters = client.services.sessions.filter_options('a', None, 'sid')

    assert transport.last_params == [
        'a',
        None,
        'sid'
    ]

    assert type(filters) is list
    assert len(filters) == 3

    assert type(filters[0]) is RemoteOption
    assert filters[0].value == '__NONE__'
    assert filters[0].text == '(None)'
    assert filters[0].divider is False

    assert type(filters[1]) is RemoteOption
    assert filters[1].value is None
    assert filters[1].text is None
    assert filters[1].divider is True

    assert type(filters[2]) is RemoteOption
    assert filters[2].value == 'Filter A'
    assert filters[2].text is None
    assert filters[2].divider is False


def test_export() -> None:

    transport = MockTransport()
    client = transport.client()

    request = SessionExportRequestFilter('Filter A', PreprocessingFilterType.TABLE)
    client.services.sessions.export('a', request.serialize(), '')

    assert transport.last_params == [
        "a",
        "{\"type\": \"edu.duke.bartesaghi.micromon.services.SessionExportRequest.Filter\", \"name\": \"Filter A\", \"filterType\": \"TABLE\"}",
        ""
    ]


def test_export_cancel() -> None:

    transport = MockTransport()
    client = transport.client()

    client.services.sessions.cancel_export('eid')

    assert transport.last_params == [
        'eid'
    ]
