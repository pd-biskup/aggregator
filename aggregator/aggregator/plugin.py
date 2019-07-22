from typing import Any, Union, Sequence, TypeVar
from pathlib import Path
from jinja2 import Template, FileSystemLoader, Environment
from utils.log import get_logger


log = get_logger('plugin')


class Param:

    __paramtype__ = ''

    def __init__(self, name:str, description:str, default:Any=None) -> None:
        self.name = name
        self.description = description
        self.default = default
    
    def validate(self, value:Any) -> Any:
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

    def __init__(self, id, params:dict={}, user_data:dict={}):
        self.id = id
        self.params = params
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

    def render_small(self) -> str:
        template = self.get_template('plugin.html')
        return template.render(params=self.params, user_data=self.user_data, payload=self.get_payload())

    def render_wide(self) -> str:
        return self.render_small()
    
    def render_high(self) -> str:
        return self.render_small()
    
    def render_big(self) -> str:
        return self.render_small()
