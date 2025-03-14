
from __future__ import annotations

from typing import Optional, List, Dict, Set, Any, Iterator, TYPE_CHECKING, Union, cast, TypeVar, Generic, Callable
from abc import ABCMeta, abstractmethod

import json
from websockets.legacy.client import WebSocketClientProtocol

from nextpyp.client.realtime import RealtimeService, RealtimeServiceConnection, RealtimeServiceUnexpectedMessage
if TYPE_CHECKING:
    from nextpyp.client import Client


API_VERSION = '1.1.0'


T = TypeVar('T')
R = TypeVar('R')


ArgValuesToml = str


Option = list


Serialized_SessionExportResult = str
Serialized_SessionExportRequest = str


def optional_map(val: Optional[T], func: Callable[[T], R]) -> Optional[R]:
    """
    map the optional type,
    so we can avoid using intermediate variables and simplify the code generator
    """
    if val is None:
        return None
    else:
        return func(val)


def none_map(val: Optional[T], func: Callable[[], T]) -> T:
    """
    map the None value in the optional type,
    so we can avoid using intermediate variables and simplify the code generator
    """
    if val is None:
        return func()
    else:
        return val


def none_raise(val: Optional[T], func: Callable[[], Exception]) -> T:
    """
    if the optional type is None, raise the exception created by the lambda
    (because apparently Python doesn't allow lambdas consisting only of raise statements),
    so we can avoid using intermediate variables and simplify the code generator
    """
    if val is None:
        raise func()
    else:
        return val


def option_unwrap(val: Any) -> Optional[Any]:
    if len(val) == 1:
        return val[0]
    else:
        return None


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
        
        self.sessions: SessionsService = SessionsService(client)
        """
        The Sessions service.
        See: :py:class:`.SessionsService`
        """
        
        self.single_particle_sessions: SingleParticleSessionsService = SingleParticleSessionsService(client)
        """
        The SingleParticleSessions service.
        See: :py:class:`.SingleParticleSessionsService`
        """
        
        self.tomography_sessions: TomographySessionsService = TomographySessionsService(client)
        """
        The TomographySessions service.
        See: :py:class:`.TomographySessionsService`
        """
        




class AppsService:
    """
    Service providing functions specific to apps, mainly requesting and managing app tokens
    """
    
    def __init__(self, client: Client) -> None:
        self.client = client

    def versions(self) -> VersionData:
        """
        Returns the version numbers of NextPYP
        
        
        :Permission Needed: none
        """
        path = '/kv/apps/version'
        response = self.client._transport.call(path, [])
        if response is None:
            raise Exception(f'response expected from {path}, but none received')
        return VersionData.from_json(response)

    def request_token(self, user_id: str, app_name: str, app_permission_ids: List[str]) -> AppTokenRequestData:
        """
        Request an app token for your app on behalf of a specific user.
        Once requested, the user will need to approve the token request on the website. After approval, the user can copy the app token (it's a string) into your app.
        
        
        :Permission Needed: none
        """
        path = '/kv/apps/requestToken'
        response = self.client._transport.call(path, [user_id, app_name, [x for x in app_permission_ids]])
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
        
        :Permission Needed: ``project_list``
        """
        path = '/kv/projects/list'
        response = self.client._transport.call(path, [user_id])
        if response is None:
            raise Exception(f'response expected from {path}, but none received')
        return [ProjectData.from_json(x) for x in cast(List[Any], response)]


class SessionsService:
    """
    (no description yet)
    """
    
    def __init__(self, client: Client) -> None:
        self.client = client

    def session_options(self, search: Optional[str], initial: Optional[str], state: Optional[str]) -> List[RemoteOption]:
        """
        (no description yet)
        
        :Permission Needed: ``session_list``
        """
        path = '/kv/sessions/sessionOptions'
        response = self.client._transport.call(path, [search if search is not None else None, initial if initial is not None else None, state if state is not None else None])
        if response is None:
            raise Exception(f'response expected from {path}, but none received')
        return [RemoteOption.from_json(x) for x in cast(List[Any], response)]

    def groups(self) -> List[Group]:
        """
        (no description yet)
        
        :Permission Needed: ``group_list``
        """
        path = '/kv/sessions/groups'
        response = self.client._transport.call(path, [])
        if response is None:
            raise Exception(f'response expected from {path}, but none received')
        return [Group.from_json(x) for x in cast(List[Any], response)]

    def group_options(self, search: Optional[str], initial: Optional[str], state: Optional[str]) -> List[RemoteOption]:
        """
        (no description yet)
        
        :Permission Needed: ``group_list``
        """
        path = '/kv/sessions/groupOptions'
        response = self.client._transport.call(path, [search if search is not None else None, initial if initial is not None else None, state if state is not None else None])
        if response is None:
            raise Exception(f'response expected from {path}, but none received')
        return [RemoteOption.from_json(x) for x in cast(List[Any], response)]

    def running(self) -> RunningSessions:
        """
        (no description yet)
        
        :Permission Needed: ``session_list``
        """
        path = '/kv/sessions/running'
        response = self.client._transport.call(path, [])
        if response is None:
            raise Exception(f'response expected from {path}, but none received')
        return RunningSessions.from_json(response)

    def is_running(self, session_id: str, daemon: SessionDaemon) -> bool:
        """
        (no description yet)
        
        :Permission Needed: ``session_read``
        """
        path = '/kv/sessions/isRunning'
        response = self.client._transport.call(path, [session_id, daemon.to_json()])
        if response is None:
            raise Exception(f'response expected from {path}, but none received')
        return cast(bool, response)

    def start(self, session_id: str, daemon: SessionDaemon) -> None:
        """
        (no description yet)
        
        :Permission Needed: ``session_control``
        """
        path = '/kv/sessions/start'
        self.client._transport.call(path, [session_id, daemon.to_json()])

    def restart(self, session_id: str, daemon: SessionDaemon) -> None:
        """
        (no description yet)
        
        :Permission Needed: ``session_control``
        """
        path = '/kv/sessions/restart'
        self.client._transport.call(path, [session_id, daemon.to_json()])

    def clear(self, session_id: str, daemon: SessionDaemon) -> None:
        """
        (no description yet)
        
        :Permission Needed: ``session_control``
        """
        path = '/kv/sessions/clear'
        self.client._transport.call(path, [session_id, daemon.to_json()])

    def stop(self, session_id: str, daemon: SessionDaemon) -> None:
        """
        (no description yet)
        
        :Permission Needed: ``session_control``
        """
        path = '/kv/sessions/stop'
        self.client._transport.call(path, [session_id, daemon.to_json()])

    def cancel(self, session_id: str) -> None:
        """
        (no description yet)
        
        :Permission Needed: ``session_control``
        """
        path = '/kv/sessions/cancel'
        self.client._transport.call(path, [session_id])

    def logs(self, session_id: str, daemon: SessionDaemon) -> SessionLogs:
        """
        (no description yet)
        
        :Permission Needed: ``session_read``
        """
        path = '/kv/sessions/logs'
        response = self.client._transport.call(path, [session_id, daemon.to_json()])
        if response is None:
            raise Exception(f'response expected from {path}, but none received')
        return SessionLogs.from_json(response)

    def speeds(self, session_id: str) -> SessionSpeeds:
        """
        (no description yet)
        
        :Permission Needed: ``session_read``
        """
        path = '/kv/sessions/speeds'
        response = self.client._transport.call(path, [session_id])
        if response is None:
            raise Exception(f'response expected from {path}, but none received')
        return SessionSpeeds.from_json(response)

    def jobs_logs(self, session_id: str) -> SessionJobsLogs:
        """
        (no description yet)
        
        :Permission Needed: ``session_read``
        """
        path = '/kv/sessions/jobsLogs'
        response = self.client._transport.call(path, [session_id])
        if response is None:
            raise Exception(f'response expected from {path}, but none received')
        return SessionJobsLogs.from_json(response)

    def get_avg_rot(self, session_id: str, data_id: str) -> Optional[AvgRotData]:
        """
        (no description yet)
        
        :Permission Needed: ``session_read``
        """
        path = '/kv/sessions/avgRot'
        response = self.client._transport.call(path, [session_id, data_id])
        if response is None:
            raise Exception(f'response expected from {path}, but none received')
        return optional_map(option_unwrap(response), lambda x: AvgRotData.from_json(x))

    def get_motion(self, session_id: str, data_id: str) -> Optional[MotionData]:
        """
        (no description yet)
        
        :Permission Needed: ``session_read``
        """
        path = '/kv/sessions/motion'
        response = self.client._transport.call(path, [session_id, data_id])
        if response is None:
            raise Exception(f'response expected from {path}, but none received')
        return optional_map(option_unwrap(response), lambda x: MotionData.from_json(x))

    def data_log(self, session_id: str, data_id: str) -> str:
        """
        (no description yet)
        
        :Permission Needed: ``session_read``
        """
        path = '/kv/sessions/dataLog'
        response = self.client._transport.call(path, [session_id, data_id])
        if response is None:
            raise Exception(f'response expected from {path}, but none received')
        return cast(str, response)

    def list_filters(self, session_id: str) -> List[str]:
        """
        (no description yet)
        
        :Permission Needed: ``session_read``
        """
        path = '/kv/sessions/listFilters'
        response = self.client._transport.call(path, [session_id])
        if response is None:
            raise Exception(f'response expected from {path}, but none received')
        return [cast(str, x) for x in cast(List[Any], response)]

    def get_filter(self, session_id: str, name: str) -> PreprocessingFilter:
        """
        (no description yet)
        
        :Permission Needed: ``session_read``
        """
        path = '/kv/sessions/getFilter'
        response = self.client._transport.call(path, [session_id, name])
        if response is None:
            raise Exception(f'response expected from {path}, but none received')
        return PreprocessingFilter.from_json(response)

    def save_filter(self, session_id: str, filter: PreprocessingFilter) -> None:
        """
        (no description yet)
        
        :Permission Needed: ``session_write``
        """
        path = '/kv/sessions/saveFilter'
        self.client._transport.call(path, [session_id, filter.to_json()])

    def delete_filter(self, session_id: str, name: str) -> None:
        """
        (no description yet)
        
        :Permission Needed: ``session_write``
        """
        path = '/kv/sessions/deleteFilter'
        self.client._transport.call(path, [session_id, name])

    def filter_options(self, search: Optional[str], initial: Optional[str], state: Optional[str]) -> List[RemoteOption]:
        """
        (no description yet)
        
        :Permission Needed: ``session_read``
        """
        path = '/kv/sessions/filterOptions'
        response = self.client._transport.call(path, [search if search is not None else None, initial if initial is not None else None, state if state is not None else None])
        if response is None:
            raise Exception(f'response expected from {path}, but none received')
        return [RemoteOption.from_json(x) for x in cast(List[Any], response)]

    def export(self, session_id: str, request: Serialized_SessionExportRequest, slurm_values: ArgValuesToml) -> None:
        """
        (no description yet)
        
        :Permission Needed: ``session_export``
        """
        path = '/kv/sessions/export'
        self.client._transport.call(path, [session_id, request, slurm_values])

    def cancel_export(self, export_id: str) -> None:
        """
        (no description yet)
        
        :Permission Needed: ``session_export``
        """
        path = '/kv/sessions/cancelExport'
        self.client._transport.call(path, [export_id])


class SingleParticleSessionsService:
    """
    (no description yet)
    """
    
    def __init__(self, client: Client) -> None:
        self.client = client

    def list(self) -> List[SingleParticleSessionData]:
        """
        (no description yet)
        
        :Permission Needed: ``session_list``
        """
        path = '/kv/session/single-particle/list'
        response = self.client._transport.call(path, [])
        if response is None:
            raise Exception(f'response expected from {path}, but none received')
        return [SingleParticleSessionData.from_json(x) for x in cast(List[Any], response)]

    def create(self, args: SingleParticleSessionArgs) -> SingleParticleSessionData:
        """
        (no description yet)
        
        :Permission Needed: ``session_create``
        """
        path = '/kv/session/single-particle/create'
        response = self.client._transport.call(path, [args.to_json()])
        if response is None:
            raise Exception(f'response expected from {path}, but none received')
        return SingleParticleSessionData.from_json(response)

    def edit(self, session_id: str, args: SingleParticleSessionArgs) -> SingleParticleSessionData:
        """
        (no description yet)
        
        :Permission Needed: ``session_write``
        """
        path = '/kv/session/single-particle/edit'
        response = self.client._transport.call(path, [session_id, args.to_json()])
        if response is None:
            raise Exception(f'response expected from {path}, but none received')
        return SingleParticleSessionData.from_json(response)

    def get(self, session_id: str) -> SingleParticleSessionData:
        """
        (no description yet)
        
        :Permission Needed: ``session_read``
        """
        path = '/kv/session/single-particle/get'
        response = self.client._transport.call(path, [session_id])
        if response is None:
            raise Exception(f'response expected from {path}, but none received')
        return SingleParticleSessionData.from_json(response)

    def delete(self, session_id: str) -> None:
        """
        (no description yet)
        
        :Permission Needed: ``session_delete``
        """
        path = '/kv/session/single-particle/delete'
        self.client._transport.call(path, [session_id])


class TomographySessionsService:
    """
    (no description yet)
    """
    
    def __init__(self, client: Client) -> None:
        self.client = client

    def list(self) -> List[TomographySessionData]:
        """
        (no description yet)
        
        :Permission Needed: ``session_list``
        """
        path = '/kv/session/tomography/list'
        response = self.client._transport.call(path, [])
        if response is None:
            raise Exception(f'response expected from {path}, but none received')
        return [TomographySessionData.from_json(x) for x in cast(List[Any], response)]

    def create(self, args: TomographySessionArgs) -> TomographySessionData:
        """
        (no description yet)
        
        :Permission Needed: ``session_create``
        """
        path = '/kv/session/tomography/create'
        response = self.client._transport.call(path, [args.to_json()])
        if response is None:
            raise Exception(f'response expected from {path}, but none received')
        return TomographySessionData.from_json(response)

    def edit(self, session_id: str, args: TomographySessionArgs) -> TomographySessionData:
        """
        (no description yet)
        
        :Permission Needed: ``session_write``
        """
        path = '/kv/session/tomography/edit'
        response = self.client._transport.call(path, [session_id, args.to_json()])
        if response is None:
            raise Exception(f'response expected from {path}, but none received')
        return TomographySessionData.from_json(response)

    def get(self, session_id: str) -> TomographySessionData:
        """
        (no description yet)
        
        :Permission Needed: ``session_read``
        """
        path = '/kv/session/tomography/get'
        response = self.client._transport.call(path, [session_id])
        if response is None:
            raise Exception(f'response expected from {path}, but none received')
        return TomographySessionData.from_json(response)

    def delete(self, session_id: str) -> None:
        """
        (no description yet)
        
        :Permission Needed: ``session_delete``
        """
        path = '/kv/session/tomography/delete'
        self.client._transport.call(path, [session_id])

    def get_drift_metadata(self, session_id: str, tilt_series_id: str) -> Optional[DriftMetadata]:
        """
        (no description yet)
        
        :Permission Needed: ``session_read``
        """
        path = '/kv/session/tomography/driftMetadata'
        response = self.client._transport.call(path, [session_id, tilt_series_id])
        if response is None:
            raise Exception(f'response expected from {path}, but none received')
        return optional_map(option_unwrap(response), lambda x: DriftMetadata.from_json(x))


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
        The Project realtime service, see :py:class:`.ProjectRealtimeServiceConnection`
        """
        self.single_particle_session: RealtimeService[SingleParticleSessionRealtimeServiceConnection] = RealtimeService(client, '/ws/singleParticleSession', SingleParticleSessionRealtimeServiceConnection)
        """
        The SingleParticleSession realtime service, see :py:class:`.SingleParticleSessionRealtimeServiceConnection`
        """
        self.tomography_session: RealtimeService[TomographySessionRealtimeServiceConnection] = RealtimeService(client, '/ws/tomographySession', TomographySessionRealtimeServiceConnection)
        """
        The TomographySession realtime service, see :py:class:`.TomographySessionRealtimeServiceConnection`
        """


class ProjectRealtimeServiceConnection(RealtimeServiceConnection):
    """
    (no description yet)
    
    :Permission Needed: ``project_listen``
    
    :Client to Server messages:
    
    * :py:class:`.RealTimeC2SListenToProject`
    
    :Server to Client messages:
    
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


class SingleParticleSessionRealtimeServiceConnection(RealtimeServiceConnection):
    """
    (no description yet)
    
    :Permission Needed: ``session_listen``
    
    :Client to Server messages:
    
    * :py:class:`.RealTimeC2SListenToSession`
    * :py:class:`.RealTimeC2SSessionSettingsSaved`
    
    :Server to Client messages:
    
    * :py:class:`.RealTimeS2CSessionStatus`
    * :py:class:`.RealTimeS2CSessionSmallData`
    * :py:class:`.RealTimeS2CSessionLargeData`
    * :py:class:`.RealTimeS2CUpdatedParameters`
    * :py:class:`.RealTimeS2CSessionMicrograph`
    * :py:class:`.RealTimeS2CSessionTwoDClasses`
    * :py:class:`.RealTimeS2CSessionExport`
    * :py:class:`.RealTimeS2CSessionFilesystems`
    * :py:class:`.RealTimeS2CSessionTransferInit`
    * :py:class:`.RealTimeS2CSessionTransferWaiting`
    * :py:class:`.RealTimeS2CSessionTransferStarted`
    * :py:class:`.RealTimeS2CSessionTransferProgress`
    * :py:class:`.RealTimeS2CSessionTransferFinished`
    * :py:class:`.RealTimeS2CSessionDaemonSubmitted`
    * :py:class:`.RealTimeS2CSessionDaemonStarted`
    * :py:class:`.RealTimeS2CSessionDaemonFinished`
    * :py:class:`.RealTimeS2CSessionJobSubmitted`
    * :py:class:`.RealTimeS2CSessionJobStarted`
    * :py:class:`.RealTimeS2CSessionJobFinished`
    """
    
    def __init__(self, websocket: WebSocketClientProtocol) -> None:
        super(SingleParticleSessionRealtimeServiceConnection, self).__init__(websocket)
    
    async def send_listen_to_session(self, msg: RealTimeC2SListenToSession) -> None:
        """
        Sends a RealTimeC2SListenToSession message
        """
        
        j = msg.to_json()
        j['type'] = RealTimeC2SListenToSession.TYPE_ID
        await self._send(j)
    
    async def send_session_settings_saved(self, msg: RealTimeC2SSessionSettingsSaved) -> None:
        """
        Sends a RealTimeC2SSessionSettingsSaved message
        """
        
        j = msg.to_json()
        j['type'] = RealTimeC2SSessionSettingsSaved.TYPE_ID
        await self._send(j)
    
    async def recv(self) -> Union[RealTimeS2CSessionStatus, RealTimeS2CSessionSmallData, RealTimeS2CSessionLargeData, RealTimeS2CUpdatedParameters, RealTimeS2CSessionMicrograph, RealTimeS2CSessionTwoDClasses, RealTimeS2CSessionExport, RealTimeS2CSessionFilesystems, RealTimeS2CSessionTransferInit, RealTimeS2CSessionTransferWaiting, RealTimeS2CSessionTransferStarted, RealTimeS2CSessionTransferProgress, RealTimeS2CSessionTransferFinished, RealTimeS2CSessionDaemonSubmitted, RealTimeS2CSessionDaemonStarted, RealTimeS2CSessionDaemonFinished, RealTimeS2CSessionJobSubmitted, RealTimeS2CSessionJobStarted, RealTimeS2CSessionJobFinished]:
        """
        Receives a message from the website. Could be any one of several different messages.
        
        Examples
        --------
        
        Receive a message from this realtime service:
        
        .. code-block:: python
        
            msg = await project.recv()
            if type(msg) is RealTimeS2CSessionStatus:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CSessionSmallData:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CSessionLargeData:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CUpdatedParameters:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CSessionMicrograph:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CSessionTwoDClasses:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CSessionExport:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CSessionFilesystems:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CSessionTransferInit:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CSessionTransferWaiting:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CSessionTransferStarted:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CSessionTransferProgress:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CSessionTransferFinished:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CSessionDaemonSubmitted:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CSessionDaemonStarted:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CSessionDaemonFinished:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CSessionJobSubmitted:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CSessionJobStarted:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CSessionJobFinished:
                print(f'received message: {msg}')
            else:
                raise Exception(f'received unexpected msg: {msg}')
        """
        
        msg = await self._recv()
        type = msg.get('type')
        match type:
            case RealTimeS2CSessionStatus.TYPE_ID:
                return RealTimeS2CSessionStatus.from_json(msg)
            case RealTimeS2CSessionSmallData.TYPE_ID:
                return RealTimeS2CSessionSmallData.from_json(msg)
            case RealTimeS2CSessionLargeData.TYPE_ID:
                return RealTimeS2CSessionLargeData.from_json(msg)
            case RealTimeS2CUpdatedParameters.TYPE_ID:
                return RealTimeS2CUpdatedParameters.from_json(msg)
            case RealTimeS2CSessionMicrograph.TYPE_ID:
                return RealTimeS2CSessionMicrograph.from_json(msg)
            case RealTimeS2CSessionTwoDClasses.TYPE_ID:
                return RealTimeS2CSessionTwoDClasses.from_json(msg)
            case RealTimeS2CSessionExport.TYPE_ID:
                return RealTimeS2CSessionExport.from_json(msg)
            case RealTimeS2CSessionFilesystems.TYPE_ID:
                return RealTimeS2CSessionFilesystems.from_json(msg)
            case RealTimeS2CSessionTransferInit.TYPE_ID:
                return RealTimeS2CSessionTransferInit.from_json(msg)
            case RealTimeS2CSessionTransferWaiting.TYPE_ID:
                return RealTimeS2CSessionTransferWaiting.from_json(msg)
            case RealTimeS2CSessionTransferStarted.TYPE_ID:
                return RealTimeS2CSessionTransferStarted.from_json(msg)
            case RealTimeS2CSessionTransferProgress.TYPE_ID:
                return RealTimeS2CSessionTransferProgress.from_json(msg)
            case RealTimeS2CSessionTransferFinished.TYPE_ID:
                return RealTimeS2CSessionTransferFinished.from_json(msg)
            case RealTimeS2CSessionDaemonSubmitted.TYPE_ID:
                return RealTimeS2CSessionDaemonSubmitted.from_json(msg)
            case RealTimeS2CSessionDaemonStarted.TYPE_ID:
                return RealTimeS2CSessionDaemonStarted.from_json(msg)
            case RealTimeS2CSessionDaemonFinished.TYPE_ID:
                return RealTimeS2CSessionDaemonFinished.from_json(msg)
            case RealTimeS2CSessionJobSubmitted.TYPE_ID:
                return RealTimeS2CSessionJobSubmitted.from_json(msg)
            case RealTimeS2CSessionJobStarted.TYPE_ID:
                return RealTimeS2CSessionJobStarted.from_json(msg)
            case RealTimeS2CSessionJobFinished.TYPE_ID:
                return RealTimeS2CSessionJobFinished.from_json(msg)
            case _:
                raise RealtimeServiceUnexpectedMessage(type)


class TomographySessionRealtimeServiceConnection(RealtimeServiceConnection):
    """
    (no description yet)
    
    :Permission Needed: ``session_listen``
    
    :Client to Server messages:
    
    * :py:class:`.RealTimeC2SListenToSession`
    * :py:class:`.RealTimeC2SSessionSettingsSaved`
    
    :Server to Client messages:
    
    * :py:class:`.RealTimeS2CSessionStatus`
    * :py:class:`.RealTimeS2CSessionSmallData`
    * :py:class:`.RealTimeS2CSessionLargeData`
    * :py:class:`.RealTimeS2CUpdatedParameters`
    * :py:class:`.RealTimeS2CSessionTiltSeries`
    * :py:class:`.RealTimeS2CSessionExport`
    * :py:class:`.RealTimeS2CSessionFilesystems`
    * :py:class:`.RealTimeS2CSessionTransferInit`
    * :py:class:`.RealTimeS2CSessionTransferWaiting`
    * :py:class:`.RealTimeS2CSessionTransferStarted`
    * :py:class:`.RealTimeS2CSessionTransferProgress`
    * :py:class:`.RealTimeS2CSessionTransferFinished`
    * :py:class:`.RealTimeS2CSessionDaemonSubmitted`
    * :py:class:`.RealTimeS2CSessionDaemonStarted`
    * :py:class:`.RealTimeS2CSessionDaemonFinished`
    * :py:class:`.RealTimeS2CSessionJobSubmitted`
    * :py:class:`.RealTimeS2CSessionJobStarted`
    * :py:class:`.RealTimeS2CSessionJobFinished`
    """
    
    def __init__(self, websocket: WebSocketClientProtocol) -> None:
        super(TomographySessionRealtimeServiceConnection, self).__init__(websocket)
    
    async def send_listen_to_session(self, msg: RealTimeC2SListenToSession) -> None:
        """
        Sends a RealTimeC2SListenToSession message
        """
        
        j = msg.to_json()
        j['type'] = RealTimeC2SListenToSession.TYPE_ID
        await self._send(j)
    
    async def send_session_settings_saved(self, msg: RealTimeC2SSessionSettingsSaved) -> None:
        """
        Sends a RealTimeC2SSessionSettingsSaved message
        """
        
        j = msg.to_json()
        j['type'] = RealTimeC2SSessionSettingsSaved.TYPE_ID
        await self._send(j)
    
    async def recv(self) -> Union[RealTimeS2CSessionStatus, RealTimeS2CSessionSmallData, RealTimeS2CSessionLargeData, RealTimeS2CUpdatedParameters, RealTimeS2CSessionTiltSeries, RealTimeS2CSessionExport, RealTimeS2CSessionFilesystems, RealTimeS2CSessionTransferInit, RealTimeS2CSessionTransferWaiting, RealTimeS2CSessionTransferStarted, RealTimeS2CSessionTransferProgress, RealTimeS2CSessionTransferFinished, RealTimeS2CSessionDaemonSubmitted, RealTimeS2CSessionDaemonStarted, RealTimeS2CSessionDaemonFinished, RealTimeS2CSessionJobSubmitted, RealTimeS2CSessionJobStarted, RealTimeS2CSessionJobFinished]:
        """
        Receives a message from the website. Could be any one of several different messages.
        
        Examples
        --------
        
        Receive a message from this realtime service:
        
        .. code-block:: python
        
            msg = await project.recv()
            if type(msg) is RealTimeS2CSessionStatus:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CSessionSmallData:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CSessionLargeData:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CUpdatedParameters:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CSessionTiltSeries:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CSessionExport:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CSessionFilesystems:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CSessionTransferInit:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CSessionTransferWaiting:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CSessionTransferStarted:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CSessionTransferProgress:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CSessionTransferFinished:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CSessionDaemonSubmitted:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CSessionDaemonStarted:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CSessionDaemonFinished:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CSessionJobSubmitted:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CSessionJobStarted:
                print(f'received message: {msg}')
            elif type(msg) is RealTimeS2CSessionJobFinished:
                print(f'received message: {msg}')
            else:
                raise Exception(f'received unexpected msg: {msg}')
        """
        
        msg = await self._recv()
        type = msg.get('type')
        match type:
            case RealTimeS2CSessionStatus.TYPE_ID:
                return RealTimeS2CSessionStatus.from_json(msg)
            case RealTimeS2CSessionSmallData.TYPE_ID:
                return RealTimeS2CSessionSmallData.from_json(msg)
            case RealTimeS2CSessionLargeData.TYPE_ID:
                return RealTimeS2CSessionLargeData.from_json(msg)
            case RealTimeS2CUpdatedParameters.TYPE_ID:
                return RealTimeS2CUpdatedParameters.from_json(msg)
            case RealTimeS2CSessionTiltSeries.TYPE_ID:
                return RealTimeS2CSessionTiltSeries.from_json(msg)
            case RealTimeS2CSessionExport.TYPE_ID:
                return RealTimeS2CSessionExport.from_json(msg)
            case RealTimeS2CSessionFilesystems.TYPE_ID:
                return RealTimeS2CSessionFilesystems.from_json(msg)
            case RealTimeS2CSessionTransferInit.TYPE_ID:
                return RealTimeS2CSessionTransferInit.from_json(msg)
            case RealTimeS2CSessionTransferWaiting.TYPE_ID:
                return RealTimeS2CSessionTransferWaiting.from_json(msg)
            case RealTimeS2CSessionTransferStarted.TYPE_ID:
                return RealTimeS2CSessionTransferStarted.from_json(msg)
            case RealTimeS2CSessionTransferProgress.TYPE_ID:
                return RealTimeS2CSessionTransferProgress.from_json(msg)
            case RealTimeS2CSessionTransferFinished.TYPE_ID:
                return RealTimeS2CSessionTransferFinished.from_json(msg)
            case RealTimeS2CSessionDaemonSubmitted.TYPE_ID:
                return RealTimeS2CSessionDaemonSubmitted.from_json(msg)
            case RealTimeS2CSessionDaemonStarted.TYPE_ID:
                return RealTimeS2CSessionDaemonStarted.from_json(msg)
            case RealTimeS2CSessionDaemonFinished.TYPE_ID:
                return RealTimeS2CSessionDaemonFinished.from_json(msg)
            case RealTimeS2CSessionJobSubmitted.TYPE_ID:
                return RealTimeS2CSessionJobSubmitted.from_json(msg)
            case RealTimeS2CSessionJobStarted.TYPE_ID:
                return RealTimeS2CSessionJobStarted.from_json(msg)
            case RealTimeS2CSessionJobFinished.TYPE_ID:
                return RealTimeS2CSessionJobFinished.from_json(msg)
            case _:
                raise RealtimeServiceUnexpectedMessage(type)


class RemoteOption:
    """
    Search result option, with some options for presentation
    """
    
    TYPE_ID: str = 'io.kvision.remote.RemoteOption'
    
    def __init__(self, value: Optional[str], text: Optional[str], class_name: Optional[str], subtext: Optional[str], icon: Optional[str], content: Optional[str], disabled: bool, divider: bool) -> None:
        self.value: Optional[str] = value
        """
        (no description yet)
        """
        self.text: Optional[str] = text
        """
        (no description yet)
        """
        self.class_name: Optional[str] = class_name
        """
        (no description yet)
        """
        self.subtext: Optional[str] = subtext
        """
        (no description yet)
        """
        self.icon: Optional[str] = icon
        """
        (no description yet)
        """
        self.content: Optional[str] = content
        """
        (no description yet)
        """
        self.disabled: bool = disabled
        """
        (no description yet)
        """
        self.divider: bool = divider
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'value': self.value if self.value is not None else None,
            'text': self.text if self.text is not None else None,
            'className': self.class_name if self.class_name is not None else None,
            'subtext': self.subtext if self.subtext is not None else None,
            'icon': self.icon if self.icon is not None else None,
            'content': self.content if self.content is not None else None,
            'disabled': self.disabled,
            'divider': self.divider,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RemoteOption:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            optional_map(json.get('value', None), lambda it: cast(str, it)),
            optional_map(json.get('text', None), lambda it: cast(str, it)),
            optional_map(json.get('className', None), lambda it: cast(str, it)),
            optional_map(json.get('subtext', None), lambda it: cast(str, it)),
            optional_map(json.get('icon', None), lambda it: cast(str, it)),
            optional_map(json.get('content', None), lambda it: cast(str, it)),
            none_map(optional_map(json.get('disabled', None), lambda it: cast(bool, it)), lambda: False),
            none_map(optional_map(json.get('divider', None), lambda it: cast(bool, it)), lambda: False),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RemoteOption:
        return RemoteOption.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'value={self.value}',
            f'text={self.text}',
            f'class_name={self.class_name}',
            f'subtext={self.subtext}',
            f'icon={self.icon}',
            f'content={self.content}',
            f'disabled={self.disabled}',
            f'divider={self.divider}',
        ])
        return f'RemoteOption[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RemoteOption):
            return NotImplemented
        return self.value == other.value \
            and self.text == other.text \
            and self.class_name == other.class_name \
            and self.subtext == other.subtext \
            and self.icon == other.icon \
            and self.content == other.content \
            and self.disabled == other.disabled \
            and self.divider == other.divider


class Group:
    """
    Represents a group of users (usually an academic lab)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.Group'
    
    def __init__(self, name: str, id: Optional[str]) -> None:
        self.name: str = name
        """
        a display name
        """
        self.id: Optional[str] = id
        """
        a unique identifier
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'name': self.name,
            'id': self.id if self.id is not None else None,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> Group:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('name', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: name')),
            optional_map(json.get('id', None), lambda it: cast(str, it)),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> Group:
        return Group.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'name={self.name}',
            f'id={self.id}',
        ])
        return f'Group[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, Group):
            return NotImplemented
        return self.name == other.name \
            and self.id == other.id


class VersionData:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.VersionData'
    
    def __init__(self, version: str, api_version: str) -> None:
        self.version: str = version
        """
        The version of nextPYP itself
        """
        self.api_version: str = api_version
        """
        The version of the nextPYP API, to determine compatibility with API clients
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'version': self.version,
            'apiVersion': self.api_version,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> VersionData:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('version', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: version')),
            none_raise(optional_map(json.get('apiVersion', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: apiVersion')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> VersionData:
        return VersionData.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'version={self.version}',
            f'api_version={self.api_version}',
        ])
        return f'VersionData[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, VersionData):
            return NotImplemented
        return self.version == other.version \
            and self.api_version == other.api_version


class AppTokenRequestData:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.AppTokenRequestData'
    
    def __init__(self, request_id: str, app_name: str, permissions: List[AppPermissionData]) -> None:
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
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> AppTokenRequestData:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('requestId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: requestId')),
            none_raise(optional_map(json.get('appName', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: appName')),
            none_raise(optional_map(json.get('permissions', None), lambda it: [AppPermissionData.from_json(x) for x in cast(List[Any], it)]), lambda: KeyError('missing JSON key: permissions')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> AppTokenRequestData:
        return AppTokenRequestData.from_json(json.loads(serialized), type_ids)
    
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


class PreprocessingFilter:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.PreprocessingFilter'
    
    def __init__(self, name: str, ranges: List[PreprocessingPropRange], excluded_ids: List[str]) -> None:
        self.name: str = name
        """
        (no description yet)
        """
        self.ranges: List[PreprocessingPropRange] = ranges
        """
        (no description yet)
        """
        self.excluded_ids: List[str] = excluded_ids
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'name': self.name,
            'ranges': [x.to_json() for x in self.ranges],
            'excludedIds': [x for x in self.excluded_ids],
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> PreprocessingFilter:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('name', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: name')),
            none_raise(optional_map(json.get('ranges', None), lambda it: [PreprocessingPropRange.from_json(x) for x in cast(List[Any], it)]), lambda: KeyError('missing JSON key: ranges')),
            none_raise(optional_map(json.get('excludedIds', None), lambda it: [cast(str, x) for x in cast(List[Any], it)]), lambda: KeyError('missing JSON key: excludedIds')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> PreprocessingFilter:
        return PreprocessingFilter.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'name={self.name}',
            f'ranges={self.ranges}',
            f'excluded_ids={self.excluded_ids}',
        ])
        return f'PreprocessingFilter[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, PreprocessingFilter):
            return NotImplemented
        return self.name == other.name \
            and self.ranges == other.ranges \
            and self.excluded_ids == other.excluded_ids


class ProjectData:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.ProjectData'
    
    def __init__(self, owner: UserData, permissions: Set[ProjectPermission], project_id: str, project_number: Optional[int], project_name: str, created: int, images: List[str], path: str) -> None:
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
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> ProjectData:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('owner', None), lambda it: UserData.from_json(it)), lambda: KeyError('missing JSON key: owner')),
            none_raise(optional_map(json.get('permissions', None), lambda it: {ProjectPermission.from_json(x) for x in cast(Set[Any], it)}), lambda: KeyError('missing JSON key: permissions')),
            none_raise(optional_map(json.get('projectId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: projectId')),
            optional_map(json.get('projectNumber', None), lambda it: cast(int, it)),
            none_raise(optional_map(json.get('projectName', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: projectName')),
            none_raise(optional_map(json.get('created', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: created')),
            none_raise(optional_map(json.get('images', None), lambda it: [cast(str, x) for x in cast(List[Any], it)]), lambda: KeyError('missing JSON key: images')),
            none_raise(optional_map(json.get('path', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: path')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> ProjectData:
        return ProjectData.from_json(json.loads(serialized), type_ids)
    
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
    client-to-server (C2S) messages for real-time communication
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeC2S'
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RealTimeC2S:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RealTimeC2S:
        return RealTimeC2S.from_json(json.loads(serialized), type_ids)
    
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
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeC2S.ListenToProject'
    
    def __init__(self, user_id: str, project_id: str) -> None:
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
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RealTimeC2SListenToProject:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('userId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: userId')),
            none_raise(optional_map(json.get('projectId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: projectId')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RealTimeC2SListenToProject:
        return RealTimeC2SListenToProject.from_json(json.loads(serialized), type_ids)
    
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


class RealTimeC2SListenToSession:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeC2S.ListenToSession'
    
    def __init__(self, session_id: str) -> None:
        self.session_id: str = session_id
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'sessionId': self.session_id,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RealTimeC2SListenToSession:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('sessionId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: sessionId')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RealTimeC2SListenToSession:
        return RealTimeC2SListenToSession.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'session_id={self.session_id}',
        ])
        return f'RealTimeC2SListenToSession[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RealTimeC2SListenToSession):
            return NotImplemented
        return self.session_id == other.session_id


class RealTimeC2SSessionSettingsSaved:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeC2S.SessionSettingsSaved'
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RealTimeC2SSessionSettingsSaved:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RealTimeC2SSessionSettingsSaved:
        return RealTimeC2SSessionSettingsSaved.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
        ])
        return f'RealTimeC2SSessionSettingsSaved[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RealTimeC2SSessionSettingsSaved):
            return NotImplemented
        return True  # we are all the same! =D


class RealTimeS2C:
    """
    server-to-client (S2C) messages for real-time communication
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C'
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2C:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2C:
        return RealTimeS2C.from_json(json.loads(serialized), type_ids)
    
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
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.Error'
    
    def __init__(self, name: Optional[str], msg: Optional[str]) -> None:
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
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CError:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            optional_map(json.get('name', None), lambda it: cast(str, it)),
            optional_map(json.get('msg', None), lambda it: cast(str, it)),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CError:
        return RealTimeS2CError.from_json(json.loads(serialized), type_ids)
    
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
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.ProjectStatus'
    
    def __init__(self, recent_runs: List[ProjectRunData], has_older_runs: bool, blocks: List[Block]) -> None:
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
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CProjectStatus:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('recentRuns', None), lambda it: [ProjectRunData.from_json(x) for x in cast(List[Any], it)]), lambda: KeyError('missing JSON key: recentRuns')),
            none_raise(optional_map(json.get('hasOlderRuns', None), lambda it: cast(bool, it)), lambda: KeyError('missing JSON key: hasOlderRuns')),
            none_raise(optional_map(json.get('blocks', None), lambda it: [Block.from_json(x) for x in cast(List[Any], it)]), lambda: KeyError('missing JSON key: blocks')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CProjectStatus:
        return RealTimeS2CProjectStatus.from_json(json.loads(serialized), type_ids)
    
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
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.ProjectRunInit'
    
    def __init__(self, run_id: int, timestamp: int, job_ids: List[str]) -> None:
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
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CProjectRunInit:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('runId', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: runId')),
            none_raise(optional_map(json.get('timestamp', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: timestamp')),
            none_raise(optional_map(json.get('jobIds', None), lambda it: [cast(str, x) for x in cast(List[Any], it)]), lambda: KeyError('missing JSON key: jobIds')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CProjectRunInit:
        return RealTimeS2CProjectRunInit.from_json(json.loads(serialized), type_ids)
    
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
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.ProjectRunStart'
    
    def __init__(self, run_id: int) -> None:
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
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CProjectRunStart:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('runId', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: runId')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CProjectRunStart:
        return RealTimeS2CProjectRunStart.from_json(json.loads(serialized), type_ids)
    
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
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.JobStart'
    
    def __init__(self, run_id: int, job_id: str) -> None:
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
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CJobStart:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('runId', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: runId')),
            none_raise(optional_map(json.get('jobId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: jobId')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CJobStart:
        return RealTimeS2CJobStart.from_json(json.loads(serialized), type_ids)
    
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
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.JobUpdate'
    
    def __init__(self, job_id: str, job_string: str) -> None:
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
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CJobUpdate:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('jobId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: jobId')),
            none_raise(optional_map(json.get('jobString', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: jobString')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CJobUpdate:
        return RealTimeS2CJobUpdate.from_json(json.loads(serialized), type_ids)
    
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
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.JobFinish'
    
    def __init__(self, run_id: int, job_id: str, job_string: str, status: RunStatus, error_message: Optional[str]) -> None:
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
        self.error_message: Optional[str] = error_message
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
            'errorMessage': self.error_message if self.error_message is not None else None,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CJobFinish:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('runId', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: runId')),
            none_raise(optional_map(json.get('jobId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: jobId')),
            none_raise(optional_map(json.get('jobString', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: jobString')),
            none_raise(optional_map(json.get('status', None), lambda it: RunStatus.from_json(it)), lambda: KeyError('missing JSON key: status')),
            optional_map(json.get('errorMessage', None), lambda it: cast(str, it)),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CJobFinish:
        return RealTimeS2CJobFinish.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'run_id={self.run_id}',
            f'job_id={self.job_id}',
            f'job_string={self.job_string}',
            f'status={self.status}',
            f'error_message={self.error_message}',
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
            and self.status == other.status \
            and self.error_message == other.error_message


class RealTimeS2CProjectRunFinish:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.ProjectRunFinish'
    
    def __init__(self, run_id: int, status: RunStatus) -> None:
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
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CProjectRunFinish:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('runId', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: runId')),
            none_raise(optional_map(json.get('status', None), lambda it: RunStatus.from_json(it)), lambda: KeyError('missing JSON key: status')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CProjectRunFinish:
        return RealTimeS2CProjectRunFinish.from_json(json.loads(serialized), type_ids)
    
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
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.ClusterJobSubmit'
    
    def __init__(self, run_id: int, job_id: str, cluster_job_id: str, cluster_job_name: Optional[str], array_size: Optional[int]) -> None:
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
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CClusterJobSubmit:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('runId', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: runId')),
            none_raise(optional_map(json.get('jobId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: jobId')),
            none_raise(optional_map(json.get('clusterJobId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: clusterJobId')),
            optional_map(json.get('clusterJobName', None), lambda it: cast(str, it)),
            optional_map(json.get('arraySize', None), lambda it: cast(int, it)),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CClusterJobSubmit:
        return RealTimeS2CClusterJobSubmit.from_json(json.loads(serialized), type_ids)
    
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
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.ClusterJobStart'
    
    def __init__(self, run_id: int, job_id: str, cluster_job_id: str) -> None:
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
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CClusterJobStart:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('runId', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: runId')),
            none_raise(optional_map(json.get('jobId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: jobId')),
            none_raise(optional_map(json.get('clusterJobId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: clusterJobId')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CClusterJobStart:
        return RealTimeS2CClusterJobStart.from_json(json.loads(serialized), type_ids)
    
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
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.ClusterJobArrayStart'
    
    def __init__(self, run_id: int, job_id: str, cluster_job_id: str, array_index: int, num_started: int) -> None:
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
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CClusterJobArrayStart:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('runId', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: runId')),
            none_raise(optional_map(json.get('jobId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: jobId')),
            none_raise(optional_map(json.get('clusterJobId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: clusterJobId')),
            none_raise(optional_map(json.get('arrayIndex', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: arrayIndex')),
            none_raise(optional_map(json.get('numStarted', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: numStarted')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CClusterJobArrayStart:
        return RealTimeS2CClusterJobArrayStart.from_json(json.loads(serialized), type_ids)
    
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
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.ClusterJobArrayEnd'
    
    def __init__(self, run_id: int, job_id: str, cluster_job_id: str, array_index: int, num_ended: int, num_canceled: int, num_failed: int) -> None:
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
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CClusterJobArrayEnd:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('runId', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: runId')),
            none_raise(optional_map(json.get('jobId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: jobId')),
            none_raise(optional_map(json.get('clusterJobId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: clusterJobId')),
            none_raise(optional_map(json.get('arrayIndex', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: arrayIndex')),
            none_raise(optional_map(json.get('numEnded', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: numEnded')),
            none_raise(optional_map(json.get('numCanceled', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: numCanceled')),
            none_raise(optional_map(json.get('numFailed', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: numFailed')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CClusterJobArrayEnd:
        return RealTimeS2CClusterJobArrayEnd.from_json(json.loads(serialized), type_ids)
    
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
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.ClusterJobEnd'
    
    def __init__(self, run_id: int, job_id: str, cluster_job_id: str, result_type: ClusterJobResultType) -> None:
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
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CClusterJobEnd:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('runId', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: runId')),
            none_raise(optional_map(json.get('jobId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: jobId')),
            none_raise(optional_map(json.get('clusterJobId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: clusterJobId')),
            none_raise(optional_map(json.get('resultType', None), lambda it: ClusterJobResultType.from_json(it)), lambda: KeyError('missing JSON key: resultType')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CClusterJobEnd:
        return RealTimeS2CClusterJobEnd.from_json(json.loads(serialized), type_ids)
    
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


class RealTimeS2CUpdatedParameters:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.UpdatedParameters'
    
    def __init__(self, pyp_stats: PypStats) -> None:
        self.pyp_stats: PypStats = pyp_stats
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'pypStats': self.pyp_stats.to_json(),
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CUpdatedParameters:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('pypStats', None), lambda it: PypStats.from_json(it)), lambda: KeyError('missing JSON key: pypStats')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CUpdatedParameters:
        return RealTimeS2CUpdatedParameters.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'pyp_stats={self.pyp_stats}',
        ])
        return f'RealTimeS2CUpdatedParameters[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RealTimeS2CUpdatedParameters):
            return NotImplemented
        return self.pyp_stats == other.pyp_stats


class RealTimeS2CSessionStatus:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionStatus'
    
    def __init__(self, daemons_running: List[bool], jobs_running: List[RealTimeS2CSessionRunningJob], tomo_vir_method: TomoVirMethod, tomo_vir_rad: ValueA, tomo_vir_binn: int, tomo_vir_detect_method: TomoVirDetectMethod, tomo_spk_method: TomoSpkMethod, tomo_spk_rad: ValueA) -> None:
        self.daemons_running: List[bool] = daemons_running
        """
        in order of SessionDaemon.values()
        """
        self.jobs_running: List[RealTimeS2CSessionRunningJob] = jobs_running
        """
        (no description yet)
        """
        self.tomo_vir_method: TomoVirMethod = tomo_vir_method
        """
        (no description yet)
        """
        self.tomo_vir_rad: ValueA = tomo_vir_rad
        """
        (no description yet)
        """
        self.tomo_vir_binn: int = tomo_vir_binn
        """
        (no description yet)
        """
        self.tomo_vir_detect_method: TomoVirDetectMethod = tomo_vir_detect_method
        """
        (no description yet)
        """
        self.tomo_spk_method: TomoSpkMethod = tomo_spk_method
        """
        (no description yet)
        """
        self.tomo_spk_rad: ValueA = tomo_spk_rad
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'daemonsRunning': [x for x in self.daemons_running],
            'jobsRunning': [x.to_json() for x in self.jobs_running],
            'tomoVirMethod': self.tomo_vir_method.to_json(),
            'tomoVirRad': self.tomo_vir_rad.to_json(),
            'tomoVirBinn': self.tomo_vir_binn,
            'tomoVirDetectMethod': self.tomo_vir_detect_method.to_json(),
            'tomoSpkMethod': self.tomo_spk_method.to_json(),
            'tomoSpkRad': self.tomo_spk_rad.to_json(),
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionStatus:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('daemonsRunning', None), lambda it: [cast(bool, x) for x in cast(List[Any], it)]), lambda: KeyError('missing JSON key: daemonsRunning')),
            none_raise(optional_map(json.get('jobsRunning', None), lambda it: [RealTimeS2CSessionRunningJob.from_json(x) for x in cast(List[Any], it)]), lambda: KeyError('missing JSON key: jobsRunning')),
            none_raise(optional_map(json.get('tomoVirMethod', None), lambda it: TomoVirMethod.from_json(it)), lambda: KeyError('missing JSON key: tomoVirMethod')),
            none_raise(optional_map(json.get('tomoVirRad', None), lambda it: ValueA.from_json(it)), lambda: KeyError('missing JSON key: tomoVirRad')),
            none_raise(optional_map(json.get('tomoVirBinn', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: tomoVirBinn')),
            none_raise(optional_map(json.get('tomoVirDetectMethod', None), lambda it: TomoVirDetectMethod.from_json(it)), lambda: KeyError('missing JSON key: tomoVirDetectMethod')),
            none_raise(optional_map(json.get('tomoSpkMethod', None), lambda it: TomoSpkMethod.from_json(it)), lambda: KeyError('missing JSON key: tomoSpkMethod')),
            none_raise(optional_map(json.get('tomoSpkRad', None), lambda it: ValueA.from_json(it)), lambda: KeyError('missing JSON key: tomoSpkRad')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionStatus:
        return RealTimeS2CSessionStatus.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'daemons_running={self.daemons_running}',
            f'jobs_running={self.jobs_running}',
            f'tomo_vir_method={self.tomo_vir_method}',
            f'tomo_vir_rad={self.tomo_vir_rad}',
            f'tomo_vir_binn={self.tomo_vir_binn}',
            f'tomo_vir_detect_method={self.tomo_vir_detect_method}',
            f'tomo_spk_method={self.tomo_spk_method}',
            f'tomo_spk_rad={self.tomo_spk_rad}',
        ])
        return f'RealTimeS2CSessionStatus[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RealTimeS2CSessionStatus):
            return NotImplemented
        return self.daemons_running == other.daemons_running \
            and self.jobs_running == other.jobs_running \
            and self.tomo_vir_method == other.tomo_vir_method \
            and self.tomo_vir_rad == other.tomo_vir_rad \
            and self.tomo_vir_binn == other.tomo_vir_binn \
            and self.tomo_vir_detect_method == other.tomo_vir_detect_method \
            and self.tomo_spk_method == other.tomo_spk_method \
            and self.tomo_spk_rad == other.tomo_spk_rad


class RealTimeS2CSessionSmallData:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionSmallData'
    
    def __init__(self, exports: List[SessionExportData]) -> None:
        self.exports: List[SessionExportData] = exports
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'exports': [x.to_json() for x in self.exports],
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionSmallData:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('exports', None), lambda it: [SessionExportData.from_json(x) for x in cast(List[Any], it)]), lambda: KeyError('missing JSON key: exports')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionSmallData:
        return RealTimeS2CSessionSmallData.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'exports={self.exports}',
        ])
        return f'RealTimeS2CSessionSmallData[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RealTimeS2CSessionSmallData):
            return NotImplemented
        return self.exports == other.exports


class RealTimeS2CSessionLargeData:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionLargeData'
    
    def __init__(self, auto_virions_count: int, auto_particles_count: int, micrographs: List[MicrographMetadata], tilt_serieses: List[TiltSeriesData], two_dclasses: List[TwoDClassesData]) -> None:
        self.auto_virions_count: int = auto_virions_count
        """
        (no description yet)
        """
        self.auto_particles_count: int = auto_particles_count
        """
        (no description yet)
        """
        self.micrographs: List[MicrographMetadata] = micrographs
        """
        (no description yet)
        """
        self.tilt_serieses: List[TiltSeriesData] = tilt_serieses
        """
        (no description yet)
        """
        self.two_dclasses: List[TwoDClassesData] = two_dclasses
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'autoVirionsCount': self.auto_virions_count,
            'autoParticlesCount': self.auto_particles_count,
            'micrographs': [x.to_json() for x in self.micrographs],
            'tiltSerieses': [x.to_json() for x in self.tilt_serieses],
            'twoDClasses': [x.to_json() for x in self.two_dclasses],
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionLargeData:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_map(optional_map(json.get('autoVirionsCount', None), lambda it: cast(int, it)), lambda: 0),
            none_map(optional_map(json.get('autoParticlesCount', None), lambda it: cast(int, it)), lambda: 0),
            none_raise(optional_map(json.get('micrographs', None), lambda it: [MicrographMetadata.from_json(x) for x in cast(List[Any], it)]), lambda: KeyError('missing JSON key: micrographs')),
            none_raise(optional_map(json.get('tiltSerieses', None), lambda it: [TiltSeriesData.from_json(x) for x in cast(List[Any], it)]), lambda: KeyError('missing JSON key: tiltSerieses')),
            none_raise(optional_map(json.get('twoDClasses', None), lambda it: [TwoDClassesData.from_json(x) for x in cast(List[Any], it)]), lambda: KeyError('missing JSON key: twoDClasses')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionLargeData:
        return RealTimeS2CSessionLargeData.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'auto_virions_count={self.auto_virions_count}',
            f'auto_particles_count={self.auto_particles_count}',
            f'micrographs={self.micrographs}',
            f'tilt_serieses={self.tilt_serieses}',
            f'two_dclasses={self.two_dclasses}',
        ])
        return f'RealTimeS2CSessionLargeData[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RealTimeS2CSessionLargeData):
            return NotImplemented
        return self.auto_virions_count == other.auto_virions_count \
            and self.auto_particles_count == other.auto_particles_count \
            and self.micrographs == other.micrographs \
            and self.tilt_serieses == other.tilt_serieses \
            and self.two_dclasses == other.two_dclasses


class RealTimeS2CSessionRunningJob:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionRunningJob'
    
    def __init__(self, job_id: str, name: str, size: int, status: RunStatus) -> None:
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
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionRunningJob:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('jobId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: jobId')),
            none_raise(optional_map(json.get('name', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: name')),
            none_raise(optional_map(json.get('size', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: size')),
            none_raise(optional_map(json.get('status', None), lambda it: RunStatus.from_json(it)), lambda: KeyError('missing JSON key: status')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionRunningJob:
        return RealTimeS2CSessionRunningJob.from_json(json.loads(serialized), type_ids)
    
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


class RealTimeS2CSessionDaemonSubmitted:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionDaemonSubmitted'
    
    def __init__(self, job_id: str, daemon: SessionDaemon) -> None:
        self.job_id: str = job_id
        """
        (no description yet)
        """
        self.daemon: SessionDaemon = daemon
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'jobId': self.job_id,
            'daemon': self.daemon.to_json(),
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionDaemonSubmitted:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('jobId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: jobId')),
            none_raise(optional_map(json.get('daemon', None), lambda it: SessionDaemon.from_json(it)), lambda: KeyError('missing JSON key: daemon')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionDaemonSubmitted:
        return RealTimeS2CSessionDaemonSubmitted.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'job_id={self.job_id}',
            f'daemon={self.daemon}',
        ])
        return f'RealTimeS2CSessionDaemonSubmitted[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RealTimeS2CSessionDaemonSubmitted):
            return NotImplemented
        return self.job_id == other.job_id \
            and self.daemon == other.daemon


class RealTimeS2CSessionDaemonStarted:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionDaemonStarted'
    
    def __init__(self, job_id: str, daemon: SessionDaemon) -> None:
        self.job_id: str = job_id
        """
        (no description yet)
        """
        self.daemon: SessionDaemon = daemon
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'jobId': self.job_id,
            'daemon': self.daemon.to_json(),
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionDaemonStarted:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('jobId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: jobId')),
            none_raise(optional_map(json.get('daemon', None), lambda it: SessionDaemon.from_json(it)), lambda: KeyError('missing JSON key: daemon')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionDaemonStarted:
        return RealTimeS2CSessionDaemonStarted.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'job_id={self.job_id}',
            f'daemon={self.daemon}',
        ])
        return f'RealTimeS2CSessionDaemonStarted[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RealTimeS2CSessionDaemonStarted):
            return NotImplemented
        return self.job_id == other.job_id \
            and self.daemon == other.daemon


class RealTimeS2CSessionDaemonFinished:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionDaemonFinished'
    
    def __init__(self, job_id: str, daemon: SessionDaemon) -> None:
        self.job_id: str = job_id
        """
        (no description yet)
        """
        self.daemon: SessionDaemon = daemon
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'jobId': self.job_id,
            'daemon': self.daemon.to_json(),
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionDaemonFinished:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('jobId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: jobId')),
            none_raise(optional_map(json.get('daemon', None), lambda it: SessionDaemon.from_json(it)), lambda: KeyError('missing JSON key: daemon')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionDaemonFinished:
        return RealTimeS2CSessionDaemonFinished.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'job_id={self.job_id}',
            f'daemon={self.daemon}',
        ])
        return f'RealTimeS2CSessionDaemonFinished[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RealTimeS2CSessionDaemonFinished):
            return NotImplemented
        return self.job_id == other.job_id \
            and self.daemon == other.daemon


class RealTimeS2CSessionJobSubmitted:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionJobSubmitted'
    
    def __init__(self, job_id: str, name: str, size: int) -> None:
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
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'jobId': self.job_id,
            'name': self.name,
            'size': self.size,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionJobSubmitted:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('jobId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: jobId')),
            none_raise(optional_map(json.get('name', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: name')),
            none_raise(optional_map(json.get('size', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: size')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionJobSubmitted:
        return RealTimeS2CSessionJobSubmitted.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'job_id={self.job_id}',
            f'name={self.name}',
            f'size={self.size}',
        ])
        return f'RealTimeS2CSessionJobSubmitted[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RealTimeS2CSessionJobSubmitted):
            return NotImplemented
        return self.job_id == other.job_id \
            and self.name == other.name \
            and self.size == other.size


class RealTimeS2CSessionJobStarted:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionJobStarted'
    
    def __init__(self, job_id: str) -> None:
        self.job_id: str = job_id
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'jobId': self.job_id,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionJobStarted:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('jobId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: jobId')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionJobStarted:
        return RealTimeS2CSessionJobStarted.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'job_id={self.job_id}',
        ])
        return f'RealTimeS2CSessionJobStarted[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RealTimeS2CSessionJobStarted):
            return NotImplemented
        return self.job_id == other.job_id


class RealTimeS2CSessionJobFinished:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionJobFinished'
    
    def __init__(self, job_id: str, result_type: ClusterJobResultType) -> None:
        self.job_id: str = job_id
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
            'jobId': self.job_id,
            'resultType': self.result_type.to_json(),
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionJobFinished:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('jobId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: jobId')),
            none_raise(optional_map(json.get('resultType', None), lambda it: ClusterJobResultType.from_json(it)), lambda: KeyError('missing JSON key: resultType')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionJobFinished:
        return RealTimeS2CSessionJobFinished.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'job_id={self.job_id}',
            f'result_type={self.result_type}',
        ])
        return f'RealTimeS2CSessionJobFinished[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RealTimeS2CSessionJobFinished):
            return NotImplemented
        return self.job_id == other.job_id \
            and self.result_type == other.result_type


class RealTimeS2CSessionFilesystem:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionFilesystem'
    
    def __init__(self, path: str, type: str, bytes: int, bytes_used: int) -> None:
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
            'path': self.path,
            'type': self.type,
            'bytes': self.bytes,
            'bytesUsed': self.bytes_used,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionFilesystem:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('path', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: path')),
            none_raise(optional_map(json.get('type', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: type')),
            none_raise(optional_map(json.get('bytes', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: bytes')),
            none_raise(optional_map(json.get('bytesUsed', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: bytesUsed')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionFilesystem:
        return RealTimeS2CSessionFilesystem.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
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
        return self.path == other.path \
            and self.type == other.type \
            and self.bytes == other.bytes \
            and self.bytes_used == other.bytes_used


class RealTimeS2CSessionFilesystems:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionFilesystems'
    
    def __init__(self, filesystems: List[RealTimeS2CSessionFilesystem]) -> None:
        self.filesystems: List[RealTimeS2CSessionFilesystem] = filesystems
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'filesystems': [x.to_json() for x in self.filesystems],
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionFilesystems:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('filesystems', None), lambda it: [RealTimeS2CSessionFilesystem.from_json(x) for x in cast(List[Any], it)]), lambda: KeyError('missing JSON key: filesystems')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionFilesystems:
        return RealTimeS2CSessionFilesystems.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'filesystems={self.filesystems}',
        ])
        return f'RealTimeS2CSessionFilesystems[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RealTimeS2CSessionFilesystems):
            return NotImplemented
        return self.filesystems == other.filesystems


class RealTimeS2CSessionTransferInit:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionTransferInit'
    
    def __init__(self, files: List[RealTimeS2CSessionTransferInitFileInfo]) -> None:
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
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionTransferInit:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('files', None), lambda it: [RealTimeS2CSessionTransferInitFileInfo.from_json(x) for x in cast(List[Any], it)]), lambda: KeyError('missing JSON key: files')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionTransferInit:
        return RealTimeS2CSessionTransferInit.from_json(json.loads(serialized), type_ids)
    
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
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionTransferInit.FileInfo'
    
    def __init__(self, filename: str, bytes_total: int, bytes_transfered: int) -> None:
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
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionTransferInitFileInfo:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('filename', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: filename')),
            none_raise(optional_map(json.get('bytesTotal', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: bytesTotal')),
            none_raise(optional_map(json.get('bytesTransfered', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: bytesTransfered')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionTransferInitFileInfo:
        return RealTimeS2CSessionTransferInitFileInfo.from_json(json.loads(serialized), type_ids)
    
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


class RealTimeS2CSessionTransferWaiting:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionTransferWaiting'
    
    def __init__(self, filename: str) -> None:
        self.filename: str = filename
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'filename': self.filename,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionTransferWaiting:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('filename', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: filename')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionTransferWaiting:
        return RealTimeS2CSessionTransferWaiting.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'filename={self.filename}',
        ])
        return f'RealTimeS2CSessionTransferWaiting[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RealTimeS2CSessionTransferWaiting):
            return NotImplemented
        return self.filename == other.filename


class RealTimeS2CSessionTransferStarted:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionTransferStarted'
    
    def __init__(self, filename: str, bytes_total: int) -> None:
        self.filename: str = filename
        """
        (no description yet)
        """
        self.bytes_total: int = bytes_total
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
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionTransferStarted:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('filename', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: filename')),
            none_raise(optional_map(json.get('bytesTotal', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: bytesTotal')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionTransferStarted:
        return RealTimeS2CSessionTransferStarted.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'filename={self.filename}',
            f'bytes_total={self.bytes_total}',
        ])
        return f'RealTimeS2CSessionTransferStarted[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RealTimeS2CSessionTransferStarted):
            return NotImplemented
        return self.filename == other.filename \
            and self.bytes_total == other.bytes_total


class RealTimeS2CSessionTransferProgress:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionTransferProgress'
    
    def __init__(self, filename: str, bytes_transferred: int) -> None:
        self.filename: str = filename
        """
        (no description yet)
        """
        self.bytes_transferred: int = bytes_transferred
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'filename': self.filename,
            'bytesTransferred': self.bytes_transferred,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionTransferProgress:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('filename', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: filename')),
            none_raise(optional_map(json.get('bytesTransferred', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: bytesTransferred')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionTransferProgress:
        return RealTimeS2CSessionTransferProgress.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'filename={self.filename}',
            f'bytes_transferred={self.bytes_transferred}',
        ])
        return f'RealTimeS2CSessionTransferProgress[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RealTimeS2CSessionTransferProgress):
            return NotImplemented
        return self.filename == other.filename \
            and self.bytes_transferred == other.bytes_transferred


class RealTimeS2CSessionTransferFinished:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionTransferFinished'
    
    def __init__(self, filename: str) -> None:
        self.filename: str = filename
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'filename': self.filename,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionTransferFinished:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('filename', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: filename')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionTransferFinished:
        return RealTimeS2CSessionTransferFinished.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'filename={self.filename}',
        ])
        return f'RealTimeS2CSessionTransferFinished[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RealTimeS2CSessionTransferFinished):
            return NotImplemented
        return self.filename == other.filename


class RealTimeS2CSessionMicrograph:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionMicrograph'
    
    def __init__(self, micrograph: MicrographMetadata) -> None:
        self.micrograph: MicrographMetadata = micrograph
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'micrograph': self.micrograph.to_json(),
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionMicrograph:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('micrograph', None), lambda it: MicrographMetadata.from_json(it)), lambda: KeyError('missing JSON key: micrograph')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionMicrograph:
        return RealTimeS2CSessionMicrograph.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'micrograph={self.micrograph}',
        ])
        return f'RealTimeS2CSessionMicrograph[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RealTimeS2CSessionMicrograph):
            return NotImplemented
        return self.micrograph == other.micrograph


class RealTimeS2CSessionTiltSeries:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionTiltSeries'
    
    def __init__(self, tilt_series: TiltSeriesData) -> None:
        self.tilt_series: TiltSeriesData = tilt_series
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'tiltSeries': self.tilt_series.to_json(),
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionTiltSeries:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('tiltSeries', None), lambda it: TiltSeriesData.from_json(it)), lambda: KeyError('missing JSON key: tiltSeries')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionTiltSeries:
        return RealTimeS2CSessionTiltSeries.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'tilt_series={self.tilt_series}',
        ])
        return f'RealTimeS2CSessionTiltSeries[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RealTimeS2CSessionTiltSeries):
            return NotImplemented
        return self.tilt_series == other.tilt_series


class RealTimeS2CSessionTwoDClasses:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionTwoDClasses'
    
    def __init__(self, two_dclasses: TwoDClassesData) -> None:
        self.two_dclasses: TwoDClassesData = two_dclasses
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'twoDClasses': self.two_dclasses.to_json(),
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionTwoDClasses:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('twoDClasses', None), lambda it: TwoDClassesData.from_json(it)), lambda: KeyError('missing JSON key: twoDClasses')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionTwoDClasses:
        return RealTimeS2CSessionTwoDClasses.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'two_dclasses={self.two_dclasses}',
        ])
        return f'RealTimeS2CSessionTwoDClasses[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RealTimeS2CSessionTwoDClasses):
            return NotImplemented
        return self.two_dclasses == other.two_dclasses


class RealTimeS2CSessionExport:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RealTimeS2C.SessionExport'
    
    def __init__(self, export: SessionExportData) -> None:
        self.export: SessionExportData = export
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'export': self.export.to_json(),
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionExport:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('export', None), lambda it: SessionExportData.from_json(it)), lambda: KeyError('missing JSON key: export')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RealTimeS2CSessionExport:
        return RealTimeS2CSessionExport.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'export={self.export}',
        ])
        return f'RealTimeS2CSessionExport[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RealTimeS2CSessionExport):
            return NotImplemented
        return self.export == other.export


class SingleParticleSessionArgs:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.SingleParticleSessionArgs'
    
    def __init__(self, name: str, path: str, group_id: str, values: ArgValuesToml) -> None:
        self.name: str = name
        """
        (no description yet)
        """
        self.path: str = path
        """
        (no description yet)
        """
        self.group_id: str = group_id
        """
        (no description yet)
        """
        self.values: ArgValuesToml = values
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'name': self.name,
            'path': self.path,
            'groupId': self.group_id,
            'values': self.values,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> SingleParticleSessionArgs:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('name', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: name')),
            none_raise(optional_map(json.get('path', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: path')),
            none_raise(optional_map(json.get('groupId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: groupId')),
            none_raise(optional_map(json.get('values', None), lambda it: cast(ArgValuesToml, it)), lambda: KeyError('missing JSON key: values')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> SingleParticleSessionArgs:
        return SingleParticleSessionArgs.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'name={self.name}',
            f'path={self.path}',
            f'group_id={self.group_id}',
            f'values={self.values}',
        ])
        return f'SingleParticleSessionArgs[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, SingleParticleSessionArgs):
            return NotImplemented
        return self.name == other.name \
            and self.path == other.path \
            and self.group_id == other.group_id \
            and self.values == other.values


class SingleParticleSessionData:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.SingleParticleSessionData'
    
    def __init__(self, user_id: str, session_id: str, session_number: Optional[int], created: int, permissions: Set[SessionPermission], path: str, args: JobArgs[SingleParticleSessionArgs], display: JobArgs[SingleParticleSessionDisplay], num_micrographs: int, num_frames: int) -> None:
        self.user_id: str = user_id
        """
        (no description yet)
        """
        self.session_id: str = session_id
        """
        (no description yet)
        """
        self.session_number: Optional[int] = session_number
        """
        (no description yet)
        """
        self.created: int = created
        """
        (no description yet)
        """
        self.permissions: Set[SessionPermission] = permissions
        """
        (no description yet)
        """
        self.path: str = path
        """
        (no description yet)
        """
        self.args: JobArgs[SingleParticleSessionArgs] = args
        """
        (no description yet)
        """
        self.display: JobArgs[SingleParticleSessionDisplay] = display
        """
        (no description yet)
        """
        self.num_micrographs: int = num_micrographs
        """
        (no description yet)
        """
        self.num_frames: int = num_frames
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'userId': self.user_id,
            'sessionId': self.session_id,
            'sessionNumber': self.session_number if self.session_number is not None else None,
            'created': self.created,
            'permissions': [x.to_json() for x in self.permissions],
            'path': self.path,
            'args': self.args.to_json(),
            'display': self.display.to_json(),
            'numMicrographs': self.num_micrographs,
            'numFrames': self.num_frames,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> SingleParticleSessionData:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('userId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: userId')),
            none_raise(optional_map(json.get('sessionId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: sessionId')),
            optional_map(json.get('sessionNumber', None), lambda it: cast(int, it)),
            none_raise(optional_map(json.get('created', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: created')),
            none_raise(optional_map(json.get('permissions', None), lambda it: {SessionPermission.from_json(x) for x in cast(Set[Any], it)}), lambda: KeyError('missing JSON key: permissions')),
            none_raise(optional_map(json.get('path', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: path')),
            none_raise(optional_map(json.get('args', None), lambda it: JobArgs.from_json(it, type_ids={'T': 'edu.duke.bartesaghi.micromon.services/SingleParticleSessionArgs'})), lambda: KeyError('missing JSON key: args')),
            none_raise(optional_map(json.get('display', None), lambda it: JobArgs.from_json(it, type_ids={'T': 'edu.duke.bartesaghi.micromon.services/SingleParticleSessionDisplay'})), lambda: KeyError('missing JSON key: display')),
            none_raise(optional_map(json.get('numMicrographs', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: numMicrographs')),
            none_raise(optional_map(json.get('numFrames', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: numFrames')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> SingleParticleSessionData:
        return SingleParticleSessionData.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'user_id={self.user_id}',
            f'session_id={self.session_id}',
            f'session_number={self.session_number}',
            f'created={self.created}',
            f'permissions={self.permissions}',
            f'path={self.path}',
            f'args={self.args}',
            f'display={self.display}',
            f'num_micrographs={self.num_micrographs}',
            f'num_frames={self.num_frames}',
        ])
        return f'SingleParticleSessionData[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, SingleParticleSessionData):
            return NotImplemented
        return self.user_id == other.user_id \
            and self.session_id == other.session_id \
            and self.session_number == other.session_number \
            and self.created == other.created \
            and self.permissions == other.permissions \
            and self.path == other.path \
            and self.args == other.args \
            and self.display == other.display \
            and self.num_micrographs == other.num_micrographs \
            and self.num_frames == other.num_frames


class TomographySessionArgs:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.TomographySessionArgs'
    
    def __init__(self, name: str, path: str, group_id: str, values: ArgValuesToml) -> None:
        self.name: str = name
        """
        (no description yet)
        """
        self.path: str = path
        """
        (no description yet)
        """
        self.group_id: str = group_id
        """
        (no description yet)
        """
        self.values: ArgValuesToml = values
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'name': self.name,
            'path': self.path,
            'groupId': self.group_id,
            'values': self.values,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> TomographySessionArgs:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('name', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: name')),
            none_raise(optional_map(json.get('path', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: path')),
            none_raise(optional_map(json.get('groupId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: groupId')),
            none_raise(optional_map(json.get('values', None), lambda it: cast(ArgValuesToml, it)), lambda: KeyError('missing JSON key: values')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> TomographySessionArgs:
        return TomographySessionArgs.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'name={self.name}',
            f'path={self.path}',
            f'group_id={self.group_id}',
            f'values={self.values}',
        ])
        return f'TomographySessionArgs[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, TomographySessionArgs):
            return NotImplemented
        return self.name == other.name \
            and self.path == other.path \
            and self.group_id == other.group_id \
            and self.values == other.values


class TomographySessionData:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.TomographySessionData'
    
    def __init__(self, user_id: str, session_id: str, session_number: Optional[int], created: int, permissions: Set[SessionPermission], path: str, args: JobArgs[TomographySessionArgs], display: JobArgs[TomographySessionDisplay], num_tilt_series: int, num_tilts: int) -> None:
        self.user_id: str = user_id
        """
        (no description yet)
        """
        self.session_id: str = session_id
        """
        (no description yet)
        """
        self.session_number: Optional[int] = session_number
        """
        (no description yet)
        """
        self.created: int = created
        """
        (no description yet)
        """
        self.permissions: Set[SessionPermission] = permissions
        """
        (no description yet)
        """
        self.path: str = path
        """
        (no description yet)
        """
        self.args: JobArgs[TomographySessionArgs] = args
        """
        (no description yet)
        """
        self.display: JobArgs[TomographySessionDisplay] = display
        """
        (no description yet)
        """
        self.num_tilt_series: int = num_tilt_series
        """
        (no description yet)
        """
        self.num_tilts: int = num_tilts
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'userId': self.user_id,
            'sessionId': self.session_id,
            'sessionNumber': self.session_number if self.session_number is not None else None,
            'created': self.created,
            'permissions': [x.to_json() for x in self.permissions],
            'path': self.path,
            'args': self.args.to_json(),
            'display': self.display.to_json(),
            'numTiltSeries': self.num_tilt_series,
            'numTilts': self.num_tilts,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> TomographySessionData:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('userId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: userId')),
            none_raise(optional_map(json.get('sessionId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: sessionId')),
            optional_map(json.get('sessionNumber', None), lambda it: cast(int, it)),
            none_raise(optional_map(json.get('created', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: created')),
            none_raise(optional_map(json.get('permissions', None), lambda it: {SessionPermission.from_json(x) for x in cast(Set[Any], it)}), lambda: KeyError('missing JSON key: permissions')),
            none_raise(optional_map(json.get('path', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: path')),
            none_raise(optional_map(json.get('args', None), lambda it: JobArgs.from_json(it, type_ids={'T': 'edu.duke.bartesaghi.micromon.services/TomographySessionArgs'})), lambda: KeyError('missing JSON key: args')),
            none_raise(optional_map(json.get('display', None), lambda it: JobArgs.from_json(it, type_ids={'T': 'edu.duke.bartesaghi.micromon.services/TomographySessionDisplay'})), lambda: KeyError('missing JSON key: display')),
            none_raise(optional_map(json.get('numTiltSeries', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: numTiltSeries')),
            none_raise(optional_map(json.get('numTilts', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: numTilts')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> TomographySessionData:
        return TomographySessionData.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'user_id={self.user_id}',
            f'session_id={self.session_id}',
            f'session_number={self.session_number}',
            f'created={self.created}',
            f'permissions={self.permissions}',
            f'path={self.path}',
            f'args={self.args}',
            f'display={self.display}',
            f'num_tilt_series={self.num_tilt_series}',
            f'num_tilts={self.num_tilts}',
        ])
        return f'TomographySessionData[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, TomographySessionData):
            return NotImplemented
        return self.user_id == other.user_id \
            and self.session_id == other.session_id \
            and self.session_number == other.session_number \
            and self.created == other.created \
            and self.permissions == other.permissions \
            and self.path == other.path \
            and self.args == other.args \
            and self.display == other.display \
            and self.num_tilt_series == other.num_tilt_series \
            and self.num_tilts == other.num_tilts


class SessionDaemon:
    """
    (no description yet)
    """
    
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


class RunningSessions:
    """
    because polymorphic serialization in KVision is too much of a pain
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RunningSessions'
    
    def __init__(self, single_particle: List[SingleParticleSessionData], tomography: List[TomographySessionData]) -> None:
        self.single_particle: List[SingleParticleSessionData] = single_particle
        """
        (no description yet)
        """
        self.tomography: List[TomographySessionData] = tomography
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'singleParticle': [x.to_json() for x in self.single_particle],
            'tomography': [x.to_json() for x in self.tomography],
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RunningSessions:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('singleParticle', None), lambda it: [SingleParticleSessionData.from_json(x) for x in cast(List[Any], it)]), lambda: KeyError('missing JSON key: singleParticle')),
            none_raise(optional_map(json.get('tomography', None), lambda it: [TomographySessionData.from_json(x) for x in cast(List[Any], it)]), lambda: KeyError('missing JSON key: tomography')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RunningSessions:
        return RunningSessions.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'single_particle={self.single_particle}',
            f'tomography={self.tomography}',
        ])
        return f'RunningSessions[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, RunningSessions):
            return NotImplemented
        return self.single_particle == other.single_particle \
            and self.tomography == other.tomography


class SessionLogs:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.SessionLogs'
    
    def __init__(self, logs: List[SessionLogData]) -> None:
        self.logs: List[SessionLogData] = logs
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'logs': [x.to_json() for x in self.logs],
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> SessionLogs:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('logs', None), lambda it: [SessionLogData.from_json(x) for x in cast(List[Any], it)]), lambda: KeyError('missing JSON key: logs')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> SessionLogs:
        return SessionLogs.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'logs={self.logs}',
        ])
        return f'SessionLogs[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, SessionLogs):
            return NotImplemented
        return self.logs == other.logs


class SessionSpeeds:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.SessionSpeeds'
    
    def __init__(self, transfers: List[float]) -> None:
        self.transfers: List[float] = transfers
        """
        for file transfers, in Gbps
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'transfers': [x for x in self.transfers],
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> SessionSpeeds:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('transfers', None), lambda it: [cast(float, x) for x in cast(List[Any], it)]), lambda: KeyError('missing JSON key: transfers')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> SessionSpeeds:
        return SessionSpeeds.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'transfers={self.transfers}',
        ])
        return f'SessionSpeeds[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, SessionSpeeds):
            return NotImplemented
        return self.transfers == other.transfers


class SessionJobsLogs:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.SessionJobsLogs'
    
    def __init__(self, jobs: List[SessionJobLogData]) -> None:
        self.jobs: List[SessionJobLogData] = jobs
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'jobs': [x.to_json() for x in self.jobs],
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> SessionJobsLogs:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('jobs', None), lambda it: [SessionJobLogData.from_json(x) for x in cast(List[Any], it)]), lambda: KeyError('missing JSON key: jobs')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> SessionJobsLogs:
        return SessionJobsLogs.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'jobs={self.jobs}',
        ])
        return f'SessionJobsLogs[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, SessionJobsLogs):
            return NotImplemented
        return self.jobs == other.jobs


class SessionExportRequest:
    """
    WARNING: be very careful changing these classes! They get saved in the sessionExports database in serialized form, so deserializing old data could cause problems depending on how backwards compatible kotlinx.serialization is. Making changes here may require database migrations.
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.SessionExportRequest'
    @abstractmethod
    def to_json(self) -> Dict[str,Any]:
        pass
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> SessionExportRequest:
        """
        Creates a new class instance from JSON
        """
        
        cls_type = json['type']
        if cls_type == 'edu.duke.bartesaghi.micromon.services.SessionExportRequest.Filter':
            return SessionExportRequestFilter.from_json(json)
        else:
            raise Exception(f'unrecognized polymorphic subtype {cls_type} for supertype SessionExportRequest')
    @abstractmethod
    def serialize(self) -> str:
        pass
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> SessionExportRequest:
        return SessionExportRequest.from_json(json.loads(serialized), type_ids)


class SessionExportRequestFilter(SessionExportRequest, metaclass=ABCMeta):
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.SessionExportRequest.Filter'
    
    def __init__(self, name: str) -> None:
        self.name: str = name
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'type': 'edu.duke.bartesaghi.micromon.services.SessionExportRequest.Filter',
            'name': self.name,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> SessionExportRequestFilter:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('name', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: name')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> SessionExportRequestFilter:
        return SessionExportRequestFilter.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'name={self.name}',
        ])
        return f'SessionExportRequestFilter[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, SessionExportRequestFilter):
            return NotImplemented
        return self.name == other.name


class AvgRotData:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.AvgRotData'
    
    def __init__(self, spatial_freq: List[float], avg_rot: List[float], ctf_fit: List[float], cross_correlation: List[float], min_res: float) -> None:
        self.spatial_freq: List[float] = spatial_freq
        """
        (no description yet)
        """
        self.avg_rot: List[float] = avg_rot
        """
        (no description yet)
        """
        self.ctf_fit: List[float] = ctf_fit
        """
        (no description yet)
        """
        self.cross_correlation: List[float] = cross_correlation
        """
        (no description yet)
        """
        self.min_res: float = min_res
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'spatialFreq': [x for x in self.spatial_freq],
            'avgRot': [x for x in self.avg_rot],
            'ctfFit': [x for x in self.ctf_fit],
            'crossCorrelation': [x for x in self.cross_correlation],
            'minRes': self.min_res,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> AvgRotData:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('spatialFreq', None), lambda it: [cast(float, x) for x in cast(List[Any], it)]), lambda: KeyError('missing JSON key: spatialFreq')),
            none_raise(optional_map(json.get('avgRot', None), lambda it: [cast(float, x) for x in cast(List[Any], it)]), lambda: KeyError('missing JSON key: avgRot')),
            none_raise(optional_map(json.get('ctfFit', None), lambda it: [cast(float, x) for x in cast(List[Any], it)]), lambda: KeyError('missing JSON key: ctfFit')),
            none_raise(optional_map(json.get('crossCorrelation', None), lambda it: [cast(float, x) for x in cast(List[Any], it)]), lambda: KeyError('missing JSON key: crossCorrelation')),
            none_raise(optional_map(json.get('minRes', None), lambda it: cast(float, it)), lambda: KeyError('missing JSON key: minRes')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> AvgRotData:
        return AvgRotData.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'spatial_freq={self.spatial_freq}',
            f'avg_rot={self.avg_rot}',
            f'ctf_fit={self.ctf_fit}',
            f'cross_correlation={self.cross_correlation}',
            f'min_res={self.min_res}',
        ])
        return f'AvgRotData[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, AvgRotData):
            return NotImplemented
        return self.spatial_freq == other.spatial_freq \
            and self.avg_rot == other.avg_rot \
            and self.ctf_fit == other.ctf_fit \
            and self.cross_correlation == other.cross_correlation \
            and self.min_res == other.min_res


class MotionData:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.MotionData'
    
    def __init__(self, x: List[float], y: List[float]) -> None:
        self.x: List[float] = x
        """
        (no description yet)
        """
        self.y: List[float] = y
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'x': [x for x in self.x],
            'y': [x for x in self.y],
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> MotionData:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('x', None), lambda it: [cast(float, x) for x in cast(List[Any], it)]), lambda: KeyError('missing JSON key: x')),
            none_raise(optional_map(json.get('y', None), lambda it: [cast(float, x) for x in cast(List[Any], it)]), lambda: KeyError('missing JSON key: y')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> MotionData:
        return MotionData.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'x={self.x}',
            f'y={self.y}',
        ])
        return f'MotionData[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, MotionData):
            return NotImplemented
        return self.x == other.x \
            and self.y == other.y


class DriftMetadata:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.DriftMetadata'
    
    def __init__(self, tilts: List[float], drifts: List[List[DriftXY]], ctf_values: List[CtfTiltValues], ctf_profiles: List[AvgRotData], tilt_axis_angle: float) -> None:
        self.tilts: List[float] = tilts
        """
        (no description yet)
        """
        self.drifts: List[List[DriftXY]] = drifts
        """
        (no description yet)
        """
        self.ctf_values: List[CtfTiltValues] = ctf_values
        """
        (no description yet)
        """
        self.ctf_profiles: List[AvgRotData] = ctf_profiles
        """
        (no description yet)
        """
        self.tilt_axis_angle: float = tilt_axis_angle
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'tilts': [x for x in self.tilts],
            'drifts': [[x.to_json() for x in x] for x in self.drifts],
            'ctfValues': [x.to_json() for x in self.ctf_values],
            'ctfProfiles': [x.to_json() for x in self.ctf_profiles],
            'tiltAxisAngle': self.tilt_axis_angle,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> DriftMetadata:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('tilts', None), lambda it: [cast(float, x) for x in cast(List[Any], it)]), lambda: KeyError('missing JSON key: tilts')),
            none_raise(optional_map(json.get('drifts', None), lambda it: [[DriftXY.from_json(x) for x in cast(List[Any], x)] for x in cast(List[Any], it)]), lambda: KeyError('missing JSON key: drifts')),
            none_raise(optional_map(json.get('ctfValues', None), lambda it: [CtfTiltValues.from_json(x) for x in cast(List[Any], it)]), lambda: KeyError('missing JSON key: ctfValues')),
            none_raise(optional_map(json.get('ctfProfiles', None), lambda it: [AvgRotData.from_json(x) for x in cast(List[Any], it)]), lambda: KeyError('missing JSON key: ctfProfiles')),
            none_raise(optional_map(json.get('tiltAxisAngle', None), lambda it: cast(float, it)), lambda: KeyError('missing JSON key: tiltAxisAngle')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> DriftMetadata:
        return DriftMetadata.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'tilts={self.tilts}',
            f'drifts={self.drifts}',
            f'ctf_values={self.ctf_values}',
            f'ctf_profiles={self.ctf_profiles}',
            f'tilt_axis_angle={self.tilt_axis_angle}',
        ])
        return f'DriftMetadata[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, DriftMetadata):
            return NotImplemented
        return self.tilts == other.tilts \
            and self.drifts == other.drifts \
            and self.ctf_values == other.ctf_values \
            and self.ctf_profiles == other.ctf_profiles \
            and self.tilt_axis_angle == other.tilt_axis_angle


class Block:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.pyp.Block'
    
    def __init__(self, block_id: str, name: str, description: str, group_ids: List[str]) -> None:
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
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> Block:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('blockId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: blockId')),
            none_raise(optional_map(json.get('name', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: name')),
            none_raise(optional_map(json.get('description', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: description')),
            none_raise(optional_map(json.get('groupIds', None), lambda it: [cast(str, x) for x in cast(List[Any], it)]), lambda: KeyError('missing JSON key: groupIds')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> Block:
        return Block.from_json(json.loads(serialized), type_ids)
    
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


class ValueA:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.pyp.ValueA'
    
    def __init__(self, v: float) -> None:
        self.v: float = v
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'v': self.v,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> ValueA:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('v', None), lambda it: cast(float, it)), lambda: KeyError('missing JSON key: v')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> ValueA:
        return ValueA.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'v={self.v}',
        ])
        return f'ValueA[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, ValueA):
            return NotImplemented
        return self.v == other.v


class TomoVirMethod:
    """
    (no description yet)
    """
    
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
        
        if name == 'PYPEval':
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
        return 5
    
    def __iter__(self) -> Iterator[TomoVirMethod]:
        return [TomoVirMethod.PYPEval, TomoVirMethod.PYPTrain, TomoVirMethod.Manual, TomoVirMethod.Auto, TomoVirMethod.NoneVal].__iter__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, TomoVirMethod):
            return NotImplemented
        return self.name == other.name
    
    def __hash__(self) -> int:
        return hash(self.name)

TomoVirMethod.PYPEval = TomoVirMethod('PYPEval')
TomoVirMethod.PYPTrain = TomoVirMethod('PYPTrain')
TomoVirMethod.Manual = TomoVirMethod('Manual')
TomoVirMethod.Auto = TomoVirMethod('Auto')
TomoVirMethod.NoneVal = TomoVirMethod('None')


class TomoVirDetectMethod:
    """
    (no description yet)
    """
    
    Manual: TomoVirDetectMethod
    Auto: TomoVirDetectMethod
    NoneVal: TomoVirDetectMethod
    
    def __init__(self, name: str) -> None:
        self.name = name
    
    def to_json(self) -> str:
        """
        Converts this enum value into JSON
        """
        
        return self.name
    
    @classmethod
    def from_json(cls, name: str) -> TomoVirDetectMethod:
        """
        Reads this enum value from JSON
        """
        
        if name == 'Manual':
            return TomoVirDetectMethod.Manual
        elif name == 'Auto':
            return TomoVirDetectMethod.Auto
        elif name == 'None':
            return TomoVirDetectMethod.NoneVal
        else:
            return cls(name)
    
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __len__(self) -> int:
        return 3
    
    def __iter__(self) -> Iterator[TomoVirDetectMethod]:
        return [TomoVirDetectMethod.Manual, TomoVirDetectMethod.Auto, TomoVirDetectMethod.NoneVal].__iter__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, TomoVirDetectMethod):
            return NotImplemented
        return self.name == other.name
    
    def __hash__(self) -> int:
        return hash(self.name)

TomoVirDetectMethod.Manual = TomoVirDetectMethod('Manual')
TomoVirDetectMethod.Auto = TomoVirDetectMethod('Auto')
TomoVirDetectMethod.NoneVal = TomoVirDetectMethod('None')


class TomoSpkMethod:
    """
    (no description yet)
    """
    
    TopazEval: TomoSpkMethod
    TopazTrain: TomoSpkMethod
    PYPEval: TomoSpkMethod
    PYPTrain: TomoSpkMethod
    Manual: TomoSpkMethod
    Import: TomoSpkMethod
    Auto: TomoSpkMethod
    NoneVal: TomoSpkMethod
    
    def __init__(self, name: str) -> None:
        self.name = name
    
    def to_json(self) -> str:
        """
        Converts this enum value into JSON
        """
        
        return self.name
    
    @classmethod
    def from_json(cls, name: str) -> TomoSpkMethod:
        """
        Reads this enum value from JSON
        """
        
        if name == 'TopazEval':
            return TomoSpkMethod.TopazEval
        elif name == 'TopazTrain':
            return TomoSpkMethod.TopazTrain
        elif name == 'PYPEval':
            return TomoSpkMethod.PYPEval
        elif name == 'PYPTrain':
            return TomoSpkMethod.PYPTrain
        elif name == 'Manual':
            return TomoSpkMethod.Manual
        elif name == 'Import':
            return TomoSpkMethod.Import
        elif name == 'Auto':
            return TomoSpkMethod.Auto
        elif name == 'None':
            return TomoSpkMethod.NoneVal
        else:
            return cls(name)
    
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __len__(self) -> int:
        return 8
    
    def __iter__(self) -> Iterator[TomoSpkMethod]:
        return [TomoSpkMethod.TopazEval, TomoSpkMethod.TopazTrain, TomoSpkMethod.PYPEval, TomoSpkMethod.PYPTrain, TomoSpkMethod.Manual, TomoSpkMethod.Import, TomoSpkMethod.Auto, TomoSpkMethod.NoneVal].__iter__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, TomoSpkMethod):
            return NotImplemented
        return self.name == other.name
    
    def __hash__(self) -> int:
        return hash(self.name)

TomoSpkMethod.TopazEval = TomoSpkMethod('TopazEval')
TomoSpkMethod.TopazTrain = TomoSpkMethod('TopazTrain')
TomoSpkMethod.PYPEval = TomoSpkMethod('PYPEval')
TomoSpkMethod.PYPTrain = TomoSpkMethod('PYPTrain')
TomoSpkMethod.Manual = TomoSpkMethod('Manual')
TomoSpkMethod.Import = TomoSpkMethod('Import')
TomoSpkMethod.Auto = TomoSpkMethod('Auto')
TomoSpkMethod.NoneVal = TomoSpkMethod('None')


class AppPermissionData:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.AppPermissionData'
    
    def __init__(self, app_permission_id: str, description: Optional[str]) -> None:
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
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> AppPermissionData:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('appPermissionId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: appPermissionId')),
            optional_map(json.get('description', None), lambda it: cast(str, it)),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> AppPermissionData:
        return AppPermissionData.from_json(json.loads(serialized), type_ids)
    
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


class PreprocessingPropRange:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.PreprocessingPropRange'
    
    def __init__(self, prop_id: str, min: float, max: float) -> None:
        self.prop_id: str = prop_id
        """
        must be one of PreprocessingDataProperty.id
        """
        self.min: float = min
        """
        (no description yet)
        """
        self.max: float = max
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'propId': self.prop_id,
            'min': self.min,
            'max': self.max,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> PreprocessingPropRange:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('propId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: propId')),
            none_raise(optional_map(json.get('min', None), lambda it: cast(float, it)), lambda: KeyError('missing JSON key: min')),
            none_raise(optional_map(json.get('max', None), lambda it: cast(float, it)), lambda: KeyError('missing JSON key: max')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> PreprocessingPropRange:
        return PreprocessingPropRange.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'prop_id={self.prop_id}',
            f'min={self.min}',
            f'max={self.max}',
        ])
        return f'PreprocessingPropRange[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, PreprocessingPropRange):
            return NotImplemented
        return self.prop_id == other.prop_id \
            and self.min == other.min \
            and self.max == other.max


class ReconstructionData:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.ReconstructionData'
    
    def __init__(self, id: str, timestamp: int, class_num: int, iteration: int) -> None:
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
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> ReconstructionData:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('id', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: id')),
            none_raise(optional_map(json.get('timestamp', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: timestamp')),
            none_raise(optional_map(json.get('classNum', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: classNum')),
            none_raise(optional_map(json.get('iteration', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: iteration')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> ReconstructionData:
        return ReconstructionData.from_json(json.loads(serialized), type_ids)
    
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
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RefinementData'
    
    def __init__(self, id: str, job_id: str, data_id: str, iteration: int, timestamp: int) -> None:
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
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RefinementData:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('id', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: id')),
            none_raise(optional_map(json.get('jobId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: jobId')),
            none_raise(optional_map(json.get('dataId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: dataId')),
            none_raise(optional_map(json.get('iteration', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: iteration')),
            none_raise(optional_map(json.get('timestamp', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: timestamp')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RefinementData:
        return RefinementData.from_json(json.loads(serialized), type_ids)
    
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
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.RefinementBundleData'
    
    def __init__(self, id: str, job_id: str, refinement_bundle_id: str, iteration: int, timestamp: int) -> None:
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
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> RefinementBundleData:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('id', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: id')),
            none_raise(optional_map(json.get('jobId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: jobId')),
            none_raise(optional_map(json.get('refinementBundleId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: refinementBundleId')),
            none_raise(optional_map(json.get('iteration', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: iteration')),
            none_raise(optional_map(json.get('timestamp', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: timestamp')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> RefinementBundleData:
        return RefinementBundleData.from_json(json.loads(serialized), type_ids)
    
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
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.PypStats'
    
    def __init__(self, scope_voltage: Optional[float], scope_pixel: Optional[ValueA], scope_dose_rate: Optional[float]) -> None:
        self.scope_voltage: Optional[float] = scope_voltage
        """
        (no description yet)
        """
        self.scope_pixel: Optional[ValueA] = scope_pixel
        """
        (no description yet)
        """
        self.scope_dose_rate: Optional[float] = scope_dose_rate
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'scopeVoltage': self.scope_voltage if self.scope_voltage is not None else None,
            'scopePixel': self.scope_pixel.to_json() if self.scope_pixel is not None else None,
            'scopeDoseRate': self.scope_dose_rate if self.scope_dose_rate is not None else None,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> PypStats:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            optional_map(json.get('scopeVoltage', None), lambda it: cast(float, it)),
            optional_map(json.get('scopePixel', None), lambda it: ValueA.from_json(it)),
            optional_map(json.get('scopeDoseRate', None), lambda it: cast(float, it)),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> PypStats:
        return PypStats.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'scope_voltage={self.scope_voltage}',
            f'scope_pixel={self.scope_pixel}',
            f'scope_dose_rate={self.scope_dose_rate}',
        ])
        return f'PypStats[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, PypStats):
            return NotImplemented
        return self.scope_voltage == other.scope_voltage \
            and self.scope_pixel == other.scope_pixel \
            and self.scope_dose_rate == other.scope_dose_rate


class ProjectPermission:
    """
    (no description yet)
    """
    
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


class JobArgs(Generic[T]):
    """
    Argument storage for jobs.
    Jobs can have two sets of arguments:
    
    * The ``finished`` arguments: the arguments that were used when running the job the last time.
    * And/or the ``next`` arguments: the arguments that will be used to run the job the next time.
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.JobArgs'
    
    def __init__(self, finished: Optional[T], next: Optional[T]) -> None:
        self.finished: Optional[T] = finished
        """
        job arguments that have been processed by a run ie, describes the current state of the job's output files
        """
        self.next: Optional[T] = next
        """
        job arguments pending for the next run ie, describes how the job's output files could be in the one possible future
        """
        self._generics: Dict[str,Optional[str]] = {
            'T': None
        }
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        def writer_polymorphic_T(val: Any) -> Any:
            type_id = self._generics['T']
            if type_id == 'edu.duke.bartesaghi.micromon.services/SingleParticleSessionArgs':
                return val.to_json()
            elif type_id == 'edu.duke.bartesaghi.micromon.services/TomographySessionArgs':
                return val.to_json()
            elif type_id == 'edu.duke.bartesaghi.micromon.services/SingleParticleSessionDisplay':
                return val.to_json()
            elif type_id == 'edu.duke.bartesaghi.micromon.services/TomographySessionDisplay':
                return val.to_json()
            else:
                raise Exception(f'Failed to serialize type, unrecognized type id `{type_id}` for type parameter T')
        
        return {
            'finished': writer_polymorphic_T(self.finished) if self.finished is not None else None,
            'next': writer_polymorphic_T(self.next) if self.next is not None else None,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> JobArgs[T]:
        """
        Creates a new class instance from JSON
        """
        
        def reader_polymorphic_T(json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = type_ids) -> Any:
            if type_ids is None:
                raise Exception('JobArgs.from_json() failed because no type ids were given')
            try:
                type_id = type_ids['T']
            except KeyError:
                raise Exception('JobArgs.from_json() failed because no type id was found for type parameter T')
            if type_id == 'edu.duke.bartesaghi.micromon.services/SingleParticleSessionArgs':
                return SingleParticleSessionArgs.from_json(json)
            elif type_id == 'edu.duke.bartesaghi.micromon.services/TomographySessionArgs':
                return TomographySessionArgs.from_json(json)
            elif type_id == 'edu.duke.bartesaghi.micromon.services/SingleParticleSessionDisplay':
                return SingleParticleSessionDisplay.from_json(json)
            elif type_id == 'edu.duke.bartesaghi.micromon.services/TomographySessionDisplay':
                return TomographySessionDisplay.from_json(json)
            else:
                raise Exception(f'Failed to deserialize type, unrecognized type id `{type_id}` for type parameter T')
        
        return cls(
            optional_map(json.get('finished', None), lambda it: reader_polymorphic_T(it)),
            optional_map(json.get('next', None), lambda it: reader_polymorphic_T(it)),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> JobArgs[T]:
        return JobArgs.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'finished={self.finished}',
            f'next={self.next}',
        ])
        return f'JobArgs[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, JobArgs):
            return NotImplemented
        return self.finished == other.finished \
            and self.next == other.next


class UserData:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.UserData'
    
    def __init__(self, id: str, name: Optional[str]) -> None:
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
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> UserData:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('id', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: id')),
            optional_map(json.get('name', None), lambda it: cast(str, it)),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> UserData:
        return UserData.from_json(json.loads(serialized), type_ids)
    
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
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.ProjectRunData'
    
    def __init__(self, run_id: int, timestamp: int, status: RunStatus, jobs: List[JobRunData]) -> None:
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
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> ProjectRunData:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('runId', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: runId')),
            none_raise(optional_map(json.get('timestamp', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: timestamp')),
            none_raise(optional_map(json.get('status', None), lambda it: RunStatus.from_json(it)), lambda: KeyError('missing JSON key: status')),
            none_raise(optional_map(json.get('jobs', None), lambda it: [JobRunData.from_json(x) for x in cast(List[Any], it)]), lambda: KeyError('missing JSON key: jobs')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> ProjectRunData:
        return ProjectRunData.from_json(json.loads(serialized), type_ids)
    
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
    """
    (no description yet)
    """
    
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
    """
    (no description yet)
    """
    
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
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.StreamLogMsg'
    
    def __init__(self, timestamp: int, level: int, path: str, line: int, msg: str) -> None:
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
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> StreamLogMsg:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('timestamp', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: timestamp')),
            none_raise(optional_map(json.get('level', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: level')),
            none_raise(optional_map(json.get('path', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: path')),
            none_raise(optional_map(json.get('line', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: line')),
            none_raise(optional_map(json.get('msg', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: msg')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> StreamLogMsg:
        return StreamLogMsg.from_json(json.loads(serialized), type_ids)
    
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


class SingleParticleSessionDisplay:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.SingleParticleSessionDisplay'
    
    def __init__(self, group_name: str) -> None:
        self.group_name: str = group_name
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'groupName': self.group_name,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> SingleParticleSessionDisplay:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('groupName', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: groupName')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> SingleParticleSessionDisplay:
        return SingleParticleSessionDisplay.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'group_name={self.group_name}',
        ])
        return f'SingleParticleSessionDisplay[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, SingleParticleSessionDisplay):
            return NotImplemented
        return self.group_name == other.group_name


class TomographySessionDisplay:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.TomographySessionDisplay'
    
    def __init__(self, group_name: str) -> None:
        self.group_name: str = group_name
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'groupName': self.group_name,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> TomographySessionDisplay:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('groupName', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: groupName')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> TomographySessionDisplay:
        return TomographySessionDisplay.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'group_name={self.group_name}',
        ])
        return f'TomographySessionDisplay[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, TomographySessionDisplay):
            return NotImplemented
        return self.group_name == other.group_name


class SessionLogData:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.SessionLogData'
    
    def __init__(self, cluster_job_id: str, daemon: SessionDaemon, timestamp: int) -> None:
        self.cluster_job_id: str = cluster_job_id
        """
        (no description yet)
        """
        self.daemon: SessionDaemon = daemon
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
            'clusterJobId': self.cluster_job_id,
            'daemon': self.daemon.to_json(),
            'timestamp': self.timestamp,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> SessionLogData:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('clusterJobId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: clusterJobId')),
            none_raise(optional_map(json.get('daemon', None), lambda it: SessionDaemon.from_json(it)), lambda: KeyError('missing JSON key: daemon')),
            none_raise(optional_map(json.get('timestamp', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: timestamp')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> SessionLogData:
        return SessionLogData.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'cluster_job_id={self.cluster_job_id}',
            f'daemon={self.daemon}',
            f'timestamp={self.timestamp}',
        ])
        return f'SessionLogData[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, SessionLogData):
            return NotImplemented
        return self.cluster_job_id == other.cluster_job_id \
            and self.daemon == other.daemon \
            and self.timestamp == other.timestamp


class SessionJobLogData:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.SessionJobLogData'
    
    def __init__(self, cluster_job_id: str, name: str, timestamp: int) -> None:
        self.cluster_job_id: str = cluster_job_id
        """
        (no description yet)
        """
        self.name: str = name
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
            'clusterJobId': self.cluster_job_id,
            'name': self.name,
            'timestamp': self.timestamp,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> SessionJobLogData:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('clusterJobId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: clusterJobId')),
            none_raise(optional_map(json.get('name', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: name')),
            none_raise(optional_map(json.get('timestamp', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: timestamp')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> SessionJobLogData:
        return SessionJobLogData.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'cluster_job_id={self.cluster_job_id}',
            f'name={self.name}',
            f'timestamp={self.timestamp}',
        ])
        return f'SessionJobLogData[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, SessionJobLogData):
            return NotImplemented
        return self.cluster_job_id == other.cluster_job_id \
            and self.name == other.name \
            and self.timestamp == other.timestamp


class SessionPermission:
    """
    (no description yet)
    """
    
    Write: SessionPermission
    Read: SessionPermission
    
    def __init__(self, name: str) -> None:
        self.name = name
    
    def to_json(self) -> str:
        """
        Converts this enum value into JSON
        """
        
        return self.name
    
    @classmethod
    def from_json(cls, name: str) -> SessionPermission:
        """
        Reads this enum value from JSON
        """
        
        if name == 'Write':
            return SessionPermission.Write
        elif name == 'Read':
            return SessionPermission.Read
        else:
            return cls(name)
    
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __len__(self) -> int:
        return 2
    
    def __iter__(self) -> Iterator[SessionPermission]:
        return [SessionPermission.Write, SessionPermission.Read].__iter__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, SessionPermission):
            return NotImplemented
        return self.name == other.name
    
    def __hash__(self) -> int:
        return hash(self.name)

SessionPermission.Write = SessionPermission('Write')
SessionPermission.Read = SessionPermission('Read')


class SessionExportData:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.SessionExportData'
    
    def __init__(self, session_id: str, export_id: str, request: Serialized_SessionExportRequest, created: int, cluster_job_id: Optional[str], result: Optional[Serialized_SessionExportResult]) -> None:
        self.session_id: str = session_id
        """
        (no description yet)
        """
        self.export_id: str = export_id
        """
        (no description yet)
        """
        self.request: Serialized_SessionExportRequest = request
        """
        (no description yet)
        """
        self.created: int = created
        """
        (no description yet)
        """
        self.cluster_job_id: Optional[str] = cluster_job_id
        """
        (no description yet)
        """
        self.result: Optional[Serialized_SessionExportResult] = result
        """
        (no description yet)
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
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> SessionExportData:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('sessionId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: sessionId')),
            none_raise(optional_map(json.get('exportId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: exportId')),
            none_raise(optional_map(json.get('request', None), lambda it: cast(Serialized_SessionExportRequest, it)), lambda: KeyError('missing JSON key: request')),
            none_raise(optional_map(json.get('created', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: created')),
            optional_map(json.get('clusterJobId', None), lambda it: cast(str, it)),
            optional_map(json.get('result', None), lambda it: cast(Serialized_SessionExportResult, it)),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> SessionExportData:
        return SessionExportData.from_json(json.loads(serialized), type_ids)
    
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
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.MicrographMetadata'
    
    def __init__(self, id: str, timestamp: int, ccc: float, cccc: float, defocus1: float, defocus2: float, angle_astig: float, average_motion: float, num_auto_particles: int, image_dims: ImageDims) -> None:
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
        self.num_auto_particles: int = num_auto_particles
        """
        (no description yet)
        """
        self.image_dims: ImageDims = image_dims
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
            'numAutoParticles': self.num_auto_particles,
            'imageDims': self.image_dims.to_json(),
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> MicrographMetadata:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('id', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: id')),
            none_raise(optional_map(json.get('timestamp', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: timestamp')),
            none_raise(optional_map(json.get('ccc', None), lambda it: cast(float, it)), lambda: KeyError('missing JSON key: ccc')),
            none_raise(optional_map(json.get('cccc', None), lambda it: cast(float, it)), lambda: KeyError('missing JSON key: cccc')),
            none_raise(optional_map(json.get('defocus1', None), lambda it: cast(float, it)), lambda: KeyError('missing JSON key: defocus1')),
            none_raise(optional_map(json.get('defocus2', None), lambda it: cast(float, it)), lambda: KeyError('missing JSON key: defocus2')),
            none_raise(optional_map(json.get('angleAstig', None), lambda it: cast(float, it)), lambda: KeyError('missing JSON key: angleAstig')),
            none_raise(optional_map(json.get('averageMotion', None), lambda it: cast(float, it)), lambda: KeyError('missing JSON key: averageMotion')),
            none_raise(optional_map(json.get('numAutoParticles', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: numAutoParticles')),
            none_raise(optional_map(json.get('imageDims', None), lambda it: ImageDims.from_json(it)), lambda: KeyError('missing JSON key: imageDims')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> MicrographMetadata:
        return MicrographMetadata.from_json(json.loads(serialized), type_ids)
    
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
            f'num_auto_particles={self.num_auto_particles}',
            f'image_dims={self.image_dims}',
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
            and self.num_auto_particles == other.num_auto_particles \
            and self.image_dims == other.image_dims


class TwoDClassesData:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.TwoDClassesData'
    
    def __init__(self, owner_id: str, two_dclasses_id: str, created: int) -> None:
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
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> TwoDClassesData:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('ownerId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: ownerId')),
            none_raise(optional_map(json.get('twoDClassesId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: twoDClassesId')),
            none_raise(optional_map(json.get('created', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: created')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> TwoDClassesData:
        return TwoDClassesData.from_json(json.loads(serialized), type_ids)
    
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


class TomoDrgnConvergence:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.TomoDrgnConvergence'
    
    def __init__(self, parameters: TomoDrgnConvergenceParameters, iterations: List[TomoDrgnConvergenceIteration]) -> None:
        self.parameters: TomoDrgnConvergenceParameters = parameters
        """
        (no description yet)
        """
        self.iterations: List[TomoDrgnConvergenceIteration] = iterations
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'parameters': self.parameters.to_json(),
            'iterations': [x.to_json() for x in self.iterations],
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> TomoDrgnConvergence:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('parameters', None), lambda it: TomoDrgnConvergenceParameters.from_json(it)), lambda: KeyError('missing JSON key: parameters')),
            none_raise(optional_map(json.get('iterations', None), lambda it: [TomoDrgnConvergenceIteration.from_json(x) for x in cast(List[Any], it)]), lambda: KeyError('missing JSON key: iterations')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> TomoDrgnConvergence:
        return TomoDrgnConvergence.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'parameters={self.parameters}',
            f'iterations={self.iterations}',
        ])
        return f'TomoDrgnConvergence[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, TomoDrgnConvergence):
            return NotImplemented
        return self.parameters == other.parameters \
            and self.iterations == other.iterations


class TomoDrgnConvergenceParameters:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.TomoDrgnConvergence.Parameters'
    
    def __init__(self, num_classes: int, epochs: int, epoch_interval: int, final_maxima: int) -> None:
        self.num_classes: int = num_classes
        """
        (no description yet)
        """
        self.epochs: int = epochs
        """
        (no description yet)
        """
        self.epoch_interval: int = epoch_interval
        """
        (no description yet)
        """
        self.final_maxima: int = final_maxima
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'numClasses': self.num_classes,
            'epochs': self.epochs,
            'epochInterval': self.epoch_interval,
            'finalMaxima': self.final_maxima,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> TomoDrgnConvergenceParameters:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('numClasses', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: numClasses')),
            none_raise(optional_map(json.get('epochs', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: epochs')),
            none_raise(optional_map(json.get('epochInterval', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: epochInterval')),
            none_raise(optional_map(json.get('finalMaxima', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: finalMaxima')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> TomoDrgnConvergenceParameters:
        return TomoDrgnConvergenceParameters.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'num_classes={self.num_classes}',
            f'epochs={self.epochs}',
            f'epoch_interval={self.epoch_interval}',
            f'final_maxima={self.final_maxima}',
        ])
        return f'TomoDrgnConvergenceParameters[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, TomoDrgnConvergenceParameters):
            return NotImplemented
        return self.num_classes == other.num_classes \
            and self.epochs == other.epochs \
            and self.epoch_interval == other.epoch_interval \
            and self.final_maxima == other.final_maxima


class TomoDrgnConvergenceIteration:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.TomoDrgnConvergence.Iteration'
    
    def __init__(self, epoch: int, timestamp: int) -> None:
        self.epoch: int = epoch
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
            'epoch': self.epoch,
            'timestamp': self.timestamp,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> TomoDrgnConvergenceIteration:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('epoch', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: epoch')),
            none_raise(optional_map(json.get('timestamp', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: timestamp')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> TomoDrgnConvergenceIteration:
        return TomoDrgnConvergenceIteration.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'epoch={self.epoch}',
            f'timestamp={self.timestamp}',
        ])
        return f'TomoDrgnConvergenceIteration[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, TomoDrgnConvergenceIteration):
            return NotImplemented
        return self.epoch == other.epoch \
            and self.timestamp == other.timestamp


class TiltSeriesData:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.TiltSeriesData'
    
    def __init__(self, id: str, timestamp: int, ccc: float, cccc: float, defocus1: float, defocus2: float, angle_astig: float, average_motion: float, num_auto_particles: int, num_auto_virions: int, image_dims: ImageDims) -> None:
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
        self.num_auto_particles: int = num_auto_particles
        """
        (no description yet)
        """
        self.num_auto_virions: int = num_auto_virions
        """
        used only by older combined preprocessing blocks
        """
        self.image_dims: ImageDims = image_dims
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
            'numAutoParticles': self.num_auto_particles,
            'numAutoVirions': self.num_auto_virions,
            'imageDims': self.image_dims.to_json(),
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> TiltSeriesData:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('id', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: id')),
            none_raise(optional_map(json.get('timestamp', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: timestamp')),
            none_raise(optional_map(json.get('ccc', None), lambda it: cast(float, it)), lambda: KeyError('missing JSON key: ccc')),
            none_raise(optional_map(json.get('cccc', None), lambda it: cast(float, it)), lambda: KeyError('missing JSON key: cccc')),
            none_raise(optional_map(json.get('defocus1', None), lambda it: cast(float, it)), lambda: KeyError('missing JSON key: defocus1')),
            none_raise(optional_map(json.get('defocus2', None), lambda it: cast(float, it)), lambda: KeyError('missing JSON key: defocus2')),
            none_raise(optional_map(json.get('angleAstig', None), lambda it: cast(float, it)), lambda: KeyError('missing JSON key: angleAstig')),
            none_raise(optional_map(json.get('averageMotion', None), lambda it: cast(float, it)), lambda: KeyError('missing JSON key: averageMotion')),
            none_raise(optional_map(json.get('numAutoParticles', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: numAutoParticles')),
            none_raise(optional_map(json.get('numAutoVirions', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: numAutoVirions')),
            none_raise(optional_map(json.get('imageDims', None), lambda it: ImageDims.from_json(it)), lambda: KeyError('missing JSON key: imageDims')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> TiltSeriesData:
        return TiltSeriesData.from_json(json.loads(serialized), type_ids)
    
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
            f'num_auto_particles={self.num_auto_particles}',
            f'num_auto_virions={self.num_auto_virions}',
            f'image_dims={self.image_dims}',
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
            and self.num_auto_particles == other.num_auto_particles \
            and self.num_auto_virions == other.num_auto_virions \
            and self.image_dims == other.image_dims


class DriftXY:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.DriftXY'
    
    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        """
        (no description yet)
        """
        self.y: float = y
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'x': self.x,
            'y': self.y,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> DriftXY:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('x', None), lambda it: cast(float, it)), lambda: KeyError('missing JSON key: x')),
            none_raise(optional_map(json.get('y', None), lambda it: cast(float, it)), lambda: KeyError('missing JSON key: y')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> DriftXY:
        return DriftXY.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'x={self.x}',
            f'y={self.y}',
        ])
        return f'DriftXY[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, DriftXY):
            return NotImplemented
        return self.x == other.x \
            and self.y == other.y


class CtfTiltValues:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.CtfTiltValues'
    
    def __init__(self, index: int, defocus1: float, defocus2: float, astigmatism: float, cc: float, resolution: float) -> None:
        self.index: int = index
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
        self.astigmatism: float = astigmatism
        """
        (no description yet)
        """
        self.cc: float = cc
        """
        (no description yet)
        """
        self.resolution: float = resolution
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'index': self.index,
            'defocus1': self.defocus1,
            'defocus2': self.defocus2,
            'astigmatism': self.astigmatism,
            'cc': self.cc,
            'resolution': self.resolution,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> CtfTiltValues:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('index', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: index')),
            none_raise(optional_map(json.get('defocus1', None), lambda it: cast(float, it)), lambda: KeyError('missing JSON key: defocus1')),
            none_raise(optional_map(json.get('defocus2', None), lambda it: cast(float, it)), lambda: KeyError('missing JSON key: defocus2')),
            none_raise(optional_map(json.get('astigmatism', None), lambda it: cast(float, it)), lambda: KeyError('missing JSON key: astigmatism')),
            none_raise(optional_map(json.get('cc', None), lambda it: cast(float, it)), lambda: KeyError('missing JSON key: cc')),
            none_raise(optional_map(json.get('resolution', None), lambda it: cast(float, it)), lambda: KeyError('missing JSON key: resolution')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> CtfTiltValues:
        return CtfTiltValues.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'index={self.index}',
            f'defocus1={self.defocus1}',
            f'defocus2={self.defocus2}',
            f'astigmatism={self.astigmatism}',
            f'cc={self.cc}',
            f'resolution={self.resolution}',
        ])
        return f'CtfTiltValues[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, CtfTiltValues):
            return NotImplemented
        return self.index == other.index \
            and self.defocus1 == other.defocus1 \
            and self.defocus2 == other.defocus2 \
            and self.astigmatism == other.astigmatism \
            and self.cc == other.cc \
            and self.resolution == other.resolution


class ImageDims:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.pyp.ImageDims'
    
    def __init__(self, width: ValueUnbinnedI, height: ValueUnbinnedI, depth: ValueUnbinnedI, binning_factor: int, pixel_a: ValueA) -> None:
        self.width: ValueUnbinnedI = width
        """
        image width, in unbinned pixels (or voxels)
        """
        self.height: ValueUnbinnedI = height
        """
        image height, in unbinned pixels (or voxels)
        """
        self.depth: ValueUnbinnedI = depth
        """
        image depth, in unbinned pixels (or voxels)
        """
        self.binning_factor: int = binning_factor
        """
        the binning factor, same for all dimensions
        """
        self.pixel_a: ValueA = pixel_a
        """
        the size of one unbinned pixel (or voxel) in a micrograph (or tilt series)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'width': self.width.to_json(),
            'height': self.height.to_json(),
            'depth': self.depth.to_json(),
            'binningFactor': self.binning_factor,
            'pixelA': self.pixel_a.to_json(),
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> ImageDims:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('width', None), lambda it: ValueUnbinnedI.from_json(it)), lambda: KeyError('missing JSON key: width')),
            none_raise(optional_map(json.get('height', None), lambda it: ValueUnbinnedI.from_json(it)), lambda: KeyError('missing JSON key: height')),
            none_raise(optional_map(json.get('depth', None), lambda it: ValueUnbinnedI.from_json(it)), lambda: KeyError('missing JSON key: depth')),
            none_raise(optional_map(json.get('binningFactor', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: binningFactor')),
            none_raise(optional_map(json.get('pixelA', None), lambda it: ValueA.from_json(it)), lambda: KeyError('missing JSON key: pixelA')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> ImageDims:
        return ImageDims.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'width={self.width}',
            f'height={self.height}',
            f'depth={self.depth}',
            f'binning_factor={self.binning_factor}',
            f'pixel_a={self.pixel_a}',
        ])
        return f'ImageDims[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, ImageDims):
            return NotImplemented
        return self.width == other.width \
            and self.height == other.height \
            and self.depth == other.depth \
            and self.binning_factor == other.binning_factor \
            and self.pixel_a == other.pixel_a


class JobRunData:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.JobRunData'
    
    def __init__(self, job_id: str, status: RunStatus, cluster_jobs: List[ClusterJobData]) -> None:
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
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> JobRunData:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('jobId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: jobId')),
            none_raise(optional_map(json.get('status', None), lambda it: RunStatus.from_json(it)), lambda: KeyError('missing JSON key: status')),
            none_raise(optional_map(json.get('clusterJobs', None), lambda it: [ClusterJobData.from_json(x) for x in cast(List[Any], it)]), lambda: KeyError('missing JSON key: clusterJobs')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> JobRunData:
        return JobRunData.from_json(json.loads(serialized), type_ids)
    
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


class SessionExportResult:
    """
    WARNING: be very careful changing these classes! They get saved in the sessionExports database in serialized form, so deserializing old data could cause problems depending on how backwards compatible kotlinx.serialization is. Making changes here may require database migrations.
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.SessionExportResult'
    @abstractmethod
    def to_json(self) -> Dict[str,Any]:
        pass
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> SessionExportResult:
        """
        Creates a new class instance from JSON
        """
        
        cls_type = json['type']
        if cls_type == 'edu.duke.bartesaghi.micromon.services.SessionExportResult.Canceled':
            return SessionExportResultCanceled.from_json(json)
        elif cls_type == 'edu.duke.bartesaghi.micromon.services.SessionExportResult.Failed':
            return SessionExportResultFailed.from_json(json)
        elif cls_type == 'edu.duke.bartesaghi.micromon.services.SessionExportResult.Succeeded':
            return SessionExportResultSucceeded.from_json(json)
        else:
            raise Exception(f'unrecognized polymorphic subtype {cls_type} for supertype SessionExportResult')
    @abstractmethod
    def serialize(self) -> str:
        pass
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> SessionExportResult:
        return SessionExportResult.from_json(json.loads(serialized), type_ids)


class SessionExportResultCanceled(SessionExportResult, metaclass=ABCMeta):
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.SessionExportResult.Canceled'
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'type': 'edu.duke.bartesaghi.micromon.services.SessionExportResult.Canceled',
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> SessionExportResultCanceled:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> SessionExportResultCanceled:
        return SessionExportResultCanceled.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
        ])
        return f'SessionExportResultCanceled[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, SessionExportResultCanceled):
            return NotImplemented
        return True  # we are all the same! =D


class SessionExportResultFailed(SessionExportResult, metaclass=ABCMeta):
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.SessionExportResult.Failed'
    
    def __init__(self, reason: str) -> None:
        self.reason: str = reason
        """
        This message is displayed to the user, so make it readable
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'type': 'edu.duke.bartesaghi.micromon.services.SessionExportResult.Failed',
            'reason': self.reason,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> SessionExportResultFailed:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('reason', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: reason')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> SessionExportResultFailed:
        return SessionExportResultFailed.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'reason={self.reason}',
        ])
        return f'SessionExportResultFailed[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, SessionExportResultFailed):
            return NotImplemented
        return self.reason == other.reason


class SessionExportResultSucceeded(SessionExportResult, metaclass=ABCMeta):
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.SessionExportResult.Succeeded'
    
    def __init__(self, output: SessionExportResultSucceededOutput) -> None:
        self.output: SessionExportResultSucceededOutput = output
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'type': 'edu.duke.bartesaghi.micromon.services.SessionExportResult.Succeeded',
            'output': self.output.to_json(),
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> SessionExportResultSucceeded:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('output', None), lambda it: SessionExportResultSucceededOutput.from_json(it)), lambda: KeyError('missing JSON key: output')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> SessionExportResultSucceeded:
        return SessionExportResultSucceeded.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'output={self.output}',
        ])
        return f'SessionExportResultSucceeded[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, SessionExportResultSucceeded):
            return NotImplemented
        return self.output == other.output


class SessionExportResultSucceededOutput:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.SessionExportResult.Succeeded.Output'
    @abstractmethod
    def to_json(self) -> Dict[str,Any]:
        pass
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> SessionExportResultSucceededOutput:
        """
        Creates a new class instance from JSON
        """
        
        cls_type = json['type']
        if cls_type == 'edu.duke.bartesaghi.micromon.services.SessionExportResult.Succeeded.Output.Filter':
            return SessionExportResultSucceededOutputFilter.from_json(json)
        else:
            raise Exception(f'unrecognized polymorphic subtype {cls_type} for supertype SessionExportResultSucceededOutput')
    @abstractmethod
    def serialize(self) -> str:
        pass
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> SessionExportResultSucceededOutput:
        return SessionExportResultSucceededOutput.from_json(json.loads(serialized), type_ids)


class SessionExportResultSucceededOutputFilter(SessionExportResultSucceededOutput, metaclass=ABCMeta):
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.SessionExportResult.Succeeded.Output.Filter'
    
    def __init__(self, path: str) -> None:
        self.path: str = path
        """
        relative to the session folder
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'type': 'edu.duke.bartesaghi.micromon.services.SessionExportResult.Succeeded.Output.Filter',
            'path': self.path,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> SessionExportResultSucceededOutputFilter:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('path', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: path')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> SessionExportResultSucceededOutputFilter:
        return SessionExportResultSucceededOutputFilter.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'path={self.path}',
        ])
        return f'SessionExportResultSucceededOutputFilter[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, SessionExportResultSucceededOutputFilter):
            return NotImplemented
        return self.path == other.path


class ValueUnbinnedI:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.pyp.ValueUnbinnedI'
    
    def __init__(self, v: int) -> None:
        self.v: int = v
        """
        (no description yet)
        """
    
    def to_json(self) -> Dict[str,Any]:
        """
        Converts this class instance into JSON
        """
        
        return {
            'v': self.v,
        }
    
    @classmethod
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> ValueUnbinnedI:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('v', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: v')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> ValueUnbinnedI:
        return ValueUnbinnedI.from_json(json.loads(serialized), type_ids)
    
    def __str__(self) -> str:
        props = ', '.join([
            f'v={self.v}',
        ])
        return f'ValueUnbinnedI[{props}]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> Any:
        if not isinstance(other, ValueUnbinnedI):
            return NotImplemented
        return self.v == other.v


class ClusterJobData:
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.ClusterJobData'
    
    def __init__(self, cluster_job_id: str, web_name: Optional[str], cluster_name: Optional[str], status: RunStatus, array_info: Optional[ClusterJobDataArrayInfo]) -> None:
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
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> ClusterJobData:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('clusterJobId', None), lambda it: cast(str, it)), lambda: KeyError('missing JSON key: clusterJobId')),
            optional_map(json.get('webName', None), lambda it: cast(str, it)),
            optional_map(json.get('clusterName', None), lambda it: cast(str, it)),
            none_raise(optional_map(json.get('status', None), lambda it: RunStatus.from_json(it)), lambda: KeyError('missing JSON key: status')),
            optional_map(json.get('arrayInfo', None), lambda it: ClusterJobDataArrayInfo.from_json(it)),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> ClusterJobData:
        return ClusterJobData.from_json(json.loads(serialized), type_ids)
    
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
    """
    (no description yet)
    """
    
    TYPE_ID: str = 'edu.duke.bartesaghi.micromon.services.ClusterJobData.ArrayInfo'
    
    def __init__(self, size: int, started: int, ended: int, canceled: int, failed: int) -> None:
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
    def from_json(cls, json: Dict[str,Any], type_ids: Optional[Dict[str,str]] = None) -> ClusterJobDataArrayInfo:
        """
        Creates a new class instance from JSON
        """
        
        return cls(
            none_raise(optional_map(json.get('size', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: size')),
            none_raise(optional_map(json.get('started', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: started')),
            none_raise(optional_map(json.get('ended', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: ended')),
            none_raise(optional_map(json.get('canceled', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: canceled')),
            none_raise(optional_map(json.get('failed', None), lambda it: cast(int, it)), lambda: KeyError('missing JSON key: failed')),
        )
    
    def serialize(self) -> str:
        return json.dumps(self.to_json())
    
    @classmethod
    def deserialize(cls, serialized: str, type_ids: Optional[Dict[str,str]] = None) -> ClusterJobDataArrayInfo:
        return ClusterJobDataArrayInfo.from_json(json.loads(serialized), type_ids)
    
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
