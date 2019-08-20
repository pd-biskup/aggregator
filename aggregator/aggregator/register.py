from typing import Type, Dict, List, KeysView
import inspect
from importlib.util import spec_from_file_location, module_from_spec
import pathlib
from aggregator.plugin import Plugin
from utils.log import get_logger
from utils.config import config


log = get_logger('register')


class PluginRegister:
    """Register holding available plugins."""

    def __init__(self) -> None:
        self._store:Dict[str, Type[Plugin]] = {}
    
    def register(self, plugin:Type[Plugin]) -> None:
        """Add plugin to register."""
        if plugin.__pluginname__ not in self._store:
            self._store[plugin.__pluginname__] = plugin
            log.debug(f'Registered plugin {plugin.__pluginname__}.')
        else:
            log.warning(f'Trying to register plugin with identical name: {plugin.__pluginname__}.')

    def list_plugins(self) -> KeysView:
        """Return list of names of available plugins."""
       return self._store.keys()

    def __getitem__(self, key:str) -> Type[Plugin]:
        return self._store[key]

    def __len__(self) -> int:
        return len(self._store)

    def __contains__(self, key:str) -> bool:
        return key in self._store


def find_plugins(register):
    """Scan plugins directory and add all to the register."""
    path = pathlib.Path(config['plugins']['directory'])
    log.debug(f'Looking for plugins in {path}')
    if path.exists() and path.is_dir():
        n = 0
        for dir in path.iterdir():
            if dir.is_dir() and dir.joinpath('plugin.py').exists():
                file = dir.joinpath('plugin.py')
                spec = spec_from_file_location(f'plugins.{str(file)[:-3]}', file)
                mod = module_from_spec(spec)
                spec.loader.exec_module(mod)
                for attr, value in mod.__dict__.items():
                    if inspect.isclass(value) and issubclass(value, Plugin) and value.__pluginname__:
                        n += 1
                        log.debug(f'Found plugin {value.__pluginname__}')
                        register.register(value)
                log.info(f'Found {n} plugins.')
    else:
        log.warning('Plugin directory doesn\'t exist.')


register = PluginRegister()
find_plugins(register)
