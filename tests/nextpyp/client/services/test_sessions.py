
from nextpyp.client.args import block_args, PypArgValues, PypBlock
from nextpyp.client.gen import SessionPermission

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
    arg_values = PypArgValues.from_toml(block_args(PypBlock.SessionSingleParticle), sessions[0].args.finished.values)
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

# TODO: test tomo list
# TODO: test other session functions
