
from __future__ import annotations

from typing import Optional, List, Dict, Set, Any, Iterator, TYPE_CHECKING, Union, cast

import json
from websockets.legacy.client import WebSocketClientProtocol

from nextpyp.client.realtime import RealtimeService, RealtimeServiceConnection, RealtimeServiceUnexpectedMessage
if TYPE_CHECKING:
    from nextpyp.client import Client


class Services:
    """
    This class houses all of the different regular services that can be accessed by the NextPYP client,
    with each service exposed as a class attribute.
    
    Each regular service contains a group of functions that work in your app just like regular functions,
    except the function is executed on the NextPYP website instead of in your app.
    Calling a service function will cause your app to send a request to the NextPYP website
    and then wait until the response arrives.
    
    Regular services are different from realtime services. To learn more about realtime services,
    see :py:class:`.RealtimeServices`.
    
    Examples
    --------
    
    Call the ``list`` functon of the ``projects`` service:
    
    .. code-block:: python
    
        projects = client.services.projects.list('user_id')
    """
    
    def __init__(self, client: Client) -> None:
        self.apps: AppsService = AppsService(client)
        """
        The Apps service.
        See: :py:class:`.AppsService`
        """
        
        self.projects: ProjectsService = ProjectsService(client)
        """
        The Projects service.
        See: :py:class:`.ProjectsService`
        """
        




class AppsService:
    """
    Service providing functions specific to apps, mainly requesting and managing app tokens
    """
    
    def __init__(self, client: Client) -> None:
        self.client = client

    def version(self) -> str:
        """
        Returns the version number of NextPYP
        """
        path = '/kv/apps/version'
        response = self.client._call(path, [])
        if response is None:
            raise Exception(f'response expected from {path}, but none received')
        return cast(str, response)

    def request_token(self, user_id: str, app_name: str, app_permission_ids: List[str]) -> AppTokenRequestData:
        """
        Request an app token for your app on behalf of a specific user.
        Once requested, the user will need to approve the token request on the website. After approval, the user can copy the app token (it's a string) into your app.
        """
        path = '/kv/apps/requestToken'
        response = self.client._call(path, [user_id, app_name, app_permission_ids])
        if response is None:
            raise Exception(f'response expected from {path}, but none received')
        return AppTokenRequestData.from_json(response)


class ProjectsService:
    """
    Service for interacting with user projects
    """
    
    def __init__(self, client: Client) -> None:
        self.client = client

    def list(self, user_id: str) -> List[ProjectData]:
        """
        (no description yet)
        """
        path = '/kv/projects/list'
        response = self.client._call(path, [user_id])
        if response is None:
            raise Exception(f'response expected from {path}, but none received')
        return [ProjectData.from_json(x) for x in response]


class RealtimeServices:
    """
    All of the different realtime services that can be accessed by the NextPYP client
    
    Realtime services exchange messages with the NextPYP website, rather than perform function calls,
    like regular services. The message exchange format lets the client send a message to the website
    and then wait for any number of different responses which can all arrive different times.
    In effect, this kind of connection lets the client stream data back from the website as soon as it's ready.
    
    Realtime services use Python's asyncio system over a HTTP WebSocket connection to send and receive
    messages to/from the website. This technique results in a lower event latency
    than more traditional connection polling techniques, and can be more efficient with network resources as well.
    
    Realtime services are different from regular services. To learn more about regular services,
    see :py:class:`.Services`.
    
    Examples
    --------
    
    Call a realtime service:
    
    .. code-block:: python
    
        async with client.realtime_services.project as project:
        
            await project.send_listen_to_project(RealTimeC2SListenToProject(
                user_id='user_id',
                project_id='project_id'
            ))
            
            msg = await project.recv()
            if type(msg) is RealTimeS2CProjectStatus:
                print(f'project status: {msg}')
            else:
                print(f'received other msg: {msg}')
    
    """
    
    def __init__(self, client: Client) -> None:
        self.project: RealtimeService[ProjectRealtimeServiceConnection] = RealtimeService(client, '/ws/project', ProjectRealtimeServiceConnection)
        """
        (no description yet)
        
        .. rubric:: Client to Server messages
        
        * :py:class:`.RealTimeC2SListenToProject`
        
        .. rubric:: Server to Client messages
        
        * :py:class:`.RealTimeS2CProjectStatus`
        * :py:class:`.RealTimeS2CProjectRunInit`
        * :py:class:`.RealTimeS2CProjectRunStart`
        * :py:class:`.RealTimeS2CJobStart`
        * :py:class:`.RealTimeS2CJobUpdate`
        * :py:class:`.RealTimeS2CJobFinish`
        * :py:class:`.RealTimeS2CProjectRunFinish`
        * :py:class:`.RealTimeS2CClusterJobSubmit`
        * :py:class:`.RealTimeS2CClusterJobStart`
        * :py:class:`.RealTimeS2CClusterJobArrayStart`
        * :py:class:`.RealTimeS2CClusterJobArrayEnd`
        * :py:class:`.RealTimeS2CClusterJobEnd`
        """


class ProjectRealtimeServiceConnection(RealtimeServiceConnection):
    
    def __init__(self, websocket: WebSocketClientProtocol) -> None:
        super(ProjectRealtimeServiceConnection, self).__init__(websocket)
    
    async def send_listen_to_project(self, msg: RealTimeC2SListenToProject) -> None:
        """
        Sends a RealTimeC2SListenToProject message
        """
        
        j = msg.to_json()
        j['type'] = RealTimeC2SListenToProject.TYPE_ID
        await self._send(j)
    
    async def recv(self) -> Union[RealTimeS2CProjectStatus, RealTimeS2CProjectRunInit, RealTimeS2CProjectRunStart, RealTimeS2CJobStart, RealTimeS2CJobUpdate, RealTimeS2CJobFinish, RealTimeS2CProjectRunFinish, RealTimeS2CClusterJobSubmit, RealTimeS2CClusterJobStart, RealTimeS2CClusterJobArrayStart, RealTimeS2CClusterJobArrayEnd, RealTimeS2CClusterJobEnd]:
        """
        Receives a message from the website. Could be any one of several different messages.
        
        Examples
        --------
        
        Receive a message from this realtime service:
        
        .. code-block:: python
        
            msg = await project.recv()
            if type(msg) is RealTimeS2CProjectStatus:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CProjectRunInit:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CProjectRunStart:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CJobStart:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CJobUpdate:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CJobFinish:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CProjectRunFinish:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CClusterJobSubmit:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CClusterJobStart:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CClusterJobArrayStart:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CClusterJobArrayEnd:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CClusterJobEnd:
                print(f'received message: {msg}')
            else:
                raise Exception(f'received unexpected msg: {msg}')
        """
        
        msg = await self._recv()
        type = msg.get('type')
        match type:
            case RealTimeS2CProjectStatus.TYPE_ID:
                return RealTimeS2CProjectStatus.from_json(msg)
            case RealTimeS2CProjectRunInit.TYPE_ID:
                return RealTimeS2CProjectRunInit.from_json(msg)
            case RealTimeS2CProjectRunStart.TYPE_ID:
                return RealTimeS2CProjectRunStart.from_json(msg)
            case RealTimeS2CJobStart.TYPE_ID:
                return RealTimeS2CJobStart.from_json(msg)
            case RealTimeS2CJobUpdate.TYPE_ID:
                return RealTimeS2CJobUpdate.from_json(msg)
            case RealTimeS2CJobFinish.TYPE_ID:
                return RealTimeS2CJobFinish.from_json(msg)
            case RealTimeS2CProjectRunFinish.TYPE_ID:
                return RealTimeS2CProjectRunFinish.from_json(msg)
            case RealTimeS2CClusterJobSubmit.TYPE_ID:
                return RealTimeS2CClusterJobSubmit.from_json(msg)
            case RealTimeS2CClusterJobStart.TYPE_ID:
                return RealTimeS2CClusterJobStart.from_json(msg)
            case RealTimeS2CClusterJobArrayStart.TYPE_ID:
                return RealTimeS2CClusterJobArrayStart.from_json(msg)
            case RealTimeS2CClusterJobArrayEnd.TYPE_ID:
                return RealTimeS2CClusterJobArrayEnd.from_json(msg)
            case RealTimeS2CClusterJobEnd.TYPE_ID:
                return RealTimeS2CClusterJobEnd.from_json(msg)
            case _:
                raise RealtimeServiceUnexpectedMessage(type)


class AppTokenRequestData:
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.AppTokenRequestData'
    
    def __init__(self, request_id: str, app_name: str, permissions: List[AppPermissionData]) -> None:
        """
        
        """
        self.request_id: str = request_id
        """
        (no description yet)
        """
        self.app_name: str = app_name
        """
        (no description yet)
        """
        self.permissions: List[AppPermissionData] = permissions
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'requestId': self.request_id,
            'appName': self.app_name,
            'permissions': [x.to_json() for x in self.permissions],
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> AppTokenRequestData:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            request_id=cast(str, json['requestId']),
            app_name=cast(str, json['appName']),
            permissions=[AppPermissionData.from_json(x) for x in json['permissions']],
        )
    
    def __str__(self) -> str:
        props = ', '.join([
            f'request_id={self.request_id}',
            f'app_name={self.app_name}',
            f'permissions={self.permissions}',
        ])
        return f'AppTokenRequestData[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, AppTokenRequestData):
            return NotImplemented
        return self.request_id == other.request_id \
            and self.app_name == other.app_name \
            and self.permissions == other.permissions


class ProjectData:
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.ProjectData'
    
    def __init__(self, owner: UserData, permissions: Set[ProjectPermission], project_id: str, project_number: Optional[int], project_name: str, created: int, images: List[str], path: str) -> None:
        """
        
        """
        self.owner: UserData = owner
        """
        (no description yet)
        """
        self.permissions: Set[ProjectPermission] = permissions
        """
        (no description yet)
        """
        self.project_id: str = project_id
        """
        (no description yet)
        """
        self.project_number: Optional[int] = project_number
        """
        (no description yet)
        """
        self.project_name: str = project_name
        """
        (no description yet)
        """
        self.created: int = created
        """
        (no description yet)
        """
        self.images: List[str] = images
        """
        urls of representative images for the project, small size
        """
        self.path: str = path
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
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
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            owner=UserData.from_json(json['owner']),
            permissions={ProjectPermission.from_json(x) for x in json['permissions']},
            project_id=cast(str, json['projectId']),
            project_number=cast(int, json['projectNumber']) if 'projectNumber' in json and json['projectNumber'] is not None else None,
            project_name=cast(str, json['projectName']),
            created=cast(int, json['created']),
            images=[cast(str, x) for x in json['images']],
            path=cast(str, json['path']),
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
    """
    client -
    >
     server (C2S) messages for real-time communication
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeC2S'
    
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> RealTimeC2S:
        """
        Creates a new class instance from JSON
        """
        
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


class RealTimeC2SListenToProject:
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeC2S.ListenToProject'
    
    def __init__(self, user_id: str, project_id: str) -> None:
        """
        
        """
        self.user_id: str = user_id
        """
        (no description yet)
        """
        self.project_id: str = project_id
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'userId': self.user_id,
            'projectId': self.project_id,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> RealTimeC2SListenToProject:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            user_id=cast(str, json['userId']),
            project_id=cast(str, json['projectId']),
        )
    
    def __str__(self) -> str:
        props = ', '.join([
            f'user_id={self.user_id}',
            f'project_id={self.project_id}',
        ])
        return f'RealTimeC2SListenToProject[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RealTimeC2SListenToProject):
            return NotImplemented
        return self.user_id == other.user_id \
            and self.project_id == other.project_id


class RealTimeS2C:
    """
    server -
    >
     client (S2C) messages for real-time communication
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C'
    
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> RealTimeS2C:
        """
        Creates a new class instance from JSON
        """
        
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


class RealTimeS2CError:
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.Error'
    
    def __init__(self, name: Optional[str], msg: Optional[str]) -> None:
        """
        
        """
        self.name: Optional[str] = name
        """
        (no description yet)
        """
        self.msg: Optional[str] = msg
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'name': self.name if self.name is not None else None,
            'msg': self.msg if self.msg is not None else None,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> RealTimeS2CError:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            name=cast(str, json['name']) if 'name' in json and json['name'] is not None else None,
            msg=cast(str, json['msg']) if 'msg' in json and json['msg'] is not None else None,
        )
    
    def __str__(self) -> str:
        props = ', '.join([
            f'name={self.name}',
            f'msg={self.msg}',
        ])
        return f'RealTimeS2CError[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RealTimeS2CError):
            return NotImplemented
        return self.name == other.name \
            and self.msg == other.msg


class RealTimeS2CProjectStatus:
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.ProjectStatus'
    
    def __init__(self, recent_runs: List[ProjectRunData], has_older_runs: bool, blocks: List[Block]) -> None:
        """
        
        """
        self.recent_runs: List[ProjectRunData] = recent_runs
        """
        (no description yet)
        """
        self.has_older_runs: bool = has_older_runs
        """
        (no description yet)
        """
        self.blocks: List[Block] = blocks
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'recentRuns': [x.to_json() for x in self.recent_runs],
            'hasOlderRuns': self.has_older_runs,
            'blocks': [x.to_json() for x in self.blocks],
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> RealTimeS2CProjectStatus:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            recent_runs=[ProjectRunData.from_json(x) for x in json['recentRuns']],
            has_older_runs=cast(bool, json['hasOlderRuns']),
            blocks=[Block.from_json(x) for x in json['blocks']],
        )
    
    def __str__(self) -> str:
        props = ', '.join([
            f'recent_runs={self.recent_runs}',
            f'has_older_runs={self.has_older_runs}',
            f'blocks={self.blocks}',
        ])
        return f'RealTimeS2CProjectStatus[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RealTimeS2CProjectStatus):
            return NotImplemented
        return self.recent_runs == other.recent_runs \
            and self.has_older_runs == other.has_older_runs \
            and self.blocks == other.blocks


class RealTimeS2CProjectRunInit:
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.ProjectRunInit'
    
    def __init__(self, run_id: int, timestamp: int, job_ids: List[str]) -> None:
        """
        
        """
        self.run_id: int = run_id
        """
        (no description yet)
        """
        self.timestamp: int = timestamp
        """
        (no description yet)
        """
        self.job_ids: List[str] = job_ids
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'runId': self.run_id,
            'timestamp': self.timestamp,
            'jobIds': [x for x in self.job_ids],
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> RealTimeS2CProjectRunInit:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            run_id=cast(int, json['runId']),
            timestamp=cast(int, json['timestamp']),
            job_ids=[cast(str, x) for x in json['jobIds']],
        )
    
    def __str__(self) -> str:
        props = ', '.join([
            f'run_id={self.run_id}',
            f'timestamp={self.timestamp}',
            f'job_ids={self.job_ids}',
        ])
        return f'RealTimeS2CProjectRunInit[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RealTimeS2CProjectRunInit):
            return NotImplemented
        return self.run_id == other.run_id \
            and self.timestamp == other.timestamp \
            and self.job_ids == other.job_ids


class RealTimeS2CProjectRunStart:
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.ProjectRunStart'
    
    def __init__(self, run_id: int) -> None:
        """
        
        """
        self.run_id: int = run_id
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'runId': self.run_id,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> RealTimeS2CProjectRunStart:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            run_id=cast(int, json['runId']),
        )
    
    def __str__(self) -> str:
        props = ', '.join([
            f'run_id={self.run_id}',
        ])
        return f'RealTimeS2CProjectRunStart[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RealTimeS2CProjectRunStart):
            return NotImplemented
        return self.run_id == other.run_id


class RealTimeS2CJobStart:
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.JobStart'
    
    def __init__(self, run_id: int, job_id: str) -> None:
        """
        
        """
        self.run_id: int = run_id
        """
        (no description yet)
        """
        self.job_id: str = job_id
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'runId': self.run_id,
            'jobId': self.job_id,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> RealTimeS2CJobStart:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            run_id=cast(int, json['runId']),
            job_id=cast(str, json['jobId']),
        )
    
    def __str__(self) -> str:
        props = ', '.join([
            f'run_id={self.run_id}',
            f'job_id={self.job_id}',
        ])
        return f'RealTimeS2CJobStart[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RealTimeS2CJobStart):
            return NotImplemented
        return self.run_id == other.run_id \
            and self.job_id == other.job_id


class RealTimeS2CJobUpdate:
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.JobUpdate'
    
    def __init__(self, job_id: str, job_string: str) -> None:
        """
        
        """
        self.job_id: str = job_id
        """
        (no description yet)
        """
        self.job_string: str = job_string
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'jobId': self.job_id,
            'jobString': self.job_string,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> RealTimeS2CJobUpdate:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            job_id=cast(str, json['jobId']),
            job_string=cast(str, json['jobString']),
        )
    
    def __str__(self) -> str:
        props = ', '.join([
            f'job_id={self.job_id}',
            f'job_string={self.job_string}',
        ])
        return f'RealTimeS2CJobUpdate[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RealTimeS2CJobUpdate):
            return NotImplemented
        return self.job_id == other.job_id \
            and self.job_string == other.job_string


class RealTimeS2CJobFinish:
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.JobFinish'
    
    def __init__(self, run_id: int, job_id: str, job_string: str, status: RunStatus) -> None:
        """
        
        """
        self.run_id: int = run_id
        """
        (no description yet)
        """
        self.job_id: str = job_id
        """
        (no description yet)
        """
        self.job_string: str = job_string
        """
        (no description yet)
        """
        self.status: RunStatus = status
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'runId': self.run_id,
            'jobId': self.job_id,
            'jobString': self.job_string,
            'status': self.status.to_json(),
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> RealTimeS2CJobFinish:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            run_id=cast(int, json['runId']),
            job_id=cast(str, json['jobId']),
            job_string=cast(str, json['jobString']),
            status=RunStatus.from_json(json['status']),
        )
    
    def __str__(self) -> str:
        props = ', '.join([
            f'run_id={self.run_id}',
            f'job_id={self.job_id}',
            f'job_string={self.job_string}',
            f'status={self.status}',
        ])
        return f'RealTimeS2CJobFinish[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RealTimeS2CJobFinish):
            return NotImplemented
        return self.run_id == other.run_id \
            and self.job_id == other.job_id \
            and self.job_string == other.job_string \
            and self.status == other.status


class RealTimeS2CProjectRunFinish:
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.ProjectRunFinish'
    
    def __init__(self, run_id: int, status: RunStatus) -> None:
        """
        
        """
        self.run_id: int = run_id
        """
        (no description yet)
        """
        self.status: RunStatus = status
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'runId': self.run_id,
            'status': self.status.to_json(),
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> RealTimeS2CProjectRunFinish:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            run_id=cast(int, json['runId']),
            status=RunStatus.from_json(json['status']),
        )
    
    def __str__(self) -> str:
        props = ', '.join([
            f'run_id={self.run_id}',
            f'status={self.status}',
        ])
        return f'RealTimeS2CProjectRunFinish[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RealTimeS2CProjectRunFinish):
            return NotImplemented
        return self.run_id == other.run_id \
            and self.status == other.status


class RealTimeS2CClusterJobSubmit:
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.ClusterJobSubmit'
    
    def __init__(self, run_id: int, job_id: str, cluster_job_id: str, cluster_job_name: Optional[str], array_size: Optional[int]) -> None:
        """
        
        """
        self.run_id: int = run_id
        """
        (no description yet)
        """
        self.job_id: str = job_id
        """
        (no description yet)
        """
        self.cluster_job_id: str = cluster_job_id
        """
        (no description yet)
        """
        self.cluster_job_name: Optional[str] = cluster_job_name
        """
        (no description yet)
        """
        self.array_size: Optional[int] = array_size
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'runId': self.run_id,
            'jobId': self.job_id,
            'clusterJobId': self.cluster_job_id,
            'clusterJobName': self.cluster_job_name if self.cluster_job_name is not None else None,
            'arraySize': self.array_size if self.array_size is not None else None,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> RealTimeS2CClusterJobSubmit:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            run_id=cast(int, json['runId']),
            job_id=cast(str, json['jobId']),
            cluster_job_id=cast(str, json['clusterJobId']),
            cluster_job_name=cast(str, json['clusterJobName']) if 'clusterJobName' in json and json['clusterJobName'] is not None else None,
            array_size=cast(int, json['arraySize']) if 'arraySize' in json and json['arraySize'] is not None else None,
        )
    
    def __str__(self) -> str:
        props = ', '.join([
            f'run_id={self.run_id}',
            f'job_id={self.job_id}',
            f'cluster_job_id={self.cluster_job_id}',
            f'cluster_job_name={self.cluster_job_name}',
            f'array_size={self.array_size}',
        ])
        return f'RealTimeS2CClusterJobSubmit[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RealTimeS2CClusterJobSubmit):
            return NotImplemented
        return self.run_id == other.run_id \
            and self.job_id == other.job_id \
            and self.cluster_job_id == other.cluster_job_id \
            and self.cluster_job_name == other.cluster_job_name \
            and self.array_size == other.array_size


class RealTimeS2CClusterJobStart:
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.ClusterJobStart'
    
    def __init__(self, run_id: int, job_id: str, cluster_job_id: str) -> None:
        """
        
        """
        self.run_id: int = run_id
        """
        (no description yet)
        """
        self.job_id: str = job_id
        """
        (no description yet)
        """
        self.cluster_job_id: str = cluster_job_id
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'runId': self.run_id,
            'jobId': self.job_id,
            'clusterJobId': self.cluster_job_id,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> RealTimeS2CClusterJobStart:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            run_id=cast(int, json['runId']),
            job_id=cast(str, json['jobId']),
            cluster_job_id=cast(str, json['clusterJobId']),
        )
    
    def __str__(self) -> str:
        props = ', '.join([
            f'run_id={self.run_id}',
            f'job_id={self.job_id}',
            f'cluster_job_id={self.cluster_job_id}',
        ])
        return f'RealTimeS2CClusterJobStart[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RealTimeS2CClusterJobStart):
            return NotImplemented
        return self.run_id == other.run_id \
            and self.job_id == other.job_id \
            and self.cluster_job_id == other.cluster_job_id


class RealTimeS2CClusterJobArrayStart:
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.ClusterJobArrayStart'
    
    def __init__(self, run_id: int, job_id: str, cluster_job_id: str, array_index: int, num_started: int) -> None:
        """
        
        """
        self.run_id: int = run_id
        """
        (no description yet)
        """
        self.job_id: str = job_id
        """
        (no description yet)
        """
        self.cluster_job_id: str = cluster_job_id
        """
        (no description yet)
        """
        self.array_index: int = array_index
        """
        (no description yet)
        """
        self.num_started: int = num_started
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'runId': self.run_id,
            'jobId': self.job_id,
            'clusterJobId': self.cluster_job_id,
            'arrayIndex': self.array_index,
            'numStarted': self.num_started,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> RealTimeS2CClusterJobArrayStart:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            run_id=cast(int, json['runId']),
            job_id=cast(str, json['jobId']),
            cluster_job_id=cast(str, json['clusterJobId']),
            array_index=cast(int, json['arrayIndex']),
            num_started=cast(int, json['numStarted']),
        )
    
    def __str__(self) -> str:
        props = ', '.join([
            f'run_id={self.run_id}',
            f'job_id={self.job_id}',
            f'cluster_job_id={self.cluster_job_id}',
            f'array_index={self.array_index}',
            f'num_started={self.num_started}',
        ])
        return f'RealTimeS2CClusterJobArrayStart[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RealTimeS2CClusterJobArrayStart):
            return NotImplemented
        return self.run_id == other.run_id \
            and self.job_id == other.job_id \
            and self.cluster_job_id == other.cluster_job_id \
            and self.array_index == other.array_index \
            and self.num_started == other.num_started


class RealTimeS2CClusterJobArrayEnd:
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.ClusterJobArrayEnd'
    
    def __init__(self, run_id: int, job_id: str, cluster_job_id: str, array_index: int, num_ended: int, num_canceled: int, num_failed: int) -> None:
        """
        
        """
        self.run_id: int = run_id
        """
        (no description yet)
        """
        self.job_id: str = job_id
        """
        (no description yet)
        """
        self.cluster_job_id: str = cluster_job_id
        """
        (no description yet)
        """
        self.array_index: int = array_index
        """
        (no description yet)
        """
        self.num_ended: int = num_ended
        """
        (no description yet)
        """
        self.num_canceled: int = num_canceled
        """
        (no description yet)
        """
        self.num_failed: int = num_failed
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
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
    def from_json(cls, json: Dict[str,Any]) -> RealTimeS2CClusterJobArrayEnd:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            run_id=cast(int, json['runId']),
            job_id=cast(str, json['jobId']),
            cluster_job_id=cast(str, json['clusterJobId']),
            array_index=cast(int, json['arrayIndex']),
            num_ended=cast(int, json['numEnded']),
            num_canceled=cast(int, json['numCanceled']),
            num_failed=cast(int, json['numFailed']),
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
        return f'RealTimeS2CClusterJobArrayEnd[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RealTimeS2CClusterJobArrayEnd):
            return NotImplemented
        return self.run_id == other.run_id \
            and self.job_id == other.job_id \
            and self.cluster_job_id == other.cluster_job_id \
            and self.array_index == other.array_index \
            and self.num_ended == other.num_ended \
            and self.num_canceled == other.num_canceled \
            and self.num_failed == other.num_failed


class RealTimeS2CClusterJobEnd:
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.ClusterJobEnd'
    
    def __init__(self, run_id: int, job_id: str, cluster_job_id: str, result_type: ClusterJobResultType) -> None:
        """
        
        """
        self.run_id: int = run_id
        """
        (no description yet)
        """
        self.job_id: str = job_id
        """
        (no description yet)
        """
        self.cluster_job_id: str = cluster_job_id
        """
        (no description yet)
        """
        self.result_type: ClusterJobResultType = result_type
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'runId': self.run_id,
            'jobId': self.job_id,
            'clusterJobId': self.cluster_job_id,
            'resultType': self.result_type.to_json(),
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> RealTimeS2CClusterJobEnd:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            run_id=cast(int, json['runId']),
            job_id=cast(str, json['jobId']),
            cluster_job_id=cast(str, json['clusterJobId']),
            result_type=ClusterJobResultType.from_json(json['resultType']),
        )
    
    def __str__(self) -> str:
        props = ', '.join([
            f'run_id={self.run_id}',
            f'job_id={self.job_id}',
            f'cluster_job_id={self.cluster_job_id}',
            f'result_type={self.result_type}',
        ])
        return f'RealTimeS2CClusterJobEnd[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RealTimeS2CClusterJobEnd):
            return NotImplemented
        return self.run_id == other.run_id \
            and self.job_id == other.job_id \
            and self.cluster_job_id == other.cluster_job_id \
            and self.result_type == other.result_type


class RealTimeS2CSessionRunningJob:
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionRunningJob'
    
    def __init__(self, job_id: str, name: str, size: int, status: RunStatus) -> None:
        """
        
        """
        self.job_id: str = job_id
        """
        (no description yet)
        """
        self.name: str = name
        """
        (no description yet)
        """
        self.size: int = size
        """
        (no description yet)
        """
        self.status: RunStatus = status
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'jobId': self.job_id,
            'name': self.name,
            'size': self.size,
            'status': self.status.to_json(),
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> RealTimeS2CSessionRunningJob:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            job_id=cast(str, json['jobId']),
            name=cast(str, json['name']),
            size=cast(int, json['size']),
            status=RunStatus.from_json(json['status']),
        )
    
    def __str__(self) -> str:
        props = ', '.join([
            f'job_id={self.job_id}',
            f'name={self.name}',
            f'size={self.size}',
            f'status={self.status}',
        ])
        return f'RealTimeS2CSessionRunningJob[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RealTimeS2CSessionRunningJob):
            return NotImplemented
        return self.job_id == other.job_id \
            and self.name == other.name \
            and self.size == other.size \
            and self.status == other.status


class RealTimeS2CSessionFilesystem:
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionFilesystem'
    
    def __init__(self, used: float, bytes_available: int, path: str, type: str, bytes: int, bytes_used: int) -> None:
        """
        
        """
        self.used: float = used
        """
        (no description yet)
        """
        self.bytes_available: int = bytes_available
        """
        (no description yet)
        """
        self.path: str = path
        """
        (no description yet)
        """
        self.type: str = type
        """
        (no description yet)
        """
        self.bytes: int = bytes
        """
        (no description yet)
        """
        self.bytes_used: int = bytes_used
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'used': self.used,
            'bytesAvailable': self.bytes_available,
            'path': self.path,
            'type': self.type,
            'bytes': self.bytes,
            'bytesUsed': self.bytes_used,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> RealTimeS2CSessionFilesystem:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            used=cast(float, json['used']),
            bytes_available=cast(int, json['bytesAvailable']),
            path=cast(str, json['path']),
            type=cast(str, json['type']),
            bytes=cast(int, json['bytes']),
            bytes_used=cast(int, json['bytesUsed']),
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
        return f'RealTimeS2CSessionFilesystem[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RealTimeS2CSessionFilesystem):
            return NotImplemented
        return self.used == other.used \
            and self.bytes_available == other.bytes_available \
            and self.path == other.path \
            and self.type == other.type \
            and self.bytes == other.bytes \
            and self.bytes_used == other.bytes_used


class RealTimeS2CSessionTransferInit:
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionTransferInit'
    
    def __init__(self, files: List[RealTimeS2CSessionTransferInitFileInfo]) -> None:
        """
        
        """
        self.files: List[RealTimeS2CSessionTransferInitFileInfo] = files
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'files': [x.to_json() for x in self.files],
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> RealTimeS2CSessionTransferInit:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            files=[RealTimeS2CSessionTransferInitFileInfo.from_json(x) for x in json['files']],
        )
    
    def __str__(self) -> str:
        props = ', '.join([
            f'files={self.files}',
        ])
        return f'RealTimeS2CSessionTransferInit[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RealTimeS2CSessionTransferInit):
            return NotImplemented
        return self.files == other.files


class RealTimeS2CSessionTransferInitFileInfo:
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionTransferInit.FileInfo'
    
    def __init__(self, filename: str, bytes_total: int, bytes_transfered: int) -> None:
        """
        
        """
        self.filename: str = filename
        """
        (no description yet)
        """
        self.bytes_total: int = bytes_total
        """
        (no description yet)
        """
        self.bytes_transfered: int = bytes_transfered
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'filename': self.filename,
            'bytesTotal': self.bytes_total,
            'bytesTransfered': self.bytes_transfered,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> RealTimeS2CSessionTransferInitFileInfo:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            filename=cast(str, json['filename']),
            bytes_total=cast(int, json['bytesTotal']),
            bytes_transfered=cast(int, json['bytesTransfered']),
        )
    
    def __str__(self) -> str:
        props = ', '.join([
            f'filename={self.filename}',
            f'bytes_total={self.bytes_total}',
            f'bytes_transfered={self.bytes_transfered}',
        ])
        return f'RealTimeS2CSessionTransferInitFileInfo[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RealTimeS2CSessionTransferInitFileInfo):
            return NotImplemented
        return self.filename == other.filename \
            and self.bytes_total == other.bytes_total \
            and self.bytes_transfered == other.bytes_transfered


class Block:
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.pyp.Block'
    
    def __init__(self, block_id: str, name: str, description: str, group_ids: List[str]) -> None:
        """
        
        """
        self.block_id: str = block_id
        """
        (no description yet)
        """
        self.name: str = name
        """
        (no description yet)
        """
        self.description: str = description
        """
        (no description yet)
        """
        self.group_ids: List[str] = group_ids
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'blockId': self.block_id,
            'name': self.name,
            'description': self.description,
            'groupIds': [x for x in self.group_ids],
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> Block:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            block_id=cast(str, json['blockId']),
            name=cast(str, json['name']),
            description=cast(str, json['description']),
            group_ids=[cast(str, x) for x in json['groupIds']],
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
    """
    A way to represent the physical size of things in micrograph and tomogram images. These are params common to a set of source images.
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.pyp.ImagesScale'
    
    def __init__(self, particle_radius_unbinned: float, pixel_a: float, particle_radius_a: float) -> None:
        """
        A way to represent the physical size of things in micrograph and tomogram images. These are params common to a set of source images.
        """
        self.particle_radius_unbinned: float = particle_radius_unbinned
        """
        The particle radius, in unbinned pixels
        """
        self.pixel_a: float = pixel_a
        """
        The size, in Angstroms, of one pixel in the source image
        """
        self.particle_radius_a: float = particle_radius_a
        """
        The radius, in Angstroms, of a particle
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'particleRadiusUnbinned': self.particle_radius_unbinned,
            'pixelA': self.pixel_a,
            'particleRadiusA': self.particle_radius_a,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> ImagesScale:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            particle_radius_unbinned=cast(float, json['particleRadiusUnbinned']),
            pixel_a=cast(float, json['pixelA']),
            particle_radius_a=cast(float, json['particleRadiusA']),
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
        """
        Converts this enum value into JSON
        """
        
        return self.name
    
    @classmethod
    def from_json(cls, name: str) -> TomoVirMethod:
        """
        Reads this enum value from JSON
        """
        
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


class AppPermissionData:
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.AppPermissionData'
    
    def __init__(self, app_permission_id: str, description: Optional[str]) -> None:
        """
        
        """
        self.app_permission_id: str = app_permission_id
        """
        (no description yet)
        """
        self.description: Optional[str] = description
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'appPermissionId': self.app_permission_id,
            'description': self.description if self.description is not None else None,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> AppPermissionData:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            app_permission_id=cast(str, json['appPermissionId']),
            description=cast(str, json['description']) if 'description' in json and json['description'] is not None else None,
        )
    
    def __str__(self) -> str:
        props = ', '.join([
            f'app_permission_id={self.app_permission_id}',
            f'description={self.description}',
        ])
        return f'AppPermissionData[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, AppPermissionData):
            return NotImplemented
        return self.app_permission_id == other.app_permission_id \
            and self.description == other.description


class ReconstructionData:
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.ReconstructionData'
    
    def __init__(self, id: str, timestamp: int, class_num: int, iteration: int) -> None:
        """
        
        """
        self.id: str = id
        """
        (no description yet)
        """
        self.timestamp: int = timestamp
        """
        (no description yet)
        """
        self.class_num: int = class_num
        """
        (no description yet)
        """
        self.iteration: int = iteration
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'id': self.id,
            'timestamp': self.timestamp,
            'classNum': self.class_num,
            'iteration': self.iteration,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> ReconstructionData:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            id=cast(str, json['id']),
            timestamp=cast(int, json['timestamp']),
            class_num=cast(int, json['classNum']),
            iteration=cast(int, json['iteration']),
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
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RefinementData'
    
    def __init__(self, id: str, job_id: str, data_id: str, iteration: int, timestamp: int) -> None:
        """
        
        """
        self.id: str = id
        """
        (no description yet)
        """
        self.job_id: str = job_id
        """
        (no description yet)
        """
        self.data_id: str = data_id
        """
        eg a micrograph id or a tilt series id
        """
        self.iteration: int = iteration
        """
        (no description yet)
        """
        self.timestamp: int = timestamp
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'id': self.id,
            'jobId': self.job_id,
            'dataId': self.data_id,
            'iteration': self.iteration,
            'timestamp': self.timestamp,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> RefinementData:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            id=cast(str, json['id']),
            job_id=cast(str, json['jobId']),
            data_id=cast(str, json['dataId']),
            iteration=cast(int, json['iteration']),
            timestamp=cast(int, json['timestamp']),
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
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RefinementBundleData'
    
    def __init__(self, id: str, job_id: str, refinement_bundle_id: str, iteration: int, timestamp: int) -> None:
        """
        
        """
        self.id: str = id
        """
        (no description yet)
        """
        self.job_id: str = job_id
        """
        (no description yet)
        """
        self.refinement_bundle_id: str = refinement_bundle_id
        """
        (no description yet)
        """
        self.iteration: int = iteration
        """
        (no description yet)
        """
        self.timestamp: int = timestamp
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'id': self.id,
            'jobId': self.job_id,
            'refinementBundleId': self.refinement_bundle_id,
            'iteration': self.iteration,
            'timestamp': self.timestamp,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> RefinementBundleData:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            id=cast(str, json['id']),
            job_id=cast(str, json['jobId']),
            refinement_bundle_id=cast(str, json['refinementBundleId']),
            iteration=cast(int, json['iteration']),
            timestamp=cast(int, json['timestamp']),
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
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.PypStats'
    
    def __init__(self, scope_voltage: Optional[float], scope_pixel: Optional[float], scope_dose_rate: Optional[float], particle_radius: Optional[float]) -> None:
        """
        
        """
        self.scope_voltage: Optional[float] = scope_voltage
        """
        (no description yet)
        """
        self.scope_pixel: Optional[float] = scope_pixel
        """
        (no description yet)
        """
        self.scope_dose_rate: Optional[float] = scope_dose_rate
        """
        (no description yet)
        """
        self.particle_radius: Optional[float] = particle_radius
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'scopeVoltage': self.scope_voltage if self.scope_voltage is not None else None,
            'scopePixel': self.scope_pixel if self.scope_pixel is not None else None,
            'scopeDoseRate': self.scope_dose_rate if self.scope_dose_rate is not None else None,
            'particleRadius': self.particle_radius if self.particle_radius is not None else None,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> PypStats:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            scope_voltage=cast(float, json['scopeVoltage']) if 'scopeVoltage' in json and json['scopeVoltage'] is not None else None,
            scope_pixel=cast(float, json['scopePixel']) if 'scopePixel' in json and json['scopePixel'] is not None else None,
            scope_dose_rate=cast(float, json['scopeDoseRate']) if 'scopeDoseRate' in json and json['scopeDoseRate'] is not None else None,
            particle_radius=cast(float, json['particleRadius']) if 'particleRadius' in json and json['particleRadius'] is not None else None,
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
        """
        Converts this enum value into JSON
        """
        
        return self.name
    
    @classmethod
    def from_json(cls, name: str) -> ProjectPermission:
        """
        Reads this enum value from JSON
        """
        
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
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.UserData'
    
    def __init__(self, id: str, name: Optional[str]) -> None:
        """
        
        """
        self.id: str = id
        """
        (no description yet)
        """
        self.name: Optional[str] = name
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'id': self.id,
            'name': self.name if self.name is not None else None,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> UserData:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            id=cast(str, json['id']),
            name=cast(str, json['name']) if 'name' in json and json['name'] is not None else None,
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
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.ProjectRunData'
    
    def __init__(self, run_id: int, timestamp: int, status: RunStatus, jobs: List[JobRunData]) -> None:
        """
        
        """
        self.run_id: int = run_id
        """
        (no description yet)
        """
        self.timestamp: int = timestamp
        """
        (no description yet)
        """
        self.status: RunStatus = status
        """
        (no description yet)
        """
        self.jobs: List[JobRunData] = jobs
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'runId': self.run_id,
            'timestamp': self.timestamp,
            'status': self.status.to_json(),
            'jobs': [x.to_json() for x in self.jobs],
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> ProjectRunData:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            run_id=cast(int, json['runId']),
            timestamp=cast(int, json['timestamp']),
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
        """
        Converts this enum value into JSON
        """
        
        return self.name
    
    @classmethod
    def from_json(cls, name: str) -> ClusterJobResultType:
        """
        Reads this enum value from JSON
        """
        
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
        """
        Converts this enum value into JSON
        """
        
        return self.name
    
    @classmethod
    def from_json(cls, name: str) -> RunStatus:
        """
        Reads this enum value from JSON
        """
        
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
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.StreamLogMsg'
    
    def __init__(self, timestamp: int, level: int, path: str, line: int, msg: str) -> None:
        """
        
        """
        self.timestamp: int = timestamp
        """
        (no description yet)
        """
        self.level: int = level
        """
        (no description yet)
        """
        self.path: str = path
        """
        (no description yet)
        """
        self.line: int = line
        """
        (no description yet)
        """
        self.msg: str = msg
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'timestamp': self.timestamp,
            'level': self.level,
            'path': self.path,
            'line': self.line,
            'msg': self.msg,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> StreamLogMsg:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            timestamp=cast(int, json['timestamp']),
            level=cast(int, json['level']),
            path=cast(str, json['path']),
            line=cast(int, json['line']),
            msg=cast(str, json['msg']),
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
        """
        Converts this enum value into JSON
        """
        
        return self.name
    
    @classmethod
    def from_json(cls, name: str) -> SessionDaemon:
        """
        Reads this enum value from JSON
        """
        
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
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.SessionExportData'
    
    def __init__(self, session_id: str, export_id: str, request: str, created: int, cluster_job_id: Optional[str], result: Optional[str]) -> None:
        """
        
        """
        self.session_id: str = session_id
        """
        (no description yet)
        """
        self.export_id: str = export_id
        """
        (no description yet)
        """
        self.request: str = request
        """
        serialized SessionExportRequest
        """
        self.created: int = created
        """
        (no description yet)
        """
        self.cluster_job_id: Optional[str] = cluster_job_id
        """
        (no description yet)
        """
        self.result: Optional[str] = result
        """
        serialized SessionExportResult
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
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
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            session_id=cast(str, json['sessionId']),
            export_id=cast(str, json['exportId']),
            request=cast(str, json['request']),
            created=cast(int, json['created']),
            cluster_job_id=cast(str, json['clusterJobId']) if 'clusterJobId' in json and json['clusterJobId'] is not None else None,
            result=cast(str, json['result']) if 'result' in json and json['result'] is not None else None,
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
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.MicrographMetadata'
    
    def __init__(self, id: str, timestamp: int, ccc: float, cccc: float, defocus1: float, defocus2: float, angle_astig: float, average_motion: float, num_particles: int, source_dims: Optional[ImageDims]) -> None:
        """
        
        """
        self.id: str = id
        """
        (no description yet)
        """
        self.timestamp: int = timestamp
        """
        (no description yet)
        """
        self.ccc: float = ccc
        """
        (no description yet)
        """
        self.cccc: float = cccc
        """
        (no description yet)
        """
        self.defocus1: float = defocus1
        """
        (no description yet)
        """
        self.defocus2: float = defocus2
        """
        (no description yet)
        """
        self.angle_astig: float = angle_astig
        """
        (no description yet)
        """
        self.average_motion: float = average_motion
        """
        (no description yet)
        """
        self.num_particles: int = num_particles
        """
        (no description yet)
        """
        self.source_dims: Optional[ImageDims] = source_dims
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
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
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            id=cast(str, json['id']),
            timestamp=cast(int, json['timestamp']),
            ccc=cast(float, json['ccc']),
            cccc=cast(float, json['cccc']),
            defocus1=cast(float, json['defocus1']),
            defocus2=cast(float, json['defocus2']),
            angle_astig=cast(float, json['angleAstig']),
            average_motion=cast(float, json['averageMotion']),
            num_particles=cast(int, json['numParticles']),
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
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.TwoDClassesData'
    
    def __init__(self, owner_id: str, two_dclasses_id: str, created: int) -> None:
        """
        
        """
        self.owner_id: str = owner_id
        """
        (no description yet)
        """
        self.two_dclasses_id: str = two_dclasses_id
        """
        (no description yet)
        """
        self.created: int = created
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'ownerId': self.owner_id,
            'twoDClassesId': self.two_dclasses_id,
            'created': self.created,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> TwoDClassesData:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            owner_id=cast(str, json['ownerId']),
            two_dclasses_id=cast(str, json['twoDClassesId']),
            created=cast(int, json['created']),
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
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.TiltSeriesData'
    
    def __init__(self, id: str, timestamp: int, ccc: float, cccc: float, defocus1: float, defocus2: float, angle_astig: float, average_motion: float, num_particles: int, source_dims: Optional[ImageDims]) -> None:
        """
        
        """
        self.id: str = id
        """
        (no description yet)
        """
        self.timestamp: int = timestamp
        """
        (no description yet)
        """
        self.ccc: float = ccc
        """
        (no description yet)
        """
        self.cccc: float = cccc
        """
        (no description yet)
        """
        self.defocus1: float = defocus1
        """
        (no description yet)
        """
        self.defocus2: float = defocus2
        """
        (no description yet)
        """
        self.angle_astig: float = angle_astig
        """
        (no description yet)
        """
        self.average_motion: float = average_motion
        """
        (no description yet)
        """
        self.num_particles: int = num_particles
        """
        (no description yet)
        """
        self.source_dims: Optional[ImageDims] = source_dims
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
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
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            id=cast(str, json['id']),
            timestamp=cast(int, json['timestamp']),
            ccc=cast(float, json['ccc']),
            cccc=cast(float, json['cccc']),
            defocus1=cast(float, json['defocus1']),
            defocus2=cast(float, json['defocus2']),
            angle_astig=cast(float, json['angleAstig']),
            average_motion=cast(float, json['averageMotion']),
            num_particles=cast(int, json['numParticles']),
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
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.pyp.ImageDims'
    
    def __init__(self, num_slices: int, width: int, height: int, depth: int, binning_factor: int) -> None:
        """
        
        """
        self.num_slices: int = num_slices
        """
        (no description yet)
        """
        self.width: int = width
        """
        image width, in pixels
        """
        self.height: int = height
        """
        image height, in pixels
        """
        self.depth: int = depth
        """
        image depth, in pixels (for tomograms)
        """
        self.binning_factor: int = binning_factor
        """
        the binning factor, same for all dimensions
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'numSlices': self.num_slices,
            'width': self.width,
            'height': self.height,
            'depth': self.depth,
            'binningFactor': self.binning_factor,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> ImageDims:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            num_slices=cast(int, json['numSlices']),
            width=cast(int, json['width']),
            height=cast(int, json['height']),
            depth=cast(int, json['depth']),
            binning_factor=cast(int, json['binningFactor']),
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
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.JobRunData'
    
    def __init__(self, job_id: str, status: RunStatus, cluster_jobs: List[ClusterJobData]) -> None:
        """
        
        """
        self.job_id: str = job_id
        """
        (no description yet)
        """
        self.status: RunStatus = status
        """
        (no description yet)
        """
        self.cluster_jobs: List[ClusterJobData] = cluster_jobs
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'jobId': self.job_id,
            'status': self.status.to_json(),
            'clusterJobs': [x.to_json() for x in self.cluster_jobs],
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> JobRunData:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            job_id=cast(str, json['jobId']),
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
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.ClusterJobData'
    
    def __init__(self, cluster_job_id: str, web_name: Optional[str], cluster_name: Optional[str], status: RunStatus, array_info: Optional[ClusterJobDataArrayInfo]) -> None:
        """
        
        """
        self.cluster_job_id: str = cluster_job_id
        """
        (no description yet)
        """
        self.web_name: Optional[str] = web_name
        """
        (no description yet)
        """
        self.cluster_name: Optional[str] = cluster_name
        """
        (no description yet)
        """
        self.status: RunStatus = status
        """
        (no description yet)
        """
        self.array_info: Optional[ClusterJobDataArrayInfo] = array_info
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'clusterJobId': self.cluster_job_id,
            'webName': self.web_name if self.web_name is not None else None,
            'clusterName': self.cluster_name if self.cluster_name is not None else None,
            'status': self.status.to_json(),
            'arrayInfo': self.array_info.to_json() if self.array_info is not None else None,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> ClusterJobData:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            cluster_job_id=cast(str, json['clusterJobId']),
            web_name=cast(str, json['webName']) if 'webName' in json and json['webName'] is not None else None,
            cluster_name=cast(str, json['clusterName']) if 'clusterName' in json and json['clusterName'] is not None else None,
            status=RunStatus.from_json(json['status']),
            array_info=ClusterJobDataArrayInfo.from_json(json['arrayInfo']) if 'arrayInfo' in json and json['arrayInfo'] is not None else None,
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


class ClusterJobDataArrayInfo:
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.ClusterJobData.ArrayInfo'
    
    def __init__(self, size: int, started: int, ended: int, canceled: int, failed: int) -> None:
        """
        
        """
        self.size: int = size
        """
        (no description yet)
        """
        self.started: int = started
        """
        (no description yet)
        """
        self.ended: int = ended
        """
        (no description yet)
        """
        self.canceled: int = canceled
        """
        (no description yet)
        """
        self.failed: int = failed
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'size': self.size,
            'started': self.started,
            'ended': self.ended,
            'canceled': self.canceled,
            'failed': self.failed,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any]) -> ClusterJobDataArrayInfo:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            size=cast(int, json['size']),
            started=cast(int, json['started']),
            ended=cast(int, json['ended']),
            canceled=cast(int, json['canceled']),
            failed=cast(int, json['failed']),
        )
    
    def __str__(self) -> str:
        props = ', '.join([
            f'size={self.size}',
            f'started={self.started}',
            f'ended={self.ended}',
            f'canceled={self.canceled}',
            f'failed={self.failed}',
        ])
        return f'ClusterJobDataArrayInfo[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, ClusterJobDataArrayInfo):
            return NotImplemented
        return self.size == other.size \
            and self.started == other.started \
            and self.ended == other.ended \
            and self.canceled == other.canceled \
            and self.failed == other.failed
