
from __future__ import annotations

from typing import Optional, List, Dict, Set, Any, Iterator, TYPE_CHECKING

from nextpyp.client.realtime import RealtimeService

if TYPE_CHECKING:
    from nextpyp.client import Client


class Services:

    def __init__(self, client: Client) -> None:
        self.projects = ProjectsService(client)


class ProjectsService:

    def __init__(self, client: Client) -> None:
        self.client = client

    def list(self, user_id: str) -> List[ProjectData]:
        path = '/kv/projects/list'
        response = self.client._call(path, [user_id])
        if response is None:
            raise Exception(f'response expected from {path}, but none received')
        return [ProjectData.from_json(x) for x in response]


class RealtimeServices:

    def __init__(self, client: Client) -> None:
        self.project = RealtimeService(client, '/ws/project')


class ProjectData:

    def __init__(self, owner: UserData, permissions: Set[ProjectPermission], project_id: str, project_number: Optional[int], project_name: str, created: int, images: List[str], path: str) -> None:
        self.owner = owner
        self.permissions = permissions
        self.project_id = project_id
        self.project_number = project_number
        self.project_name = project_name
        self.created = created
        self.images = images
        self.path = path

    def to_json(self) -> Dict[str,Any]:
        return {
            'owner': self.owner.to_json(),
            'permissions': [x.to_json() for x in self.permissions],
            'projectId': self.project_id,
            'projectNumber': self.project_number if self.project_number is not None else None,
            'projectName': self.project_name,
            'created': self.created,
            'images': [x for x in self.images],
            'path': self.path,
        }

    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> ProjectData:
        return cls(
            owner=UserData.from_json(json['owner']),
            permissions={ProjectPermission.from_json(x) for x in json['permissions']},
            project_id=json['projectId'],
            project_number=json['projectNumber'] if 'projectNumber' in json and json['projectNumber'] is not None else None,
            project_name=json['projectName'],
            created=json['created'],
            images=[x for x in json['images']],
            path=json['path'],
        )

    def __str__(self) -> str:
        props = ', '.join([
            f'owner={self.owner}',
            f'permissions={self.permissions}',
            f'project_id={self.project_id}',
            f'project_number={self.project_number}',
            f'project_name={self.project_name}',
            f'created={self.created}',
            f'images={self.images}',
            f'path={self.path}',
        ])
        return f'ProjectData[{props}]'

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> Any:
        if not isinstance(other, ProjectData):
            return NotImplemented
        return self.owner == other.owner \
            and self.permissions == other.permissions \
            and self.project_id == other.project_id \
            and self.project_number == other.project_number \
            and self.project_name == other.project_name \
            and self.created == other.created \
            and self.images == other.images \
            and self.path == other.path


class RealTimeC2S:


    def to_json(self) -> Dict[str,Any]:
        return {
        }

    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> RealTimeC2S:
        return cls(
        )

    def __str__(self) -> str:
        props = ', '.join([
        ])
        return f'RealTimeC2S[{props}]'

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RealTimeC2S):
            return NotImplemented
        return True  # we are all the same! =D


    class ListenToProject:

        def __init__(self, user_id: str, project_id: str) -> None:
            self.user_id = user_id
            self.project_id = project_id

        def to_json(self) -> Dict[str,Any]:
            return {
                'userId': self.user_id,
                'projectId': self.project_id,
            }

        @classmethod
        def from_json(cls, json: Dict[str,Any]) -> RealTimeC2S.ListenToProject:
            return cls(
                user_id=json['userId'],
                project_id=json['projectId'],
            )

        def __str__(self) -> str:
            props = ', '.join([
                f'user_id={self.user_id}',
                f'project_id={self.project_id}',
            ])
            return f'ListenToProject[{props}]'

        def __repr__(self) -> str:
            return self.__str__()

        def __eq__(self, other: object) -> Any:
            if not isinstance(other, RealTimeC2S.ListenToProject):
                return NotImplemented
            return self.user_id == other.user_id \
                and self.project_id == other.project_id


class RealTimeS2C:


    def to_json(self) -> Dict[str,Any]:
        return {
        }

    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> RealTimeS2C:
        return cls(
        )

    def __str__(self) -> str:
        props = ', '.join([
        ])
        return f'RealTimeS2C[{props}]'

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RealTimeS2C):
            return NotImplemented
        return True  # we are all the same! =D


    class ProjectStatus:

        def __init__(self, recent_runs: List[ProjectRunData], has_older_runs: bool, blocks: List[Block]) -> None:
            self.recent_runs = recent_runs
            self.has_older_runs = has_older_runs
            self.blocks = blocks

        def to_json(self) -> Dict[str,Any]:
            return {
                'recentRuns': [x.to_json() for x in self.recent_runs],
                'hasOlderRuns': self.has_older_runs,
                'blocks': [x.to_json() for x in self.blocks],
            }

        @classmethod
        def from_json(cls, json: Dict[str,Any]) -> RealTimeS2C.ProjectStatus:
            return cls(
                recent_runs=[ProjectRunData.from_json(x) for x in json['recentRuns']],
                has_older_runs=json['hasOlderRuns'],
                blocks=[Block.from_json(x) for x in json['blocks']],
            )

        def __str__(self) -> str:
            props = ', '.join([
                f'recent_runs={self.recent_runs}',
                f'has_older_runs={self.has_older_runs}',
                f'blocks={self.blocks}',
            ])
            return f'ProjectStatus[{props}]'

        def __repr__(self) -> str:
            return self.__str__()

        def __eq__(self, other: object) -> Any:
            if not isinstance(other, RealTimeS2C.ProjectStatus):
                return NotImplemented
            return self.recent_runs == other.recent_runs \
                and self.has_older_runs == other.has_older_runs \
                and self.blocks == other.blocks


    class ProjectRunInit:

        def __init__(self, run_id: int, timestamp: int, job_ids: List[str]) -> None:
            self.run_id = run_id
            self.timestamp = timestamp
            self.job_ids = job_ids

        def to_json(self) -> Dict[str,Any]:
            return {
                'runId': self.run_id,
                'timestamp': self.timestamp,
                'jobIds': [x for x in self.job_ids],
            }

        @classmethod
        def from_json(cls, json: Dict[str,Any]) -> RealTimeS2C.ProjectRunInit:
            return cls(
                run_id=json['runId'],
                timestamp=json['timestamp'],
                job_ids=[x for x in json['jobIds']],
            )

        def __str__(self) -> str:
            props = ', '.join([
                f'run_id={self.run_id}',
                f'timestamp={self.timestamp}',
                f'job_ids={self.job_ids}',
            ])
            return f'ProjectRunInit[{props}]'

        def __repr__(self) -> str:
            return self.__str__()

        def __eq__(self, other: object) -> Any:
            if not isinstance(other, RealTimeS2C.ProjectRunInit):
                return NotImplemented
            return self.run_id == other.run_id \
                and self.timestamp == other.timestamp \
                and self.job_ids == other.job_ids


    class ProjectRunStart:

        def __init__(self, run_id: int) -> None:
            self.run_id = run_id

        def to_json(self) -> Dict[str,Any]:
            return {
                'runId': self.run_id,
            }

        @classmethod
        def from_json(cls, json: Dict[str,Any]) -> RealTimeS2C.ProjectRunStart:
            return cls(
                run_id=json['runId'],
            )

        def __str__(self) -> str:
            props = ', '.join([
                f'run_id={self.run_id}',
            ])
            return f'ProjectRunStart[{props}]'

        def __repr__(self) -> str:
            return self.__str__()

        def __eq__(self, other: object) -> Any:
            if not isinstance(other, RealTimeS2C.ProjectRunStart):
                return NotImplemented
            return self.run_id == other.run_id


    class JobStart:

        def __init__(self, run_id: int, job_id: str) -> None:
            self.run_id = run_id
            self.job_id = job_id

        def to_json(self) -> Dict[str,Any]:
            return {
                'runId': self.run_id,
                'jobId': self.job_id,
            }

        @classmethod
        def from_json(cls, json: Dict[str,Any]) -> RealTimeS2C.JobStart:
            return cls(
                run_id=json['runId'],
                job_id=json['jobId'],
            )

        def __str__(self) -> str:
            props = ', '.join([
                f'run_id={self.run_id}',
                f'job_id={self.job_id}',
            ])
            return f'JobStart[{props}]'

        def __repr__(self) -> str:
            return self.__str__()

        def __eq__(self, other: object) -> Any:
            if not isinstance(other, RealTimeS2C.JobStart):
                return NotImplemented
            return self.run_id == other.run_id \
                and self.job_id == other.job_id


    class JobUpdate:

        def __init__(self, job_id: str, job_string: str) -> None:
            self.job_id = job_id
            self.job_string = job_string

        def to_json(self) -> Dict[str,Any]:
            return {
                'jobId': self.job_id,
                'jobString': self.job_string,
            }

        @classmethod
        def from_json(cls, json: Dict[str,Any]) -> RealTimeS2C.JobUpdate:
            return cls(
                job_id=json['jobId'],
                job_string=json['jobString'],
            )

        def __str__(self) -> str:
            props = ', '.join([
                f'job_id={self.job_id}',
                f'job_string={self.job_string}',
            ])
            return f'JobUpdate[{props}]'

        def __repr__(self) -> str:
            return self.__str__()

        def __eq__(self, other: object) -> Any:
            if not isinstance(other, RealTimeS2C.JobUpdate):
                return NotImplemented
            return self.job_id == other.job_id \
                and self.job_string == other.job_string


    class JobFinish:

        def __init__(self, run_id: int, job_id: str, job_string: str, status: RunStatus) -> None:
            self.run_id = run_id
            self.job_id = job_id
            self.job_string = job_string
            self.status = status

        def to_json(self) -> Dict[str,Any]:
            return {
                'runId': self.run_id,
                'jobId': self.job_id,
                'jobString': self.job_string,
                'status': self.status.to_json(),
            }

        @classmethod
        def from_json(cls, json: Dict[str,Any]) -> RealTimeS2C.JobFinish:
            return cls(
                run_id=json['runId'],
                job_id=json['jobId'],
                job_string=json['jobString'],
                status=RunStatus.from_json(json['status']),
            )

        def __str__(self) -> str:
            props = ', '.join([
                f'run_id={self.run_id}',
                f'job_id={self.job_id}',
                f'job_string={self.job_string}',
                f'status={self.status}',
            ])
            return f'JobFinish[{props}]'

        def __repr__(self) -> str:
            return self.__str__()

        def __eq__(self, other: object) -> Any:
            if not isinstance(other, RealTimeS2C.JobFinish):
                return NotImplemented
            return self.run_id == other.run_id \
                and self.job_id == other.job_id \
                and self.job_string == other.job_string \
                and self.status == other.status


    class ProjectRunFinish:

        def __init__(self, run_id: int, status: RunStatus) -> None:
            self.run_id = run_id
            self.status = status

        def to_json(self) -> Dict[str,Any]:
            return {
                'runId': self.run_id,
                'status': self.status.to_json(),
            }

        @classmethod
        def from_json(cls, json: Dict[str,Any]) -> RealTimeS2C.ProjectRunFinish:
            return cls(
                run_id=json['runId'],
                status=RunStatus.from_json(json['status']),
            )

        def __str__(self) -> str:
            props = ', '.join([
                f'run_id={self.run_id}',
                f'status={self.status}',
            ])
            return f'ProjectRunFinish[{props}]'

        def __repr__(self) -> str:
            return self.__str__()

        def __eq__(self, other: object) -> Any:
            if not isinstance(other, RealTimeS2C.ProjectRunFinish):
                return NotImplemented
            return self.run_id == other.run_id \
                and self.status == other.status


    class ClusterJobSubmit:

        def __init__(self, run_id: int, job_id: str, cluster_job_id: str, cluster_job_name: Optional[str], array_size: Optional[int]) -> None:
            self.run_id = run_id
            self.job_id = job_id
            self.cluster_job_id = cluster_job_id
            self.cluster_job_name = cluster_job_name
            self.array_size = array_size

        def to_json(self) -> Dict[str,Any]:
            return {
                'runId': self.run_id,
                'jobId': self.job_id,
                'clusterJobId': self.cluster_job_id,
                'clusterJobName': self.cluster_job_name if self.cluster_job_name is not None else None,
                'arraySize': self.array_size if self.array_size is not None else None,
            }

        @classmethod
        def from_json(cls, json: Dict[str,Any]) -> RealTimeS2C.ClusterJobSubmit:
            return cls(
                run_id=json['runId'],
                job_id=json['jobId'],
                cluster_job_id=json['clusterJobId'],
                cluster_job_name=json['clusterJobName'] if 'clusterJobName' in json and json['clusterJobName'] is not None else None,
                array_size=json['arraySize'] if 'arraySize' in json and json['arraySize'] is not None else None,
            )

        def __str__(self) -> str:
            props = ', '.join([
                f'run_id={self.run_id}',
                f'job_id={self.job_id}',
                f'cluster_job_id={self.cluster_job_id}',
                f'cluster_job_name={self.cluster_job_name}',
                f'array_size={self.array_size}',
            ])
            return f'ClusterJobSubmit[{props}]'

        def __repr__(self) -> str:
            return self.__str__()

        def __eq__(self, other: object) -> Any:
            if not isinstance(other, RealTimeS2C.ClusterJobSubmit):
                return NotImplemented
            return self.run_id == other.run_id \
                and self.job_id == other.job_id \
                and self.cluster_job_id == other.cluster_job_id \
                and self.cluster_job_name == other.cluster_job_name \
                and self.array_size == other.array_size


    class ClusterJobStart:

        def __init__(self, run_id: int, job_id: str, cluster_job_id: str) -> None:
            self.run_id = run_id
            self.job_id = job_id
            self.cluster_job_id = cluster_job_id

        def to_json(self) -> Dict[str,Any]:
            return {
                'runId': self.run_id,
                'jobId': self.job_id,
                'clusterJobId': self.cluster_job_id,
            }

        @classmethod
        def from_json(cls, json: Dict[str,Any]) -> RealTimeS2C.ClusterJobStart:
            return cls(
                run_id=json['runId'],
                job_id=json['jobId'],
                cluster_job_id=json['clusterJobId'],
            )

        def __str__(self) -> str:
            props = ', '.join([
                f'run_id={self.run_id}',
                f'job_id={self.job_id}',
                f'cluster_job_id={self.cluster_job_id}',
            ])
            return f'ClusterJobStart[{props}]'

        def __repr__(self) -> str:
            return self.__str__()

        def __eq__(self, other: object) -> Any:
            if not isinstance(other, RealTimeS2C.ClusterJobStart):
                return NotImplemented
            return self.run_id == other.run_id \
                and self.job_id == other.job_id \
                and self.cluster_job_id == other.cluster_job_id


    class ClusterJobArrayStart:

        def __init__(self, run_id: int, job_id: str, cluster_job_id: str, array_index: int, num_started: int) -> None:
            self.run_id = run_id
            self.job_id = job_id
            self.cluster_job_id = cluster_job_id
            self.array_index = array_index
            self.num_started = num_started

        def to_json(self) -> Dict[str,Any]:
            return {
                'runId': self.run_id,
                'jobId': self.job_id,
                'clusterJobId': self.cluster_job_id,
                'arrayIndex': self.array_index,
                'numStarted': self.num_started,
            }

        @classmethod
        def from_json(cls, json: Dict[str,Any]) -> RealTimeS2C.ClusterJobArrayStart:
            return cls(
                run_id=json['runId'],
                job_id=json['jobId'],
                cluster_job_id=json['clusterJobId'],
                array_index=json['arrayIndex'],
                num_started=json['numStarted'],
            )

        def __str__(self) -> str:
            props = ', '.join([
                f'run_id={self.run_id}',
                f'job_id={self.job_id}',
                f'cluster_job_id={self.cluster_job_id}',
                f'array_index={self.array_index}',
                f'num_started={self.num_started}',
            ])
            return f'ClusterJobArrayStart[{props}]'

        def __repr__(self) -> str:
            return self.__str__()

        def __eq__(self, other: object) -> Any:
            if not isinstance(other, RealTimeS2C.ClusterJobArrayStart):
                return NotImplemented
            return self.run_id == other.run_id \
                and self.job_id == other.job_id \
                and self.cluster_job_id == other.cluster_job_id \
                and self.array_index == other.array_index \
                and self.num_started == other.num_started


    class ClusterJobArrayEnd:

        def __init__(self, run_id: int, job_id: str, cluster_job_id: str, array_index: int, num_ended: int, num_canceled: int, num_failed: int) -> None:
            self.run_id = run_id
            self.job_id = job_id
            self.cluster_job_id = cluster_job_id
            self.array_index = array_index
            self.num_ended = num_ended
            self.num_canceled = num_canceled
            self.num_failed = num_failed

        def to_json(self) -> Dict[str,Any]:
            return {
                'runId': self.run_id,
                'jobId': self.job_id,
                'clusterJobId': self.cluster_job_id,
                'arrayIndex': self.array_index,
                'numEnded': self.num_ended,
                'numCanceled': self.num_canceled,
                'numFailed': self.num_failed,
            }

        @classmethod
        def from_json(cls, json: Dict[str,Any]) -> RealTimeS2C.ClusterJobArrayEnd:
            return cls(
                run_id=json['runId'],
                job_id=json['jobId'],
                cluster_job_id=json['clusterJobId'],
                array_index=json['arrayIndex'],
                num_ended=json['numEnded'],
                num_canceled=json['numCanceled'],
                num_failed=json['numFailed'],
            )

        def __str__(self) -> str:
            props = ', '.join([
                f'run_id={self.run_id}',
                f'job_id={self.job_id}',
                f'cluster_job_id={self.cluster_job_id}',
                f'array_index={self.array_index}',
                f'num_ended={self.num_ended}',
                f'num_canceled={self.num_canceled}',
                f'num_failed={self.num_failed}',
            ])
            return f'ClusterJobArrayEnd[{props}]'

        def __repr__(self) -> str:
            return self.__str__()

        def __eq__(self, other: object) -> Any:
            if not isinstance(other, RealTimeS2C.ClusterJobArrayEnd):
                return NotImplemented
            return self.run_id == other.run_id \
                and self.job_id == other.job_id \
                and self.cluster_job_id == other.cluster_job_id \
                and self.array_index == other.array_index \
                and self.num_ended == other.num_ended \
                and self.num_canceled == other.num_canceled \
                and self.num_failed == other.num_failed


    class ClusterJobEnd:

        def __init__(self, run_id: int, job_id: str, cluster_job_id: str, result_type: ClusterJobResultType) -> None:
            self.run_id = run_id
            self.job_id = job_id
            self.cluster_job_id = cluster_job_id
            self.result_type = result_type

        def to_json(self) -> Dict[str,Any]:
            return {
                'runId': self.run_id,
                'jobId': self.job_id,
                'clusterJobId': self.cluster_job_id,
                'resultType': self.result_type.to_json(),
            }

        @classmethod
        def from_json(cls, json: Dict[str,Any]) -> RealTimeS2C.ClusterJobEnd:
            return cls(
                run_id=json['runId'],
                job_id=json['jobId'],
                cluster_job_id=json['clusterJobId'],
                result_type=ClusterJobResultType.from_json(json['resultType']),
            )

        def __str__(self) -> str:
            props = ', '.join([
                f'run_id={self.run_id}',
                f'job_id={self.job_id}',
                f'cluster_job_id={self.cluster_job_id}',
                f'result_type={self.result_type}',
            ])
            return f'ClusterJobEnd[{props}]'

        def __repr__(self) -> str:
            return self.__str__()

        def __eq__(self, other: object) -> Any:
            if not isinstance(other, RealTimeS2C.ClusterJobEnd):
                return NotImplemented
            return self.run_id == other.run_id \
                and self.job_id == other.job_id \
                and self.cluster_job_id == other.cluster_job_id \
                and self.result_type == other.result_type


    class SessionRunningJob:

        def __init__(self, job_id: str, name: str, size: int, status: RunStatus) -> None:
            self.job_id = job_id
            self.name = name
            self.size = size
            self.status = status

        def to_json(self) -> Dict[str,Any]:
            return {
                'jobId': self.job_id,
                'name': self.name,
                'size': self.size,
                'status': self.status.to_json(),
            }

        @classmethod
        def from_json(cls, json: Dict[str,Any]) -> RealTimeS2C.SessionRunningJob:
            return cls(
                job_id=json['jobId'],
                name=json['name'],
                size=json['size'],
                status=RunStatus.from_json(json['status']),
            )

        def __str__(self) -> str:
            props = ', '.join([
                f'job_id={self.job_id}',
                f'name={self.name}',
                f'size={self.size}',
                f'status={self.status}',
            ])
            return f'SessionRunningJob[{props}]'

        def __repr__(self) -> str:
            return self.__str__()

        def __eq__(self, other: object) -> Any:
            if not isinstance(other, RealTimeS2C.SessionRunningJob):
                return NotImplemented
            return self.job_id == other.job_id \
                and self.name == other.name \
                and self.size == other.size \
                and self.status == other.status


    class SessionFilesystem:

        def __init__(self, used: float, bytes_available: int, path: str, type: str, bytes: int, bytes_used: int) -> None:
            self.used = used
            self.bytes_available = bytes_available
            self.path = path
            self.type = type
            self.bytes = bytes
            self.bytes_used = bytes_used

        def to_json(self) -> Dict[str,Any]:
            return {
                'used': self.used,
                'bytesAvailable': self.bytes_available,
                'path': self.path,
                'type': self.type,
                'bytes': self.bytes,
                'bytesUsed': self.bytes_used,
            }

        @classmethod
        def from_json(cls, json: Dict[str,Any]) -> RealTimeS2C.SessionFilesystem:
            return cls(
                used=json['used'],
                bytes_available=json['bytesAvailable'],
                path=json['path'],
                type=json['type'],
                bytes=json['bytes'],
                bytes_used=json['bytesUsed'],
            )

        def __str__(self) -> str:
            props = ', '.join([
                f'used={self.used}',
                f'bytes_available={self.bytes_available}',
                f'path={self.path}',
                f'type={self.type}',
                f'bytes={self.bytes}',
                f'bytes_used={self.bytes_used}',
            ])
            return f'SessionFilesystem[{props}]'

        def __repr__(self) -> str:
            return self.__str__()

        def __eq__(self, other: object) -> Any:
            if not isinstance(other, RealTimeS2C.SessionFilesystem):
                return NotImplemented
            return self.used == other.used \
                and self.bytes_available == other.bytes_available \
                and self.path == other.path \
                and self.type == other.type \
                and self.bytes == other.bytes \
                and self.bytes_used == other.bytes_used


    class SessionTransferInit:

        def __init__(self, files: List[RealTimeS2C.SessionTransferInit.FileInfo]) -> None:
            self.files = files

        def to_json(self) -> Dict[str,Any]:
            return {
                'files': [x.to_json() for x in self.files],
            }

        @classmethod
        def from_json(cls, json: Dict[str,Any]) -> RealTimeS2C.SessionTransferInit:
            return cls(
                files=[RealTimeS2C.SessionTransferInit.FileInfo.from_json(x) for x in json['files']],
            )

        def __str__(self) -> str:
            props = ', '.join([
                f'files={self.files}',
            ])
            return f'SessionTransferInit[{props}]'

        def __repr__(self) -> str:
            return self.__str__()

        def __eq__(self, other: object) -> Any:
            if not isinstance(other, RealTimeS2C.SessionTransferInit):
                return NotImplemented
            return self.files == other.files


        class FileInfo:

            def __init__(self, filename: str, bytes_total: int, bytes_transfered: int) -> None:
                self.filename = filename
                self.bytes_total = bytes_total
                self.bytes_transfered = bytes_transfered

            def to_json(self) -> Dict[str,Any]:
                return {
                    'filename': self.filename,
                    'bytesTotal': self.bytes_total,
                    'bytesTransfered': self.bytes_transfered,
                }

            @classmethod
            def from_json(cls, json: Dict[str,Any]) -> RealTimeS2C.SessionTransferInit.FileInfo:
                return cls(
                    filename=json['filename'],
                    bytes_total=json['bytesTotal'],
                    bytes_transfered=json['bytesTransfered'],
                )

            def __str__(self) -> str:
                props = ', '.join([
                    f'filename={self.filename}',
                    f'bytes_total={self.bytes_total}',
                    f'bytes_transfered={self.bytes_transfered}',
                ])
                return f'FileInfo[{props}]'

            def __repr__(self) -> str:
                return self.__str__()

            def __eq__(self, other: object) -> Any:
                if not isinstance(other, RealTimeS2C.SessionTransferInit.FileInfo):
                    return NotImplemented
                return self.filename == other.filename \
                    and self.bytes_total == other.bytes_total \
                    and self.bytes_transfered == other.bytes_transfered


class Block:

    def __init__(self, block_id: str, name: str, description: str, group_ids: List[str]) -> None:
        self.block_id = block_id
        self.name = name
        self.description = description
        self.group_ids = group_ids

    def to_json(self) -> Dict[str,Any]:
        return {
            'blockId': self.block_id,
            'name': self.name,
            'description': self.description,
            'groupIds': [x for x in self.group_ids],
        }

    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> Block:
        return cls(
            block_id=json['blockId'],
            name=json['name'],
            description=json['description'],
            group_ids=[x for x in json['groupIds']],
        )

    def __str__(self) -> str:
        props = ', '.join([
            f'block_id={self.block_id}',
            f'name={self.name}',
            f'description={self.description}',
            f'group_ids={self.group_ids}',
        ])
        return f'Block[{props}]'

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> Any:
        if not isinstance(other, Block):
            return NotImplemented
        return self.block_id == other.block_id \
            and self.name == other.name \
            and self.description == other.description \
            and self.group_ids == other.group_ids


class ImagesScale:

    def __init__(self, particle_radius_unbinned: float, pixel_a: float, particle_radius_a: float) -> None:
        self.particle_radius_unbinned = particle_radius_unbinned
        self.pixel_a = pixel_a
        self.particle_radius_a = particle_radius_a

    def to_json(self) -> Dict[str,Any]:
        return {
            'particleRadiusUnbinned': self.particle_radius_unbinned,
            'pixelA': self.pixel_a,
            'particleRadiusA': self.particle_radius_a,
        }

    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> ImagesScale:
        return cls(
            particle_radius_unbinned=json['particleRadiusUnbinned'],
            pixel_a=json['pixelA'],
            particle_radius_a=json['particleRadiusA'],
        )

    def __str__(self) -> str:
        props = ', '.join([
            f'particle_radius_unbinned={self.particle_radius_unbinned}',
            f'pixel_a={self.pixel_a}',
            f'particle_radius_a={self.particle_radius_a}',
        ])
        return f'ImagesScale[{props}]'

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> Any:
        if not isinstance(other, ImagesScale):
            return NotImplemented
        return self.particle_radius_unbinned == other.particle_radius_unbinned \
            and self.pixel_a == other.pixel_a \
            and self.particle_radius_a == other.particle_radius_a


class TomoVirMethod:

    TopazEval: TomoVirMethod
    TopazTrain: TomoVirMethod
    PYPEval: TomoVirMethod
    PYPTrain: TomoVirMethod
    Manual: TomoVirMethod
    Auto: TomoVirMethod
    NoneVal: TomoVirMethod

    def __init__(self, name: str) -> None:
        self.name = name

    def to_json(self) -> str:
        return self.name

    @classmethod
    def from_json(cls, name: str) -> TomoVirMethod:
        if name == 'TopazEval':
            return TomoVirMethod.TopazEval
        elif name == 'TopazTrain':
            return TomoVirMethod.TopazTrain
        elif name == 'PYPEval':
            return TomoVirMethod.PYPEval
        elif name == 'PYPTrain':
            return TomoVirMethod.PYPTrain
        elif name == 'Manual':
            return TomoVirMethod.Manual
        elif name == 'Auto':
            return TomoVirMethod.Auto
        elif name == 'None':
            return TomoVirMethod.NoneVal
        else:
            return cls(name)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()

    def __len__(self) -> int:
        return 7

    def __iter__(self) -> Iterator[TomoVirMethod]:
        return [TomoVirMethod.TopazEval, TomoVirMethod.TopazTrain, TomoVirMethod.PYPEval, TomoVirMethod.PYPTrain, TomoVirMethod.Manual, TomoVirMethod.Auto, TomoVirMethod.NoneVal].__iter__()

    def __eq__(self, other: object) -> Any:
        if not isinstance(other, TomoVirMethod):
            return NotImplemented
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

TomoVirMethod.TopazEval = TomoVirMethod('TopazEval')
TomoVirMethod.TopazTrain = TomoVirMethod('TopazTrain')
TomoVirMethod.PYPEval = TomoVirMethod('PYPEval')
TomoVirMethod.PYPTrain = TomoVirMethod('PYPTrain')
TomoVirMethod.Manual = TomoVirMethod('Manual')
TomoVirMethod.Auto = TomoVirMethod('Auto')
TomoVirMethod.NoneVal = TomoVirMethod('None')


class ReconstructionData:

    def __init__(self, id: str, timestamp: int, class_num: int, iteration: int) -> None:
        self.id = id
        self.timestamp = timestamp
        self.class_num = class_num
        self.iteration = iteration

    def to_json(self) -> Dict[str,Any]:
        return {
            'id': self.id,
            'timestamp': self.timestamp,
            'classNum': self.class_num,
            'iteration': self.iteration,
        }

    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> ReconstructionData:
        return cls(
            id=json['id'],
            timestamp=json['timestamp'],
            class_num=json['classNum'],
            iteration=json['iteration'],
        )

    def __str__(self) -> str:
        props = ', '.join([
            f'id={self.id}',
            f'timestamp={self.timestamp}',
            f'class_num={self.class_num}',
            f'iteration={self.iteration}',
        ])
        return f'ReconstructionData[{props}]'

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> Any:
        if not isinstance(other, ReconstructionData):
            return NotImplemented
        return self.id == other.id \
            and self.timestamp == other.timestamp \
            and self.class_num == other.class_num \
            and self.iteration == other.iteration


class RefinementData:

    def __init__(self, id: str, job_id: str, data_id: str, iteration: int, timestamp: int) -> None:
        self.id = id
        self.job_id = job_id
        self.data_id = data_id
        self.iteration = iteration
        self.timestamp = timestamp

    def to_json(self) -> Dict[str,Any]:
        return {
            'id': self.id,
            'jobId': self.job_id,
            'dataId': self.data_id,
            'iteration': self.iteration,
            'timestamp': self.timestamp,
        }

    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> RefinementData:
        return cls(
            id=json['id'],
            job_id=json['jobId'],
            data_id=json['dataId'],
            iteration=json['iteration'],
            timestamp=json['timestamp'],
        )

    def __str__(self) -> str:
        props = ', '.join([
            f'id={self.id}',
            f'job_id={self.job_id}',
            f'data_id={self.data_id}',
            f'iteration={self.iteration}',
            f'timestamp={self.timestamp}',
        ])
        return f'RefinementData[{props}]'

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RefinementData):
            return NotImplemented
        return self.id == other.id \
            and self.job_id == other.job_id \
            and self.data_id == other.data_id \
            and self.iteration == other.iteration \
            and self.timestamp == other.timestamp


class RefinementBundleData:

    def __init__(self, id: str, job_id: str, refinement_bundle_id: str, iteration: int, timestamp: int) -> None:
        self.id = id
        self.job_id = job_id
        self.refinement_bundle_id = refinement_bundle_id
        self.iteration = iteration
        self.timestamp = timestamp

    def to_json(self) -> Dict[str,Any]:
        return {
            'id': self.id,
            'jobId': self.job_id,
            'refinementBundleId': self.refinement_bundle_id,
            'iteration': self.iteration,
            'timestamp': self.timestamp,
        }

    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> RefinementBundleData:
        return cls(
            id=json['id'],
            job_id=json['jobId'],
            refinement_bundle_id=json['refinementBundleId'],
            iteration=json['iteration'],
            timestamp=json['timestamp'],
        )

    def __str__(self) -> str:
        props = ', '.join([
            f'id={self.id}',
            f'job_id={self.job_id}',
            f'refinement_bundle_id={self.refinement_bundle_id}',
            f'iteration={self.iteration}',
            f'timestamp={self.timestamp}',
        ])
        return f'RefinementBundleData[{props}]'

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RefinementBundleData):
            return NotImplemented
        return self.id == other.id \
            and self.job_id == other.job_id \
            and self.refinement_bundle_id == other.refinement_bundle_id \
            and self.iteration == other.iteration \
            and self.timestamp == other.timestamp


class PypStats:

    def __init__(self, scope_voltage: Optional[float], scope_pixel: Optional[float], scope_dose_rate: Optional[float], particle_radius: Optional[float]) -> None:
        self.scope_voltage = scope_voltage
        self.scope_pixel = scope_pixel
        self.scope_dose_rate = scope_dose_rate
        self.particle_radius = particle_radius

    def to_json(self) -> Dict[str,Any]:
        return {
            'scopeVoltage': self.scope_voltage if self.scope_voltage is not None else None,
            'scopePixel': self.scope_pixel if self.scope_pixel is not None else None,
            'scopeDoseRate': self.scope_dose_rate if self.scope_dose_rate is not None else None,
            'particleRadius': self.particle_radius if self.particle_radius is not None else None,
        }

    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> PypStats:
        return cls(
            scope_voltage=json['scopeVoltage'] if 'scopeVoltage' in json and json['scopeVoltage'] is not None else None,
            scope_pixel=json['scopePixel'] if 'scopePixel' in json and json['scopePixel'] is not None else None,
            scope_dose_rate=json['scopeDoseRate'] if 'scopeDoseRate' in json and json['scopeDoseRate'] is not None else None,
            particle_radius=json['particleRadius'] if 'particleRadius' in json and json['particleRadius'] is not None else None,
        )

    def __str__(self) -> str:
        props = ', '.join([
            f'scope_voltage={self.scope_voltage}',
            f'scope_pixel={self.scope_pixel}',
            f'scope_dose_rate={self.scope_dose_rate}',
            f'particle_radius={self.particle_radius}',
        ])
        return f'PypStats[{props}]'

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> Any:
        if not isinstance(other, PypStats):
            return NotImplemented
        return self.scope_voltage == other.scope_voltage \
            and self.scope_pixel == other.scope_pixel \
            and self.scope_dose_rate == other.scope_dose_rate \
            and self.particle_radius == other.particle_radius


class ProjectPermission:

    Write: ProjectPermission
    Read: ProjectPermission

    def __init__(self, name: str) -> None:
        self.name = name

    def to_json(self) -> str:
        return self.name

    @classmethod
    def from_json(cls, name: str) -> ProjectPermission:
        if name == 'Write':
            return ProjectPermission.Write
        elif name == 'Read':
            return ProjectPermission.Read
        else:
            return cls(name)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()

    def __len__(self) -> int:
        return 2

    def __iter__(self) -> Iterator[ProjectPermission]:
        return [ProjectPermission.Write, ProjectPermission.Read].__iter__()

    def __eq__(self, other: object) -> Any:
        if not isinstance(other, ProjectPermission):
            return NotImplemented
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

ProjectPermission.Write = ProjectPermission('Write')
ProjectPermission.Read = ProjectPermission('Read')


class UserData:

    def __init__(self, id: str, name: Optional[str]) -> None:
        self.id = id
        self.name = name

    def to_json(self) -> Dict[str,Any]:
        return {
            'id': self.id,
            'name': self.name if self.name is not None else None,
        }

    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> UserData:
        return cls(
            id=json['id'],
            name=json['name'] if 'name' in json and json['name'] is not None else None,
        )

    def __str__(self) -> str:
        props = ', '.join([
            f'id={self.id}',
            f'name={self.name}',
        ])
        return f'UserData[{props}]'

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> Any:
        if not isinstance(other, UserData):
            return NotImplemented
        return self.id == other.id \
            and self.name == other.name


class ProjectRunData:

    def __init__(self, run_id: int, timestamp: int, status: RunStatus, jobs: List[JobRunData]) -> None:
        self.run_id = run_id
        self.timestamp = timestamp
        self.status = status
        self.jobs = jobs

    def to_json(self) -> Dict[str,Any]:
        return {
            'runId': self.run_id,
            'timestamp': self.timestamp,
            'status': self.status.to_json(),
            'jobs': [x.to_json() for x in self.jobs],
        }

    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> ProjectRunData:
        return cls(
            run_id=json['runId'],
            timestamp=json['timestamp'],
            status=RunStatus.from_json(json['status']),
            jobs=[JobRunData.from_json(x) for x in json['jobs']],
        )

    def __str__(self) -> str:
        props = ', '.join([
            f'run_id={self.run_id}',
            f'timestamp={self.timestamp}',
            f'status={self.status}',
            f'jobs={self.jobs}',
        ])
        return f'ProjectRunData[{props}]'

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> Any:
        if not isinstance(other, ProjectRunData):
            return NotImplemented
        return self.run_id == other.run_id \
            and self.timestamp == other.timestamp \
            and self.status == other.status \
            and self.jobs == other.jobs


class ClusterJobResultType:

    Canceled: ClusterJobResultType
    Failure: ClusterJobResultType
    Success: ClusterJobResultType

    def __init__(self, name: str) -> None:
        self.name = name

    def to_json(self) -> str:
        return self.name

    @classmethod
    def from_json(cls, name: str) -> ClusterJobResultType:
        if name == 'Canceled':
            return ClusterJobResultType.Canceled
        elif name == 'Failure':
            return ClusterJobResultType.Failure
        elif name == 'Success':
            return ClusterJobResultType.Success
        else:
            return cls(name)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()

    def __len__(self) -> int:
        return 3

    def __iter__(self) -> Iterator[ClusterJobResultType]:
        return [ClusterJobResultType.Canceled, ClusterJobResultType.Failure, ClusterJobResultType.Success].__iter__()

    def __eq__(self, other: object) -> Any:
        if not isinstance(other, ClusterJobResultType):
            return NotImplemented
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

ClusterJobResultType.Canceled = ClusterJobResultType('Canceled')
ClusterJobResultType.Failure = ClusterJobResultType('Failure')
ClusterJobResultType.Success = ClusterJobResultType('Success')


class RunStatus:

    Canceled: RunStatus
    Failed: RunStatus
    Succeeded: RunStatus
    Running: RunStatus
    Waiting: RunStatus

    def __init__(self, name: str) -> None:
        self.name = name

    def to_json(self) -> str:
        return self.name

    @classmethod
    def from_json(cls, name: str) -> RunStatus:
        if name == 'Canceled':
            return RunStatus.Canceled
        elif name == 'Failed':
            return RunStatus.Failed
        elif name == 'Succeeded':
            return RunStatus.Succeeded
        elif name == 'Running':
            return RunStatus.Running
        elif name == 'Waiting':
            return RunStatus.Waiting
        else:
            return cls(name)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()

    def __len__(self) -> int:
        return 5

    def __iter__(self) -> Iterator[RunStatus]:
        return [RunStatus.Canceled, RunStatus.Failed, RunStatus.Succeeded, RunStatus.Running, RunStatus.Waiting].__iter__()

    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RunStatus):
            return NotImplemented
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

RunStatus.Canceled = RunStatus('Canceled')
RunStatus.Failed = RunStatus('Failed')
RunStatus.Succeeded = RunStatus('Succeeded')
RunStatus.Running = RunStatus('Running')
RunStatus.Waiting = RunStatus('Waiting')


class StreamLogMsg:

    def __init__(self, timestamp: int, level: int, path: str, line: int, msg: str) -> None:
        self.timestamp = timestamp
        self.level = level
        self.path = path
        self.line = line
        self.msg = msg

    def to_json(self) -> Dict[str,Any]:
        return {
            'timestamp': self.timestamp,
            'level': self.level,
            'path': self.path,
            'line': self.line,
            'msg': self.msg,
        }

    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> StreamLogMsg:
        return cls(
            timestamp=json['timestamp'],
            level=json['level'],
            path=json['path'],
            line=json['line'],
            msg=json['msg'],
        )

    def __str__(self) -> str:
        props = ', '.join([
            f'timestamp={self.timestamp}',
            f'level={self.level}',
            f'path={self.path}',
            f'line={self.line}',
            f'msg={self.msg}',
        ])
        return f'StreamLogMsg[{props}]'

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> Any:
        if not isinstance(other, StreamLogMsg):
            return NotImplemented
        return self.timestamp == other.timestamp \
            and self.level == other.level \
            and self.path == other.path \
            and self.line == other.line \
            and self.msg == other.msg


class SessionDaemon:

    Fypd: SessionDaemon
    Pypd: SessionDaemon
    Streampyp: SessionDaemon

    def __init__(self, name: str) -> None:
        self.name = name

    def to_json(self) -> str:
        return self.name

    @classmethod
    def from_json(cls, name: str) -> SessionDaemon:
        if name == 'Fypd':
            return SessionDaemon.Fypd
        elif name == 'Pypd':
            return SessionDaemon.Pypd
        elif name == 'Streampyp':
            return SessionDaemon.Streampyp
        else:
            return cls(name)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()

    def __len__(self) -> int:
        return 3

    def __iter__(self) -> Iterator[SessionDaemon]:
        return [SessionDaemon.Fypd, SessionDaemon.Pypd, SessionDaemon.Streampyp].__iter__()

    def __eq__(self, other: object) -> Any:
        if not isinstance(other, SessionDaemon):
            return NotImplemented
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

SessionDaemon.Fypd = SessionDaemon('Fypd')
SessionDaemon.Pypd = SessionDaemon('Pypd')
SessionDaemon.Streampyp = SessionDaemon('Streampyp')


class SessionExportData:

    def __init__(self, session_id: str, export_id: str, request: str, created: int, cluster_job_id: Optional[str], result: Optional[str]) -> None:
        self.session_id = session_id
        self.export_id = export_id
        self.request = request
        self.created = created
        self.cluster_job_id = cluster_job_id
        self.result = result

    def to_json(self) -> Dict[str,Any]:
        return {
            'sessionId': self.session_id,
            'exportId': self.export_id,
            'request': self.request,
            'created': self.created,
            'clusterJobId': self.cluster_job_id if self.cluster_job_id is not None else None,
            'result': self.result if self.result is not None else None,
        }

    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> SessionExportData:
        return cls(
            session_id=json['sessionId'],
            export_id=json['exportId'],
            request=json['request'],
            created=json['created'],
            cluster_job_id=json['clusterJobId'] if 'clusterJobId' in json and json['clusterJobId'] is not None else None,
            result=json['result'] if 'result' in json and json['result'] is not None else None,
        )

    def __str__(self) -> str:
        props = ', '.join([
            f'session_id={self.session_id}',
            f'export_id={self.export_id}',
            f'request={self.request}',
            f'created={self.created}',
            f'cluster_job_id={self.cluster_job_id}',
            f'result={self.result}',
        ])
        return f'SessionExportData[{props}]'

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> Any:
        if not isinstance(other, SessionExportData):
            return NotImplemented
        return self.session_id == other.session_id \
            and self.export_id == other.export_id \
            and self.request == other.request \
            and self.created == other.created \
            and self.cluster_job_id == other.cluster_job_id \
            and self.result == other.result


class MicrographMetadata:

    def __init__(self, id: str, timestamp: int, ccc: float, cccc: float, defocus1: float, defocus2: float, angle_astig: float, average_motion: float, num_particles: int, source_dims: Optional[ImageDims]) -> None:
        self.id = id
        self.timestamp = timestamp
        self.ccc = ccc
        self.cccc = cccc
        self.defocus1 = defocus1
        self.defocus2 = defocus2
        self.angle_astig = angle_astig
        self.average_motion = average_motion
        self.num_particles = num_particles
        self.source_dims = source_dims

    def to_json(self) -> Dict[str,Any]:
        return {
            'id': self.id,
            'timestamp': self.timestamp,
            'ccc': self.ccc,
            'cccc': self.cccc,
            'defocus1': self.defocus1,
            'defocus2': self.defocus2,
            'angleAstig': self.angle_astig,
            'averageMotion': self.average_motion,
            'numParticles': self.num_particles,
            'sourceDims': self.source_dims.to_json() if self.source_dims is not None else None,
        }

    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> MicrographMetadata:
        return cls(
            id=json['id'],
            timestamp=json['timestamp'],
            ccc=json['ccc'],
            cccc=json['cccc'],
            defocus1=json['defocus1'],
            defocus2=json['defocus2'],
            angle_astig=json['angleAstig'],
            average_motion=json['averageMotion'],
            num_particles=json['numParticles'],
            source_dims=ImageDims.from_json(json['sourceDims']) if 'sourceDims' in json and json['sourceDims'] is not None else None,
        )

    def __str__(self) -> str:
        props = ', '.join([
            f'id={self.id}',
            f'timestamp={self.timestamp}',
            f'ccc={self.ccc}',
            f'cccc={self.cccc}',
            f'defocus1={self.defocus1}',
            f'defocus2={self.defocus2}',
            f'angle_astig={self.angle_astig}',
            f'average_motion={self.average_motion}',
            f'num_particles={self.num_particles}',
            f'source_dims={self.source_dims}',
        ])
        return f'MicrographMetadata[{props}]'

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> Any:
        if not isinstance(other, MicrographMetadata):
            return NotImplemented
        return self.id == other.id \
            and self.timestamp == other.timestamp \
            and self.ccc == other.ccc \
            and self.cccc == other.cccc \
            and self.defocus1 == other.defocus1 \
            and self.defocus2 == other.defocus2 \
            and self.angle_astig == other.angle_astig \
            and self.average_motion == other.average_motion \
            and self.num_particles == other.num_particles \
            and self.source_dims == other.source_dims


class TwoDClassesData:

    def __init__(self, owner_id: str, two_dclasses_id: str, created: int) -> None:
        self.owner_id = owner_id
        self.two_dclasses_id = two_dclasses_id
        self.created = created

    def to_json(self) -> Dict[str,Any]:
        return {
            'ownerId': self.owner_id,
            'twoDClassesId': self.two_dclasses_id,
            'created': self.created,
        }

    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> TwoDClassesData:
        return cls(
            owner_id=json['ownerId'],
            two_dclasses_id=json['twoDClassesId'],
            created=json['created'],
        )

    def __str__(self) -> str:
        props = ', '.join([
            f'owner_id={self.owner_id}',
            f'two_dclasses_id={self.two_dclasses_id}',
            f'created={self.created}',
        ])
        return f'TwoDClassesData[{props}]'

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> Any:
        if not isinstance(other, TwoDClassesData):
            return NotImplemented
        return self.owner_id == other.owner_id \
            and self.two_dclasses_id == other.two_dclasses_id \
            and self.created == other.created


class TiltSeriesData:

    def __init__(self, id: str, timestamp: int, ccc: float, cccc: float, defocus1: float, defocus2: float, angle_astig: float, average_motion: float, num_particles: int, source_dims: Optional[ImageDims]) -> None:
        self.id = id
        self.timestamp = timestamp
        self.ccc = ccc
        self.cccc = cccc
        self.defocus1 = defocus1
        self.defocus2 = defocus2
        self.angle_astig = angle_astig
        self.average_motion = average_motion
        self.num_particles = num_particles
        self.source_dims = source_dims

    def to_json(self) -> Dict[str,Any]:
        return {
            'id': self.id,
            'timestamp': self.timestamp,
            'ccc': self.ccc,
            'cccc': self.cccc,
            'defocus1': self.defocus1,
            'defocus2': self.defocus2,
            'angleAstig': self.angle_astig,
            'averageMotion': self.average_motion,
            'numParticles': self.num_particles,
            'sourceDims': self.source_dims.to_json() if self.source_dims is not None else None,
        }

    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> TiltSeriesData:
        return cls(
            id=json['id'],
            timestamp=json['timestamp'],
            ccc=json['ccc'],
            cccc=json['cccc'],
            defocus1=json['defocus1'],
            defocus2=json['defocus2'],
            angle_astig=json['angleAstig'],
            average_motion=json['averageMotion'],
            num_particles=json['numParticles'],
            source_dims=ImageDims.from_json(json['sourceDims']) if 'sourceDims' in json and json['sourceDims'] is not None else None,
        )

    def __str__(self) -> str:
        props = ', '.join([
            f'id={self.id}',
            f'timestamp={self.timestamp}',
            f'ccc={self.ccc}',
            f'cccc={self.cccc}',
            f'defocus1={self.defocus1}',
            f'defocus2={self.defocus2}',
            f'angle_astig={self.angle_astig}',
            f'average_motion={self.average_motion}',
            f'num_particles={self.num_particles}',
            f'source_dims={self.source_dims}',
        ])
        return f'TiltSeriesData[{props}]'

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> Any:
        if not isinstance(other, TiltSeriesData):
            return NotImplemented
        return self.id == other.id \
            and self.timestamp == other.timestamp \
            and self.ccc == other.ccc \
            and self.cccc == other.cccc \
            and self.defocus1 == other.defocus1 \
            and self.defocus2 == other.defocus2 \
            and self.angle_astig == other.angle_astig \
            and self.average_motion == other.average_motion \
            and self.num_particles == other.num_particles \
            and self.source_dims == other.source_dims


class ImageDims:

    def __init__(self, num_slices: int, width: int, height: int, depth: int, binning_factor: int) -> None:
        self.num_slices = num_slices
        self.width = width
        self.height = height
        self.depth = depth
        self.binning_factor = binning_factor

    def to_json(self) -> Dict[str,Any]:
        return {
            'numSlices': self.num_slices,
            'width': self.width,
            'height': self.height,
            'depth': self.depth,
            'binningFactor': self.binning_factor,
        }

    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> ImageDims:
        return cls(
            num_slices=json['numSlices'],
            width=json['width'],
            height=json['height'],
            depth=json['depth'],
            binning_factor=json['binningFactor'],
        )

    def __str__(self) -> str:
        props = ', '.join([
            f'num_slices={self.num_slices}',
            f'width={self.width}',
            f'height={self.height}',
            f'depth={self.depth}',
            f'binning_factor={self.binning_factor}',
        ])
        return f'ImageDims[{props}]'

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> Any:
        if not isinstance(other, ImageDims):
            return NotImplemented
        return self.num_slices == other.num_slices \
            and self.width == other.width \
            and self.height == other.height \
            and self.depth == other.depth \
            and self.binning_factor == other.binning_factor


class JobRunData:

    def __init__(self, job_id: str, status: RunStatus, cluster_jobs: List[ClusterJobData]) -> None:
        self.job_id = job_id
        self.status = status
        self.cluster_jobs = cluster_jobs

    def to_json(self) -> Dict[str,Any]:
        return {
            'jobId': self.job_id,
            'status': self.status.to_json(),
            'clusterJobs': [x.to_json() for x in self.cluster_jobs],
        }

    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> JobRunData:
        return cls(
            job_id=json['jobId'],
            status=RunStatus.from_json(json['status']),
            cluster_jobs=[ClusterJobData.from_json(x) for x in json['clusterJobs']],
        )

    def __str__(self) -> str:
        props = ', '.join([
            f'job_id={self.job_id}',
            f'status={self.status}',
            f'cluster_jobs={self.cluster_jobs}',
        ])
        return f'JobRunData[{props}]'

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> Any:
        if not isinstance(other, JobRunData):
            return NotImplemented
        return self.job_id == other.job_id \
            and self.status == other.status \
            and self.cluster_jobs == other.cluster_jobs


class ClusterJobData:

    def __init__(self, cluster_job_id: str, web_name: Optional[str], cluster_name: Optional[str], status: RunStatus, array_info: Optional[ClusterJobData.ArrayInfo]) -> None:
        self.cluster_job_id = cluster_job_id
        self.web_name = web_name
        self.cluster_name = cluster_name
        self.status = status
        self.array_info = array_info

    def to_json(self) -> Dict[str,Any]:
        return {
            'clusterJobId': self.cluster_job_id,
            'webName': self.web_name if self.web_name is not None else None,
            'clusterName': self.cluster_name if self.cluster_name is not None else None,
            'status': self.status.to_json(),
            'arrayInfo': self.array_info.to_json() if self.array_info is not None else None,
        }

    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> ClusterJobData:
        return cls(
            cluster_job_id=json['clusterJobId'],
            web_name=json['webName'] if 'webName' in json and json['webName'] is not None else None,
            cluster_name=json['clusterName'] if 'clusterName' in json and json['clusterName'] is not None else None,
            status=RunStatus.from_json(json['status']),
            array_info=ClusterJobData.ArrayInfo.from_json(json['arrayInfo']) if 'arrayInfo' in json and json['arrayInfo'] is not None else None,
        )

    def __str__(self) -> str:
        props = ', '.join([
            f'cluster_job_id={self.cluster_job_id}',
            f'web_name={self.web_name}',
            f'cluster_name={self.cluster_name}',
            f'status={self.status}',
            f'array_info={self.array_info}',
        ])
        return f'ClusterJobData[{props}]'

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> Any:
        if not isinstance(other, ClusterJobData):
            return NotImplemented
        return self.cluster_job_id == other.cluster_job_id \
            and self.web_name == other.web_name \
            and self.cluster_name == other.cluster_name \
            and self.status == other.status \
            and self.array_info == other.array_info


    class ArrayInfo:

        def __init__(self, size: int, started: int, ended: int, canceled: int, failed: int) -> None:
            self.size = size
            self.started = started
            self.ended = ended
            self.canceled = canceled
            self.failed = failed

        def to_json(self) -> Dict[str,Any]:
            return {
                'size': self.size,
                'started': self.started,
                'ended': self.ended,
                'canceled': self.canceled,
                'failed': self.failed,
            }

        @classmethod
        def from_json(cls, json: Dict[str,Any]) -> ClusterJobData.ArrayInfo:
            return cls(
                size=json['size'],
                started=json['started'],
                ended=json['ended'],
                canceled=json['canceled'],
                failed=json['failed'],
            )

        def __str__(self) -> str:
            props = ', '.join([
                f'size={self.size}',
                f'started={self.started}',
                f'ended={self.ended}',
                f'canceled={self.canceled}',
                f'failed={self.failed}',
            ])
            return f'ArrayInfo[{props}]'

        def __repr__(self) -> str:
            return self.__str__()

        def __eq__(self, other: object) -> Any:
            if not isinstance(other, ClusterJobData.ArrayInfo):
                return NotImplemented
            return self.size == other.size \
                and self.started == other.started \
                and self.ended == other.ended \
                and self.canceled == other.canceled \
                and self.failed == other.failed
