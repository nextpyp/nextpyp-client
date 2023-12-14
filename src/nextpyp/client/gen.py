
from __future__ import annotations

from typing import Optional, List, Dict, Set, Any, Iterator, TYPE_CHECKING

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

    def __eq__(self, other: object) -> bool:
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

    def __eq__(self, other: object) -> bool:
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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UserData):
            return NotImplemented
        return self.id == other.id \
            and self.name == other.name
