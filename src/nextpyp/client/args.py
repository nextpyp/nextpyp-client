
from __future__ import annotations
from abc import ABCMeta, abstractmethod

import os

from typing import Optional, Any, Dict, List, Tuple

import toml


class PypArgType(metaclass=ABCMeta):

    def __init__(self, type_id: str) -> None:
        self.type_id = type_id

    @abstractmethod
    def check(self, value: Any) -> Any:
        pass


class TBool(PypArgType):

    type_id = 'bool'

    def __init__(self) -> None:
        super().__init__(TBool.type_id)

    def check(self, value: Any) -> Any:
        if type(value) is bool:
            return value
        else:
            raise TypeError(f'value is a {type(value)} instead of a bool')


class TInt(PypArgType):

    type_id = 'int'

    def __init__(self) -> None:
        super().__init__(TInt.type_id)

    def check(self, value: Any) -> Any:
        if type(value) is int:
            return value
        else:
            raise TypeError(f'value is a {type(value)} instead of an int')


class TFloat(PypArgType):

    type_id = 'float'

    def __init__(self) -> None:
        super().__init__(TFloat.type_id)

    def check(self, value: Any) -> Any:
        if type(value) is float:
            return value
        elif type(value) is int:
            # allow implicit promotion from int
            return float(value)
        else:
            raise TypeError(f'value is a {type(value)} instead of a float')


class TFloat2(PypArgType):

    type_id = 'float2'

    def __init__(self) -> None:
        super().__init__(TFloat2.type_id)

    def check(self, value: Any) -> Any:
        if type(value) is tuple:
            if len(value) == 2 and type(value[0]) is float and type(value[0]) is float:
                return value
            else:
                raise TypeError(f'value is a {(type(v) for v in value)} instead of a (float, float)')
        else:
            raise TypeError(f'value is a {type(value)} instead of a tuple')



class TStr(PypArgType):

    type_id = 'str'

    def __init__(self) -> None:
        super().__init__(TStr.type_id)

    def check(self, value: Any) -> Any:
        if type(value) is str:
            return value
        else:
            raise TypeError(f'value is a {type(value)} instead of a str')


class TEnumValue:

    def __init__(self, id: str, name: str) -> None:
        self.id = id
        self.name = name


class TEnum(PypArgType):

    type_id = 'enum'

    def __init__(self, values: List[TEnumValue]) -> None:
        super().__init__(TEnum.type_id)
        self.values = values

    def check(self, value: Any) -> Any:
        if type(value) is str:
            if next((v for v in self.values if v.id == value), None) is not None:
                return value
            else:
                raise ValueError(f'value {value} is not one of {self.values}')
        else:
            raise TypeError(f'value is a {type(value)} instead of a str')


class TPathKind:

    Files: TPathKind
    Folders: TPathKind

    @classmethod
    def values(cls) -> List[TPathKind]:
        return [TPathKind.Files, TPathKind.Folders]

    def __init__(self, id: str) -> None:
        self.id = id

    def __str__(self) -> str:
        return self.id

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> Any:
        if not isinstance(other, TPathKind):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)


TPathKind.Files = TPathKind('files')
TPathKind.Folders = TPathKind('folders')


class TPath(PypArgType):

    type_id = 'path'

    def __init__(self, kind: TPathKind, glob: bool) -> None:
        super().__init__(TPath.type_id)
        self.kind = kind
        self.glob = glob

    def check(self, value: Any) -> Any:
        if type(value) is str:
            return value
        else:
            raise TypeError(f'value is a {type(value)} instead of a str')


class PypArgValue:
    pass


class VBool(PypArgValue):

    def __init__(self, value: bool) -> None:
        self.value = value


class VInt(PypArgValue):

    def __init__(self, value: int) -> None:
        self.value = value


class VFloat(PypArgValue):

    def __init__(self, value: float) -> None:
        self.value = value


class VFloat2(PypArgValue):

    def __init__(self, value: Tuple[float, float]) -> None:
        self.value = value


class VStr(PypArgValue):

    def __init__(self, value: str) -> None:
        self.value = value


class VEnum(PypArgValue):

    def __init__(self, value: str) -> None:
        self.value = value


class VPath(PypArgValue):

    def __init__(self, value: str) -> None:
        self.value = value


class VRef(PypArgValue):

    def __init__(self, arg_id: str) -> None:
        self.arg_id = arg_id


class PypArg:

    def __init__(self,
                 tab_id: str, arg_id: str, name: str, description: str, arg_type: PypArgType, required: bool,
                 default: Optional[PypArgValue], hidden: PypHidden
                 ) -> None:
        self.tab_id = tab_id
        self.arg_id = arg_id
        self.name = name
        self.description = description
        self.arg_type = arg_type
        self.required = required
        self.default = default
        self.hidden = hidden
        pass

    def full_id(self) -> str:
        return f'{self.tab_id}_{self.arg_id}'

    def __str__(self) -> str:
        return f'PypArg[{self.tab_id}, {self.arg_id}]'

    def __repr__(self) -> str:
        return self.__str__()


class PypHidden:

    @classmethod
    def none(cls) -> PypHidden:
        return PypHidden([])

    @classmethod
    def all(cls) -> PypHidden:
        return PypHidden(None)

    @classmethod
    def some(cls, block_ids: List[str]) -> PypHidden:
        return PypHidden(block_ids)

    def __init__(self, block_ids: Optional[List[str]]) -> None:
        self.block_ids = block_ids

    def is_visible_in_block(self, block_id: str) -> bool:
        return self.block_ids is not None and not (block_id in self.block_ids)


class PypBlock:

    # TODO: can these be added to the codegen someday? so they stay in sync?

    JOB_SINGLE_PARTICLE_COARSE_REFINEMENT = 'spr_coarse_refine'
    JOB_SINGLE_PARTICLE_FINE_REFINEMENT = 'spr_map_clean'
    JOB_SINGLE_PARTICLE_FLEXIBLE_REFINEMENT = 'spr_flexible_refine'
    JOB_SINGLE_PARTICLE_IMPORT_DATA = 'spr_import'
    JOB_SINGLE_PARTICLE_MASKING = 'spr_tomo_map_mask'
    JOB_SINGLE_PARTICLE_POST_PROCESSING = 'spr_tomo_post_process'
    JOB_SINGLE_PARTICLE_PREPROCESSING = 'spr_pre_process'
    JOB_SINGLE_PARTICLE_RAW_DATA = 'spr_import_raw'
    JOB_SINGLE_PARTICLE_RELION_DATA = 'spr_import_star'
    JOB_SINGLE_PARTICLE_SESSION_DATA = 'spr_pre_process'

    JOB_TOMOGRAPHY_COARSE_REFINEMENT = 'tomo_coarse_refine'
    JOB_TOMOGRAPHY_FINE_REFINEMENT = 'tomo_map_clean'
    JOB_TOMOGRAPHY_FLEXIBLE_REFINEMENT = 'tomo_flexible_refine'
    JOB_TOMOGRAPHY_IMPORT_DATA = 'tomo_import'
    JOB_TOMOGRAPHY_MOVIE_CLEANING = 'tomo_map_clean'
    JOB_TOMOGRAPHY_PREPROCESSING = 'tomo_pre_process'
    JOB_TOMOGRAPHY_RAW_DATA = 'tomo_import_raw'
    JOB_TOMOGRAPHY_RELION_DATA = 'tomo_import_star'
    JOB_TOMOGRAPHY_SESSION_DATA = 'tomo_pre_process'

    SESSION_SINGLE_PARTICLE = 'stream_spr'
    SESSION_TOMOGRAPHY = 'stream_tomo'


    def __init__(self, block_id: str, name: str, description: str, tabs: List[str]) -> None:
        self.block_id = block_id
        self.name = name
        self.description = description
        self.tabs = tabs

    def __str__(self) -> str:
        return f'PypBlock[{self.block_id}]'

    def __repr__(self) -> str:
        return self.__str__()


class PypTab:

    def __init__(self, tab_id: str, name: str, description: str, hidden: PypHidden) -> None:
        self.tab_id = tab_id
        self.name = name
        self.description = description
        self.hidden = hidden
        self.args: List[PypArg] = []

    def __str__(self) -> str:
        return f'PypTab[{self.tab_id}]'

    def __repr__(self) -> str:
        return self.__str__()


class PypArgs:

    @classmethod
    def default_path(cls) -> str:
        src_dir = os.path.dirname(__file__)
        return os.path.join(src_dir, 'pyp_config.toml')

    def __init__(self,
                 blocks: Optional[List[PypBlock]] = None,
                 tabs: Optional[List[PypTab]] = None,
                 args: Optional[List[PypArg]] = None
                 ):
        if blocks is None:
            blocks = []
        self.blocks = blocks
        if tabs is None:
            tabs = []
        self.tabs = tabs
        if args is None:
            args = []
        self.args = args

    @classmethod
    def from_config(cls, toml_str: str) -> PypArgs:

        # parse the toml config file
        doc = toml.loads(toml_str)

        # read the blocks
        blocks: List[PypBlock] = []
        for block_id, doc_block in doc['blocks'].items():

            # skip entries that start with _, those aren't blocks
            if block_id.startswith('_'):
                continue

            blocks.append(PypBlock(
                block_id,
                doc_block['name'],
                doc_block['description'],
                doc_block['tabs']
            ))

        def read_hidden(d: Any) -> PypHidden:
            if d is None:
                return PypHidden.none()
            elif d is True:
                return PypHidden.all()
            elif type(d) is list:
                return PypHidden.some(d)
            else:
                raise Exception(f'unrecognized hidden value: {type(d)} = {d}')

        # read the tabs and args
        tabs: List[PypTab] = []
        args: List[PypArg] = []
        for tab_id, doc_tab in doc['tabs'].items():

            # skip entries that start with _, those aren't tabs
            if tab_id.startswith('_'):
                continue

            tab = PypTab(
                tab_id,
                doc_tab['_name'],
                doc_tab['_description'],
                read_hidden(doc_tab.get('hidden', None))
            )
            tabs.append(tab)

            # read the args for this tab
            for arg_id, doc_arg in doc_tab.items():

                # skip entries that start with _, those aren't args
                if arg_id.startswith('_'):
                    continue

                # read the arg type and default value
                arg_type_id = doc_arg['type']
                arg_type: PypArgType
                arg_default: Optional[PypArgValue] = None
                d = doc_arg.get('default', None)
                if arg_type_id == TBool.type_id:
                    arg_type = TBool()
                    if d is not None:
                        arg_default = VBool(d)
                elif arg_type_id == TInt.type_id:
                    arg_type = TInt()
                    if d is not None:
                        arg_default = VInt(d)
                elif arg_type_id == TFloat.type_id:
                    arg_type = TFloat()
                    if d is not None:
                        arg_default = VFloat(d)
                elif arg_type_id == TFloat2.type_id:
                    arg_type = TFloat2()
                    if d is not None:
                        arg_default = VFloat2((d[0], d[1]))
                elif arg_type_id == TStr.type_id:
                    arg_type = TStr()
                    if d is not None:
                        arg_default = VStr(d)
                elif arg_type_id == TEnum.type_id:
                    arg_type = TEnum(
                        [TEnumValue(id, name) for id, name in doc_arg['enum'].items()]
                    )
                    if d is not None:
                        arg_default = VEnum(d)
                elif arg_type_id == TPath.type_id:
                    arg_type = TPath(
                        next(kind for kind in TPathKind.values() if kind.id == doc_arg['path']['type']),
                        doc_arg.get('glob', False)
                    )
                    if d is not None:
                        arg_default = VPath(d)
                else:
                    raise Exception(f'unrecognized pyp arg type id: {arg_type_id}')

                arg = PypArg(
                    tab_id,
                    arg_id,
                    doc_arg['name'],
                    doc_arg['description'],
                    arg_type,
                    doc_arg.get('required', False),
                    arg_default,
                    read_hidden(doc_arg.get('hidden', None))
                )
                args.append(arg)
                tab.args.append(arg)

        return PypArgs(blocks, tabs, args)

    def find_block(self, block_id: str) -> Optional[PypBlock]:
        return next((b for b in self.blocks if b.block_id == block_id), None)

    def find_block_or_raise(self, block_id: str) -> PypBlock:
        block = self.find_block(block_id)
        if block is None:
            raise KeyError(f'no pyp block with id = {block_id}')
        return block

    def find_tab(self, tab_id: str) -> Optional[PypTab]:
        return next((t for t in self.tabs if t.tab_id == tab_id), None)

    def find_tab_or_raise(self, tab_id: str) -> PypTab:
        tab = self.find_tab(tab_id)
        if tab is None:
            raise KeyError(f'no pyp tab with id = {tab_id}')
        return tab

    def find_arg(self, full_id: str) -> Optional[PypArg]:
        return next((arg for arg in self.args if arg.full_id() == full_id), None)

    def find_arg_or_raise(self, full_id: str) -> PypArg:
        arg = self.find_arg(full_id)
        if arg is None:
            raise KeyError(f'no pyp arg with full id = {full_id}')
        return arg

    def filter_block(self,
                     block_id: str,
                     include_hidden_tabs: bool = False,
                     include_hidden_args: bool = False
                     ) -> PypArgs:

        block = self.find_block_or_raise(block_id)

        tabs = [self.find_tab_or_raise(tab_id) for tab_id in block.tabs]
        tabs = [tab for tab in tabs if include_hidden_tabs or tab.hidden.is_visible_in_block(block_id)]

        args = [arg for tab in tabs for arg in tab.args if include_hidden_args or arg.hidden.is_visible_in_block(block_id)]

        return PypArgs([], tabs, args)

    def append_all(self, args: List[PypArg]) -> PypArgs:
        return PypArgs(
            self.blocks,
            self.tabs,
            self.args + args
        )


class PypArgValues:

    @classmethod
    def from_toml(cls, args: PypArgs, toml_str: Optional[str] = None) -> PypArgValues:
        values = PypArgValues(args)
        if toml_str is not None:
            values.read(toml_str)
        return values

    def __init__(self, args: PypArgs) -> None:
        # since we overrode __setattr__ here,
        # to actually set class members, we need to use the superclass implementation
        self.args: PypArgs
        self._dict: Dict[str, Any]
        super().__setattr__('args', args)
        super().__setattr__('_dict', {})

    def __getitem__(self, arg: PypArg) -> Optional[Any]:
        return self._dict.get(arg.full_id(), None)

    def __setitem__(self, arg: PypArg, value: Any) -> None:
        self._dict[arg.full_id()] = arg.arg_type.check(value)

    def __delitem__(self, arg: PypArg) -> None:
        del self._dict[arg.full_id()]

    def __getattr__(self, full_id: str) -> Optional[Any]:
        arg = self.args.find_arg_or_raise(full_id)
        return self[arg]

    def __setattr__(self, full_id: str, value: Any) -> None:
        arg = self.args.find_arg_or_raise(full_id)
        self[arg] = value

    def read(self, toml_str: str) -> None:

        doc = toml.loads(toml_str)

        for full_id, value in doc.items():
            arg = self.args.find_arg_or_raise(full_id)

            # apply read transformations to fix roundtrip issues with TOML parsing
            if type(arg.arg_type) is TFloat:
                # if we write a float without a fractional part to a TOML file,
                # the TOML parser will read it back in as an int,
                # so convert it back to a float
                value = float(value)
            elif type(arg.arg_type) is TFloat2:
                # convert the array to a tuple
                value = (float(x) for x in value)

            self[arg] = value

    def write(self) -> str:
        out: Dict[str, Any] = {}

        for full_id, value in self._dict.items():
            arg = self.args.find_arg_or_raise(full_id)

            # don't bother writing none values
            if value is None:
                continue

            # apply write transformations to fix roundtrip issues with TOML parsing
            if type(arg.arg_type) is TFloat2:
                # convert the tuple to an array
                value = [x for x in value]

            out[full_id] = value

        return toml.dumps(out)


class MicromonArgs:

    # TODO: can these be added to the codegen someday? so they stay in sync?

    slurm_launch_cpus = PypArg(
        'slurm',
        'launch_tasks',
        'Threads (launch task)',
        'Number of CPUs used during launching',
        TInt(),
        False,
        VInt(1),
        PypHidden.none()
    )

    slurm_launch_memory = PypArg(
        'slurm',
        'launch_memory',
        'Memory (launch task)',
        'Amount of memory used during launching (0=all memory in node, GB)',
        TInt(),
        False,
        VInt(4),
        PypHidden.none()
    )

    slurm_launch_walltime = PypArg(
        'slurm',
        'launch_walltime',
        'Walltime (launch task)',
        'Max running time for each task (dd-hh:mm:ss)',
        TStr(),
        False,
        VStr('2:00:00'),
        PypHidden.none()
    )

    slurm_launch_account = PypArg(
        'slurm',
        'launch_account',
        'Slurm account (launch task)',
        'Charge resources used by this job to specified account',
        TStr(),
        False,
        None,
        PypHidden.none()
    )

    slurm_launch_queue = PypArg(
        'slurm',
        'launch_queue',
        'CPU partition (launch task)',
        'SLURM partition to submit CPU jobs',
        TStr(),
        False,
        None,
        PypHidden.none()
    )

    slurm_launch_args = [
        slurm_launch_cpus,
        slurm_launch_memory,
        slurm_launch_walltime,
        slurm_launch_account,
        slurm_launch_queue
    ]


# load the args once and save them in the module
with open(PypArgs.default_path(), 'r') as f:
    all_args = PypArgs.from_config(f.read())


def block_args(block_id: str) -> PypArgs:
    args = all_args.filter_block(block_id, include_hidden_tabs=True)
    args.append_all(MicromonArgs.slurm_launch_args)
    return args
