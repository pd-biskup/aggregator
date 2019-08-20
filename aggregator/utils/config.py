from typing import Any, Dict, Union
import json


class Config:
    """Dictionary with dynamic schema designed to hold configuration."""

    def __init__(self, name:str, locked:bool=False, static:bool=False) -> None:
        """
        Parameters
        ----------
        name : str
            Config name. Becomes key if Config is nested in another Config.
        locked : bool
            Initial lock state. Locked Config can't be edited until unlocked.
        static : bool
            Static Config can't be edited or unlocked.
        """
        self.name = name
        self._dict:Dict[str, Any] = {}
        self._locked = locked
        self._static = static
    
    def __getitem__(self, key:str) -> Any:
        if key in self._dict:
            if hasattr(self._dict[key], 'value'):
                return self._dict[key].value
            else:
                return self._dict[key]
        else:
            raise KeyError
    
    def __setitem__(self, key:str, value:Any) -> None:
        if not self._static:
            if not self._locked:
                if key in self._dict:
                    self._dict[key] = value
    
    def register(self, config:Union['ConfigItem', 'Config']) -> None:
        """Add new element to schema."""
        if not self._static:
            if not self._locked:
                if config.name not in self._dict:
                    self._dict[config.name] = config

    def lock(self) -> None:
        """Lock config. Any changes to locked config are impossible."""
        self._locked = True
    
    def unlock(self) -> None:
        """Unlock locked config."""
        self._locked = False
    
    # TODO
    def merge(self, config:'Config', replace:bool=True) -> None:
        raise NotImplementedError

    @classmethod
    def from_dict(cls, name:str, config:dict, locked:bool=False, static:bool=False) -> 'Config':
        """Return new config with content from dict."""
        new_dict:Dict[str, Union['Config', 'ConfigItem']] = {}
        for k, v in config.items():
            if isinstance(v, dict):
                new_dict[k] = cls.from_dict(k, v)
            else:
                new_dict[k] = ConfigItem(k, v)
        new_config = cls(name, locked, static)
        new_config._dict = new_dict
        return new_config

    def to_dict(self) -> dict:
        """Return dict with content of config"""
        d = {}
        for k, v in self._dict.items():
            if hasattr(v, 'value'):
                d[k] = v.value
            else:
                d[k] = v.to_dict()
        return d
    
    def __eq__(self, other:Any) -> bool:
        if isinstance(other, self.__class__):
            return self._dict == other._dict
        return False
    
    def __str__(self) -> str:
        string = f'{self.name}:\n'
        for v in self._dict.values():
            string += '  ' + str(v).replace('\n', '\n  ') + '\n'
        return string.rstrip()
    
    def __repr__(self) -> str:
        string = f'{self.__class__.__name__}('
        for v in self._dict.values():
            string += repr(v) + ', '
        if string.endswith(', '):
            string = string[:-2]
        return string + ')'


class ConfigItem:

    def __init__(self, name:str, value:Any=None, locked:bool=False, static:bool=False) -> None:
        self.name = name
        self.value = value
        self._static = static
        self._locked = locked

    def set(self, value:Any) -> None:
        if not self._static:
            if not self._locked:
                self.value = value
    
    def get(self) -> Any:
        return self.value
    
    def lock(self) -> None:
        self._locked = True
    
    def unlock(self) -> None:
        self._locked = False
    
    def __eq__(self, other:Any) -> bool:
        if isinstance(other, self.__class__):
            return self.value == other.value
        return False

    def __str__(self) -> str:
        return f'{self.name}: {self.value}'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.name}: {self.value})'

with open('config.json') as file:
    config = Config.from_dict('main', json.load(file))
