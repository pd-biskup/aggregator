import pytest
from aggregator.utils.config import Config, ConfigItem


def test_write_read_non_locked_item():
    item = ConfigItem('test', 1)
    assert item.get() == 1
    item.set(2)
    assert item.get() == 2


def test_lock_unlock_item():
    item = ConfigItem('test', 1, True)
    assert item.get() == 1
    item.set(2)
    assert item.get() == 1
    item.unlock()
    item.set(2)
    assert item.get() == 2
    item.lock()
    item.set(3)
    assert item.get() == 2


def test_static_item():
    item = ConfigItem('test', 1, True, True)
    assert item.get() == 1
    item.set(2)
    assert item.get() == 1
    item.unlock()
    item.set(2)
    assert item.get() == 1


def test_config_register():
    config = Config('test')
    config.register(ConfigItem('item', 1))
    assert config['item'] == 1
    subconfig = Config('sub')
    subconfig.register(ConfigItem('item', 2))
    config.register(subconfig)
    assert config['sub']['item'] == 2


def test_config_inexistent():
    config = Config('test')
    config['item'] = 1
    with pytest.raises(KeyError):
        config['item']


def test_config_mutate():
    config = Config('test')
    config.register(ConfigItem('item', 1))
    assert config['item'] == 1
    config['item'] = 2
    assert config['item'] == 2


def test_config_locked():
    config = Config('test', True)
    config.register(ConfigItem('item', 1))
    with pytest.raises(KeyError):
        config['item']
    config.unlock()
    config.register(ConfigItem('item', 1))
    assert config['item'] == 1
    config.lock()
    config['item'] = 2
    assert config['item'] == 1


def test_config_static():
    config = Config('test', True, True)
    config.register(ConfigItem('item1', 1))
    config.unlock()
    config.register(ConfigItem('item2', 2))
    config['item1'] = 3
    with pytest.raises(KeyError):
        config['item1']
    with pytest.raises(KeyError):
        config['item2']


def test_config_to_dict():
    config = Config('test')
    config.register(ConfigItem('item', 1))
    subconfig = Config('sub')
    subconfig.register(ConfigItem('item', 2))
    config.register(subconfig)
    assert config.to_dict() == {'item': 1, 'sub': {'item': 2}}


def test_config_from_dict():
    config = Config('test')
    config.register(ConfigItem('item', 1))
    subconfig = Config('sub')
    subconfig.register(ConfigItem('item', 2))
    config.register(subconfig)
    assert config == Config.from_dict('test', {'item': 1, 'sub': {'item': 2}})
