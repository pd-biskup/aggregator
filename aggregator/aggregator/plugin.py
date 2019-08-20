from typing import Any, Union, Sequence, TypeVar
from pathlib import Path
from enum import IntEnum
from jinja2 import Template, FileSystemLoader, Environment
from utils.log import get_logger


log = get_logger('plugin')


class PluginSize(IntEnum):
    SMALL = 1,
    WIDE = 2,
    TALL = 3,
    BIG = 4,
    FULL = 5


class Param:
    """
    Base class from which all plugin parameters inherit
    
    Class attributes
    ----------------
    __paramtype__ : str
        Identifies parameter value type. Must be overwriten when subclassing.
    """

    __paramtype__ = ''

    def __init__(self, name:str, description:str, default:Any=None) -> None:
        """
        Arguments
        ---------
        name : str
            Name of the parameter. Must be unique in the context of the plugin.
        description : str
            Short description which will show as hovertext.
        default : Any
            Default value of parameter.
        """
        self.name = name
        self.description = description
        self.default = default
    
    def validate(self, value:Any) -> Any:
        """Check if value has proper type. Cast if possible."""
        return value


class BoolParam(Param):

    __paramtype__ = 'bool'

    def __init__(self, name:str, description:str,  default:bool=False) -> None:
        super().__init__(name, description, default)
    
    def validate(self, value:Any) -> bool:
        if value == 'true':
            return True
        elif value == 'false':
            return False
        return bool(value)


class StringParam(Param):

    __paramtype__ = 'str'

    def __init__(self, name:str, description:str,  default:str='') -> None:
        super().__init__(name, description, default)
    
    def validate(self, value:Any) -> str:
        return str(value)


class NumberParam(Param):

    __paramtype__ = 'num'

    def __init__(self, name:str, description:str,  default:Union[int, float]=None, min:int=None, max:int=None, step:Union[int, float]=1) -> None:
        super().__init__(name, description, default)
        self.min = min
        self.max = max
        self.step = step

    def validate(self, value:Any) -> Union[int, float]:
        if isinstance(self.step, int):
            return int(value)
        else:
            return float(value)


class ComplexParam(Param):

    __paramtype__ = 'complex'

    def __init__(self, name:str, description:str, type:Sequence[Param], default:Sequence[Union[bool, str, int, float]]=None):
        super().__init__(name, description, default)
        self.type = type

    def validate(self, value:Sequence[Any]) -> Sequence[Union[bool, str, int, float]]:
        return [t.validate(v) for t, v in zip(self.type, value)]


class ListParam(Param):

    __paramtype__ = 'list'

    def __init__(self, name:str, description:str, type:Param, default:Union[bool, str, int, float, dict]=None) -> None:
        super().__init__(name, description, default)
    
    def validate(self, value:Sequence[Any]) -> Sequence[Union[bool, str, int, float, dict]]:
        return [self.type.validate(v) for v in value]


class Plugin:

    __pluginname__ = ''
    __paramschema__:Sequence[Param] = []
    __location__ = ''
    __sizes__:Sequence[PluginSize] = []

    def __init__(self, id, size:PluginSize, params:dict={}, user_data:dict={}):
        self.id = id
        self.params = params
        self.size = size
        for param in self.__paramschema__:
            if param.name not in self.params:
                self.params[param.name] = param.default
        self.user_data = user_data
    
    def get_payload(self) -> Any:
        return None

    def get_template(self, template:str) -> Template:
        path = Path(self.__location__).parent.joinpath('templates')
        loader = FileSystemLoader(searchpath=str(path))
        env = Environment(loader=loader)
        return env.get_template(template)
    
    def render(self) -> str:
        if self.size is PluginSize.SMALL:
            return self.render_small()
        elif self.size is PluginSize.WIDE:
            return self.render_wide()
        elif self.size is PluginSize.TALL:
            return self.render_tall()
        elif self.size is PluginSize.BIG:
            return self.render_big()
        elif self.size is PluginSize.FULL:
            return self.render_full()

    def render_small(self) -> str:
        template = self.get_template('small.html')
        return template.render(params=self.params, user_data=self.user_data, payload=self.get_payload())

    def render_wide(self) -> str:
        template = self.get_template('wide.html')
        return template.render(params=self.params, user_data=self.user_data, payload=self.get_payload())
    
    def render_tall(self) -> str:
        template = self.get_template('tall.html')
        return template.render(params=self.params, user_data=self.user_data, payload=self.get_payload())
    
    def render_big(self) -> str:
        template = self.get_template('big.html')
        return template.render(params=self.params, user_data=self.user_data, payload=self.get_payload())
    
    def render_full(self) -> str:
        template = self.get_template('full.html')
        return template.render(params=self.params, user_data=self.user_data, payload=self.get_payload())