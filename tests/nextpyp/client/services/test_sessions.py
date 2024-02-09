
from nextpyp.client.args import block_args, PypArgValues, PypBlock
from nextpyp.client.gen import (
    RemoteOption,
    SessionPermission,
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
                    "groupId": "eaNh61SZ9DmeeCjD",
                    "values": "data_path = \"/media/pyp/tests/spr/raw/*.tif\"\ngain_reference = \"/media/pyp/tests/spr/raw/K3_gain.mrc\"\nscope_pixel = 1\nscope_voltage = 300\ndetect_rad = 75\ndetect_method = \"all\"\nclass2d_min = 10\nslurm_verbose = true\nslurm_memory = 2\nslurm_class2d_memory = 2\n"
                }
            },
            "display": {
                "finished": {
                    "groupName": "Bartesaghi Lab"
                }
            },
            "numMicrographs": 2,
            "numFrames": 120
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
    assert sessions[0].args.finished.group_id == "eaNh61SZ9DmeeCjD"
    assert sessions[0].args.finished.values.startswith('data_path = ')
    assert sessions[0].args.next is None
    assert sessions[0].display.finished is not None
    assert sessions[0].display.finished.group_name == 'Bartesaghi Lab'
    assert sessions[0].display.next is None
    assert sessions[0].num_micrographs == 2
    assert sessions[0].num_frames == 120

    # check the pyp args
    arg_values = PypArgValues.from_toml(block_args(PypBlock.SESSION_SINGLE_PARTICLE), sessions[0].args.finished.values)
    assert arg_values.data_path == '/media/pyp/tests/spr/raw/*.tif'
    assert arg_values.gain_reference == '/media/pyp/tests/spr/raw/K3_gain.mrc'
    assert arg_values.scope_pixel == 1.0
    assert arg_values.scope_voltage == 300
    assert arg_values.detect_rad == 75.0
    assert arg_values.detect_method == 'all'
    assert arg_values.class2d_min == 10
    assert arg_values.slurm_verbose is True
    assert arg_values.slurm_memory == 2
    assert arg_values.slurm_class2d_memory == 2


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
                "groupId": "groupid",
                "values": "data_path = \"/foo/bar\"\nscope_pixel = 1.0\nslurm_verbose = true\nslurm_memory = 2\n"
            }
        },
        "display": {
            "next": {
                "groupName": "Bob"
            }
        },
        "numMicrographs": 0,
        "numFrames": 0
    }

    pyp_args = PypArgValues.from_toml(block_args(PypBlock.SESSION_SINGLE_PARTICLE))
    pyp_args.data_path = '/foo/bar'
    pyp_args.scope_pixel = 1
    pyp_args.slurm_verbose = True
    pyp_args.slurm_memory = 2
    args = SingleParticleSessionArgs(
        'My new session',
        'groupid',
        pyp_args.write()
    )
    session = client.services.single_particle_sessions.create(args)

    assert transport.last_params == [
        {
            'name': 'My new session',
            'groupId': 'groupid',
            'values': 'data_path = \"/foo/bar\"\nscope_pixel = 1.0\nslurm_verbose = true\nslurm_memory = 2\n'
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
    assert session.args.next.group_id == 'groupid'
    assert session.args.next.values == "data_path = \"/foo/bar\"\nscope_pixel = 1.0\nslurm_verbose = true\nslurm_memory = 2\n"
    assert session.display.finished is None
    assert session.display.next is not None
    assert session.display.next.group_name == 'Bob'
    assert session.num_micrographs == 0
    assert session.num_frames == 0


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
        "numFrames": 0
    }

    pyp_args = PypArgValues.from_toml(block_args(PypBlock.SESSION_SINGLE_PARTICLE))
    pyp_args.data_path = '/foo/bar'
    args = SingleParticleSessionArgs(
        'My new session',
        'groupid',
        pyp_args.write()
    )
    session = client.services.single_particle_sessions.edit('sid', args)

    assert transport.last_params == [
        'sid',
        {
            'name': 'My new session',
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
        "numFrames": 0
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
                    "groupId": "drGkM99qI3bEpLmo",
                    "values": "data_path = \"/media/pyp/tests/tomo/raw/tilt*.mrc\"\nscope_pixel = 1\nscope_voltage = 300\nstream_transfer_fileset = \".order,.rawtlt\"\nmovie_no_frames = true\n"
                },
                "next": {
                    "name": "New Tomography Session",
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
            "numTilts": 10
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
    assert sessions[0].args.finished.group_id == "drGkM99qI3bEpLmo"
    assert sessions[0].args.finished.values.startswith('data_path = ')
    assert sessions[0].args.next is not None
    assert sessions[0].args.next.name == "New Tomography Session"
    assert sessions[0].args.next.group_id == "eaNh61SZ9DmeeCjD"
    assert sessions[0].args.next.values.startswith('data_path = ')
    assert sessions[0].display.finished is not None
    assert sessions[0].display.finished.group_name == '(unknown group)'
    assert sessions[0].display.next is not None
    assert sessions[0].display.next.group_name == 'Bartesaghi Lab'
    assert sessions[0].num_tilt_series == 1
    assert sessions[0].num_tilts == 10

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
                "groupId": "groupid",
                "values": "data_path = \"/foo/bar\"\nscope_pixel = 1.0\nslurm_verbose = true\nslurm_memory = 2\n"
            }
        },
        "display": {
            "next": {
                "groupName": "Bob"
            }
        },
        "numTiltSeries": 0,
        "numTilts": 0
    }

    pyp_args = PypArgValues.from_toml(block_args(PypBlock.SESSION_TOMOGRAPHY))
    pyp_args.data_path = '/foo/bar'
    pyp_args.scope_pixel = 1
    pyp_args.slurm_verbose = True
    pyp_args.slurm_memory = 2
    args = TomographySessionArgs(
        'My new session',
        'groupid',
        pyp_args.write()
    )
    session = client.services.tomography_sessions.create(args)

    assert transport.last_params == [
        {
            'name': 'My new session',
            'groupId': 'groupid',
            'values': 'data_path = \"/foo/bar\"\nscope_pixel = 1.0\nslurm_verbose = true\nslurm_memory = 2\n'
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
    assert session.args.next.group_id == 'groupid'
    assert session.args.next.values == "data_path = \"/foo/bar\"\nscope_pixel = 1.0\nslurm_verbose = true\nslurm_memory = 2\n"
    assert session.display.finished is None
    assert session.display.next is not None
    assert session.display.next.group_name == 'Bob'
    assert session.num_tilt_series == 0
    assert session.num_tilts == 0


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
        "numTilts": 0
    }

    pyp_args = PypArgValues.from_toml(block_args(PypBlock.SESSION_TOMOGRAPHY))
    pyp_args.data_path = '/foo/bar'
    args = TomographySessionArgs(
        'My new session',
        'groupid',
        pyp_args.write()
    )
    session = client.services.tomography_sessions.edit('sid', args)

    assert transport.last_params == [
        'sid',
        {
            'name': 'My new session',
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
        "numTilts": 0
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

    assert len(options) == 2

    assert type(options[0]) is RemoteOption
    assert options[0].value == 'eQMBiHKJK5YsOLdQ'
    assert options[0].text == 'Single-particle'

    assert type(options[1]) is RemoteOption
    assert options[1].value == 'evKcXLQz3JlrDgV6'
    assert options[1].text == 'S2-Test blank'


# TODO: test other session functions
