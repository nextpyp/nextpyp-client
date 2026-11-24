
import pytest

from nextpyp.client.gen import (
    ClusterJobResultType,
    ImageDims,
    MicrographMetadata,
    PreprocessingFilterType,
    PypStats,
    RealTimeC2SListenToSession,
    RealTimeC2SSessionSettingsSaved,
    RealTimeS2CError,
    RealTimeS2CSessionDaemonFinished,
    RealTimeS2CSessionDaemonStarted,
    RealTimeS2CSessionDaemonSubmitted,
    RealTimeS2CSessionExport,
    RealTimeS2CSessionFilesystem,
    RealTimeS2CSessionFilesystems,
    RealTimeS2CSessionJobFinished,
    RealTimeS2CSessionJobStarted,
    RealTimeS2CSessionJobSubmitted,
    RealTimeS2CSessionLargeData,
    RealTimeS2CSessionMicrograph,
    RealTimeS2CSessionRunningJob,
    RealTimeS2CSessionSmallData,
    RealTimeS2CSessionStatus,
    RealTimeS2CSessionTiltSeries,
    RealTimeS2CSessionTransferFinished,
    RealTimeS2CSessionTransferInit,
    RealTimeS2CSessionTransferInitFileInfo,
    RealTimeS2CSessionTransferProgress,
    RealTimeS2CSessionTransferStarted,
    RealTimeS2CSessionTransferWaiting,
    RealTimeS2CSessionTwoDClasses,
    RealTimeS2CUpdatedParameters,
    RunStatus,
    SessionDaemon,
    SessionExportData,
    SessionExportRequest,
    SessionExportRequestFilter,
    SessionExportResultFailed,
    SessionExportResult,
    TiltSeriesData,
    TwoDClassData,
    TwoDClassesData
)
from nextpyp.client.realtime import RealtimeServiceError

from testlib import MockTransport


pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
async def test_send_listen() -> None:

    transport = MockTransport()
    client = transport.client()

    async with client.realtime_services.single_particle_session as srv:
        await srv.send_listen_to_session(RealTimeC2SListenToSession(
            session_id='sid'
        ))

    assert transport.get_last_sent_message() == {
        'type': RealTimeC2SListenToSession.TYPE_ID,
        'sessionId': 'sid'
    }


@pytest.mark.asyncio
async def test_send_session_settings_saved() -> None:

    transport = MockTransport()
    client = transport.client()

    async with client.realtime_services.single_particle_session as srv:
        await srv.send_session_settings_saved(RealTimeC2SSessionSettingsSaved())

    assert transport.get_last_sent_message() == {
        'type': RealTimeC2SSessionSettingsSaved.TYPE_ID
    }


@pytest.mark.asyncio
async def test_recv_error() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.set_next_recv_message({
        'type': RealTimeS2CError.TYPE_ID,
        'name': 'Foo',
        'msg': 'bar'
    })

    async with client.realtime_services.single_particle_session as srv:
        with pytest.raises(RealtimeServiceError) as ex_info:
            await srv.recv()
        assert ex_info.value.e.name == 'Foo'
        assert ex_info.value.e.msg == 'bar'


@pytest.mark.asyncio
async def test_recv_status() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.set_next_recv_message({
        "type": "edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionStatus",
        "daemonsRunning": [False, False, False],
        "jobsRunning": [
            {
                "jobId": "jid",
                "name": "The Job",
                "size": 5,
                "status": "Running",
                "arrayInfo": None,
                "launchedTimestamp": 1705851990000,
                "finishedTimestamp": None,
                "submittedTimestamp": 1705851989949
            }
        ]
    })

    async with client.realtime_services.single_particle_session as srv:
        msg = await srv.recv()

    assert msg == RealTimeS2CSessionStatus(
        daemons_running=[False, False, False],
        jobs_running=[
            RealTimeS2CSessionRunningJob(
                job_id='jid',
                name='The Job',
                size=5,
                status=RunStatus.Running,
                array_info=None,
                launched_timestamp=1705851990000,
                finished_timestamp=None,
                submitted_timestamp=1705851989949
            )
        ]
    )


@pytest.mark.asyncio
async def test_recv_small_data() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.set_next_recv_message({
        "type": "edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionSmallData",
        "exports": [
            {
                "sessionId": "evKcXLQz3JlrDgV6",
                "exportId": "exnNcFR3PJe2IeKl",
                "request": "{\"type\": \"edu.duke.bartesaghi.micromon.services.SessionExportRequest.Filter\", \"name\": \"Cheese\", \"filterType\": \"TABLE\"}",
                "created": 1707508385501,
                "clusterJobId": "exnNcFR3PJe2IeKm",
                "result": "{\"type\": \"edu.duke.bartesaghi.micromon.services.SessionExportResult.Failed\", \"reason\": \"The cluster job failed\"}"
            },
            {
                "sessionId": "evKcXLQz3JlrDgV6",
                "exportId": "exnUOmyr7tXLR90H",
                "request": "{\"type\": \"edu.duke.bartesaghi.micromon.services.SessionExportRequest.Filter\", \"name\": \"Cheese\", \"filterType\": \"TABLE\"}",
                "created": 1707509571120,
                "clusterJobId": "exnUOmyr7tXLR90I",
                "result":"{\"type\": \"edu.duke.bartesaghi.micromon.services.SessionExportResult.Failed\", \"reason\": \"The cluster job failed\"}"
            }
        ]
    })

    async with client.realtime_services.single_particle_session as srv:
        msg = await srv.recv()

    assert msg == RealTimeS2CSessionSmallData(
        exports=[
            SessionExportData(
                session_id="evKcXLQz3JlrDgV6",
                export_id="exnNcFR3PJe2IeKl",
                request=SessionExportRequestFilter('Cheese', PreprocessingFilterType.TABLE).serialize(),
                created=1707508385501,
                cluster_job_id='exnNcFR3PJe2IeKm',
                result=SessionExportResultFailed('The cluster job failed').serialize()
            ),
            SessionExportData(
                session_id="evKcXLQz3JlrDgV6",
                export_id="exnUOmyr7tXLR90H",
                request=SessionExportRequestFilter('Cheese', PreprocessingFilterType.TABLE).serialize(),
                created=1707509571120,
                cluster_job_id='exnUOmyr7tXLR90I',
                result=SessionExportResultFailed('The cluster job failed').serialize()
            )
        ]
    )

    assert type(msg) is RealTimeS2CSessionSmallData
    assert SessionExportRequest.deserialize(msg.exports[0].request) == SessionExportRequestFilter('Cheese', PreprocessingFilterType.TABLE)
    assert msg.exports[0].result is not None
    assert SessionExportResult.deserialize(msg.exports[0].result) == SessionExportResultFailed('The cluster job failed')


@pytest.mark.asyncio
async def test_recv_large_data() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.set_next_recv_message({
        "type": "edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionLargeData",
        "autoVirionsCount": 5,
        "autoParticlesCount": 42,
        "micrographs": [
            {
                "id": "20201009_1138_NBtest_A007_G001_H079_D007",
                "timestamp": 1705852580054,
                "ccc": 0.26655301451683044,
                "cccc": 3.554455041885376,
                "defocus1": 22489.82421875,
                "defocus2": 21469.396484375,
                "angleAstig": -68.99641418457031,
                "averageMotion": 0.966963111549991,
                "maxMotion": 2.0543212890625,
                "numAutoParticles": 0,
                "imageDims": {
                    "width": 5760,
                    "height": 4092,
                    "depth": 1,
                    "binningFactor": 2,
                    "pixelA": 1.2,
                    "binningFactorZ": 1
                }
            }
        ],
        "tiltSerieses": [
            {
                "id": "tilt_series",
                "timestamp": 1677180769930,
                "ccc": 0.028843000531196594,
                "cccc": 718.0,
                "defocus1": 5611.99365234375,
                "defocus2": 5078.1337890625,
                "angleAstig": 45.86092758178711,
                "averageMotion": 188.23980617348099,
                "maxMotion": 412.5,
                "numAutoParticles": 3,
                "numAutoVirions": 5,
                "imageDims": {
                    "width": 1536,
                    "height": 1536,
                    "depth": 10,
                    "binningFactor": 1,
                    "pixelA": 1.2,
                    "binningFactorZ": 1
                },
                "dataBin": 2,
                "missAlignLoss": None
            }
        ],
        "twoDClasses": [
            {
                "ownerId": "oid",
                "twoDClassesId": "2Did",
                "created": 5,
                "classes": [
                    {
                        "classNum": 1,
                        "numParticles": 1234,
                        "metadata": {"resolution": 8.5},
                        "classScore": 0.75
                    }
                ],
                "metadataLabels": ["resolution"],
                "splitIndex": None
            }
        ],
        "last": False
    })

    async with client.realtime_services.single_particle_session as srv:
        msg = await srv.recv()

    assert msg == RealTimeS2CSessionLargeData(
        auto_virions_count=5,
        auto_particles_count=42,
        micrographs=[
            MicrographMetadata(
                id="20201009_1138_NBtest_A007_G001_H079_D007",
                timestamp=1705852580054,
                ccc=0.26655301451683044,
                cccc=3.554455041885376,
                defocus1=22489.82421875,
                defocus2=21469.396484375,
                angle_astig=-68.99641418457031,
                average_motion=0.966963111549991,
                max_motion=2.0543212890625,
                num_auto_particles=0,
                image_dims=ImageDims(
                    width=5760,
                    height=4092,
                    depth=1,
                    binning_factor=2,
                    pixel_a=1.2,
                    binning_factor_z=1
                )
            )
        ],
        tilt_serieses=[
            TiltSeriesData(
                id="tilt_series",
                timestamp=1677180769930,
                ccc=0.028843000531196594,
                cccc=718.0,
                defocus1=5611.99365234375,
                defocus2=5078.1337890625,
                angle_astig=45.86092758178711,
                average_motion=188.23980617348099,
                max_motion=412.5,
                num_auto_particles=3,
                num_auto_virions=5,
                image_dims=ImageDims(
                    width=1536,
                    height=1536,
                    depth=10,
                    binning_factor=1,
                    pixel_a=1.2,
                    binning_factor_z=1
                ),
                data_bin=2,
                miss_align_loss=None
            )
        ],
        two_dclasses=[
            TwoDClassesData(
                owner_id='oid',
                two_dclasses_id='2Did',
                created=5,
                classes=[
                    TwoDClassData(
                        class_num=1,
                        num_particles=1234,
                        metadata={'resolution': 8.5},
                        class_score=0.75
                    )
                ],
                metadata_labels=['resolution'],
                split_index=None
            )
        ],
        last=False
    )


@pytest.mark.asyncio
async def test_recv_updated_parameters() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.set_next_recv_message({
        "type": "edu.duke.bartesaghi.micromon.services.RealTimeS2C.UpdatedParameters",
        "pypStats": {
            "scopeVoltage": 1.2,
            "scopePixel": 3.4,
            "scopeDoseRate": None
        }
    })

    async with client.realtime_services.single_particle_session as srv:
        msg = await srv.recv()

    assert msg == RealTimeS2CUpdatedParameters(
        pyp_stats=PypStats(
            scope_voltage=1.2,
            scope_pixel=3.4,
            scope_dose_rate=None
        )
    )


@pytest.mark.asyncio
async def test_recv_session_micrograph() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.set_next_recv_message({
        "type": "edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionMicrograph",
        "micrograph": {
            "id": "20201009_1138_NBtest_A007_G001_H079_D007",
            "timestamp": 1705852580054,
            "ccc": 0.26655301451683044,
            "cccc": 3.554455041885376,
            "defocus1": 22489.82421875,
            "defocus2": 21469.396484375,
            "angleAstig": -68.99641418457031,
            "averageMotion": 0.966963111549991,
            "maxMotion": 2.0543212890625,
            "numAutoParticles": 0,
            "imageDims": {
                "width": 5760,
                "height": 4092,
                "depth": 1,
                "binningFactor": 2,
                "pixelA": 1.2,
                "binningFactorZ": 1
            }
        }
    })

    async with client.realtime_services.single_particle_session as srv:
        msg = await srv.recv()

    assert msg == RealTimeS2CSessionMicrograph(
        micrograph=MicrographMetadata(
            id="20201009_1138_NBtest_A007_G001_H079_D007",
            timestamp=1705852580054,
            ccc=0.26655301451683044,
            cccc=3.554455041885376,
            defocus1=22489.82421875,
            defocus2=21469.396484375,
            angle_astig=-68.99641418457031,
            average_motion=0.966963111549991,
            max_motion=2.0543212890625,
            num_auto_particles=0,
            image_dims=ImageDims(
                width=5760,
                height=4092,
                depth=1,
                binning_factor=2,
                pixel_a=1.2,
                binning_factor_z=1
            )
        )
    )


@pytest.mark.asyncio
async def test_recv_session_tilt_series() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.set_next_recv_message({
        "type": "edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionTiltSeries",
        "tiltSeries": {
            "id": "tilt_series",
            "timestamp": 1677180769930,
            "ccc": 0.028843000531196594,
            "cccc": 718.0,
            "defocus1": 5611.99365234375,
            "defocus2": 5078.1337890625,
            "angleAstig": 45.86092758178711,
            "averageMotion": 188.23980617348099,
            "maxMotion": 412.5,
            "numAutoParticles": 0,
            "numAutoVirions": 0,
            "imageDims": {
                "width": 1536,
                "height": 1536,
                "depth": 10,
                "binningFactor": 1,
                "pixelA": 1.2,
                "binningFactorZ": 1
            },
            "dataBin": 1,
            "missAlignLoss": None
        }
    })

    async with client.realtime_services.tomography_session as srv:
        msg = await srv.recv()

    assert msg == RealTimeS2CSessionTiltSeries(
        tilt_series=TiltSeriesData(
            id="tilt_series",
            timestamp=1677180769930,
            ccc=0.028843000531196594,
            cccc=718.0,
            defocus1=5611.99365234375,
            defocus2=5078.1337890625,
            angle_astig=45.86092758178711,
            average_motion=188.23980617348099,
            max_motion=412.5,
            num_auto_particles=0,
            num_auto_virions=0,
            image_dims=ImageDims(
                width=1536,
                height=1536,
                depth=10,
                binning_factor=1,
                pixel_a=1.2,
                binning_factor_z=1
            ),
            data_bin=1,
            miss_align_loss=None
        )
    )


@pytest.mark.asyncio
async def test_recv_session_twod_classes() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.set_next_recv_message({
        "type": "edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionTwoDClasses",
        "twoDClasses": {
            "ownerId": "oid",
            "twoDClassesId": "2Did",
            "created": 5,
            "classes": [
                {
                    "classNum": 1,
                    "numParticles": 1234,
                    "metadata": {"resolution": 8.5},
                    "classScore": 0.75
                }
            ],
            "metadataLabels": ["resolution"],
            "splitIndex": None
        }
    })

    async with client.realtime_services.single_particle_session as srv:
        msg = await srv.recv()

    assert msg == RealTimeS2CSessionTwoDClasses(
        two_dclasses=TwoDClassesData(
            owner_id='oid',
            two_dclasses_id='2Did',
            created=5,
            classes=[
                TwoDClassData(
                    class_num=1,
                    num_particles=1234,
                    metadata={'resolution': 8.5},
                    class_score=0.75
                )
            ],
            metadata_labels=['resolution'],
            split_index=None
        )
    )


@pytest.mark.asyncio
async def test_recv_session_export() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.set_next_recv_message({
        "type": "edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionExport",
        "export": {
            "sessionId": "evKcXLQz3JlrDgV6",
            "exportId": "exnUOmyr7tXLR90H",
            "request": "{\"type\": \"edu.duke.bartesaghi.micromon.services.SessionExportRequest.Filter\", \"name\": \"Cheese\", \"filterType\": \"TABLE\"}",
            "created": 1707509571120,
            "clusterJobId": "exnUOmyr7tXLR90I",
            "result":"{\"type\": \"edu.duke.bartesaghi.micromon.services.SessionExportResult.Failed\", \"reason\": \"The cluster job failed\"}"
        }
    })

    async with client.realtime_services.single_particle_session as srv:
        msg = await srv.recv()

    assert msg == RealTimeS2CSessionExport(
        export=SessionExportData(
            session_id="evKcXLQz3JlrDgV6",
            export_id="exnUOmyr7tXLR90H",
            request=SessionExportRequestFilter('Cheese', PreprocessingFilterType.TABLE).serialize(),
            created=1707509571120,
            cluster_job_id='exnUOmyr7tXLR90I',
            result=SessionExportResultFailed('The cluster job failed').serialize()
        )
    )

    assert type(msg) is RealTimeS2CSessionExport
    assert SessionExportRequest.deserialize(msg.export.request) == SessionExportRequestFilter('Cheese', PreprocessingFilterType.TABLE)
    assert msg.export.result is not None
    assert SessionExportResult.deserialize(msg.export.result) == SessionExportResultFailed('The cluster job failed')


@pytest.mark.asyncio
async def test_recv_session_filesystems() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.set_next_recv_message({
        "type": "edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionFilesystems",
        "filesystems": [
            {
                "path": "/media/rawdata",
                "type": "vboxsf",
                "bytes": 885004435456,
                "bytesUsed": 715606044672
            }
        ]
    })

    async with client.realtime_services.single_particle_session as srv:
        msg = await srv.recv()

    assert msg == RealTimeS2CSessionFilesystems(
        filesystems=[
            RealTimeS2CSessionFilesystem(
                path='/media/rawdata',
                type='vboxsf',
                bytes=885004435456,
                bytes_used=715606044672
            )
        ]
    )


@pytest.mark.asyncio
async def test_recv_session_transfer_init() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.set_next_recv_message({
        "type": "edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionTransferInit",
        "files": [
            {
                "filename": "K3_gain.mrc",
                "bytesTotal": 94280704,
                "bytesTransfered": 94280704
            },
            {
                "filename": "20201009_1138_NBtest_A007_G001_H079_D007.tif",
                "bytesTotal": 416194010,
                "bytesTransfered": 416194009
            }
        ]
    })

    async with client.realtime_services.single_particle_session as srv:
        msg = await srv.recv()

    assert msg == RealTimeS2CSessionTransferInit(
        files=[
            RealTimeS2CSessionTransferInitFileInfo(
                filename='K3_gain.mrc',
                bytes_total=94280704,
                bytes_transfered=94280704
            ),
            RealTimeS2CSessionTransferInitFileInfo(
                filename='20201009_1138_NBtest_A007_G001_H079_D007.tif',
                bytes_total=416194010,
                bytes_transfered=416194009
            )
        ]
    )


@pytest.mark.asyncio
async def test_recv_session_transfer_waiting() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.set_next_recv_message({
        "type": "edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionTransferWaiting",
        "filename": "foo"
    })

    async with client.realtime_services.single_particle_session as srv:
        msg = await srv.recv()

    assert msg == RealTimeS2CSessionTransferWaiting(
        filename='foo'
    )


@pytest.mark.asyncio
async def test_recv_session_transfer_started() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.set_next_recv_message({
        "type": "edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionTransferStarted",
        "filename": "foo",
        "bytesTotal": 5
    })

    async with client.realtime_services.single_particle_session as srv:
        msg = await srv.recv()

    assert msg == RealTimeS2CSessionTransferStarted(
        filename='foo',
        bytes_total=5
    )


@pytest.mark.asyncio
async def test_recv_session_transfer_progress() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.set_next_recv_message({
        "type": "edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionTransferProgress",
        "filename": "bar",
        "bytesTransferred": 42
    })

    async with client.realtime_services.single_particle_session as srv:
        msg = await srv.recv()

    assert msg == RealTimeS2CSessionTransferProgress(
        filename='bar',
        bytes_transferred=42
    )


@pytest.mark.asyncio
async def test_recv_session_transfer_finished() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.set_next_recv_message({
        "type": "edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionTransferFinished",
        "filename": "cow"
    })

    async with client.realtime_services.single_particle_session as srv:
        msg = await srv.recv()

    assert msg == RealTimeS2CSessionTransferFinished(
        filename='cow'
    )


@pytest.mark.asyncio
async def test_recv_session_daemon_submitted() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.set_next_recv_message({
        "type": "edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionDaemonSubmitted",
        "jobId": "jid",
        "daemon": "Pypd"
    })

    async with client.realtime_services.single_particle_session as srv:
        msg = await srv.recv()

    assert msg == RealTimeS2CSessionDaemonSubmitted(
        job_id='jid',
        daemon=SessionDaemon.Pypd
    )


@pytest.mark.asyncio
async def test_recv_session_daemon_started() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.set_next_recv_message({
        "type": "edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionDaemonStarted",
        "jobId": "jid",
        "daemon": "Fypd"
    })

    async with client.realtime_services.single_particle_session as srv:
        msg = await srv.recv()

    assert msg == RealTimeS2CSessionDaemonStarted(
        job_id='jid',
        daemon=SessionDaemon.Fypd
    )


@pytest.mark.asyncio
async def test_recv_session_daemon_finished() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.set_next_recv_message({
        "type": "edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionDaemonFinished",
        "jobId": "jid",
        "daemon": "Streampyp"
    })

    async with client.realtime_services.single_particle_session as srv:
        msg = await srv.recv()

    assert msg == RealTimeS2CSessionDaemonFinished(
        job_id='jid',
        daemon=SessionDaemon.Streampyp
    )


@pytest.mark.asyncio
async def test_recv_session_job_submitted() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.set_next_recv_message({
        "type": "edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionJobSubmitted",
        "jobId": "jid",
        "name": "foo",
        "size": 5
    })

    async with client.realtime_services.single_particle_session as srv:
        msg = await srv.recv()

    assert msg == RealTimeS2CSessionJobSubmitted(
        job_id='jid',
        name='foo',
        size=5
    )


@pytest.mark.asyncio
async def test_recv_session_job_started() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.set_next_recv_message({
        "type": "edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionJobStarted",
        "jobId": "jid"
    })

    async with client.realtime_services.single_particle_session as srv:
        msg = await srv.recv()

    assert msg == RealTimeS2CSessionJobStarted(
        job_id='jid'
    )


@pytest.mark.asyncio
async def test_recv_session_job_finished() -> None:

    transport = MockTransport()
    client = transport.client()
    transport.set_next_recv_message({
        "type": "edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionJobFinished",
        "jobId": "jid",
        "resultType": "Success"
    })

    async with client.realtime_services.single_particle_session as srv:
        msg = await srv.recv()

    assert msg == RealTimeS2CSessionJobFinished(
        job_id='jid',
        result_type=ClusterJobResultType.Success
    )
