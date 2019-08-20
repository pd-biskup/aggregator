import logging
from typing import Optional
from sys import stdout, stderr
from utils.config import config


_logger:Optional[logging.Logger] = None


def get_logger(name:str) -> logging.Logger:
    """Return logger with given name."""
    global _logger
    if not _logger:
        _logger = logging.getLogger()
        _logger.setLevel(0)
        _logger.addHandler(logging.NullHandler(0))
        formatter = logging.Formatter('%(asctime)s|%(name)s|%(levelname)s|%(message)s')
        for info in config['logging']['loggers']:
            if info['enabled']:
                if info['type'] == 'file':
                    handler:logging.Handler = logging.FileHandler(info['output'])
                    handler.setLevel(info['level'])
                    handler.setFormatter(formatter)
                    _logger.addHandler(handler)
                elif info['type'] == 'stream':
                    if info['output'] == 'out':
                        handler = logging.StreamHandler(stdout)
                        handler.setLevel(info['level'])
                        handler.setFormatter(formatter)
                        _logger.addHandler(handler)
                    elif info['output'] == 'err':
                        handler = logging.StreamHandler(stderr)
                        handler.setLevel(info['level'])
                        handler.setFormatter(formatter)
                        _logger.addHandler(handler)
    return logging.getLogger(name)
