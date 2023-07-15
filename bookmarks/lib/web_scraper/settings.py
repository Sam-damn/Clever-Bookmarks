"""
Settings module

"""


from configparser import ConfigParser
from pathlib import Path


def use_config(filename=None, config=None):
    'Use configuration object or read and parse a settings file'
    # expert option: use config file directly
    if config is not None:
        return config
    # default filename
    if filename is None:
        filename = str(Path(__file__).parent / 'settings.cfg')
    # load
    config = ConfigParser()
    config.read(filename)
    return config

DEFAULT_CONFIG = use_config()