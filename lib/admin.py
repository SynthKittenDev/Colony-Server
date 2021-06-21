from logging import getLogger

from lib.config import get_config

# Load Configuration
config = get_config()

log = getLogger(__name__)


def is_mod(name):
    """
    Checks if the given name is that of a mod, the mod list is imported from the config.ini file.
    :param name:
    :return:
    """
    mod_names = [x.lower() for x in config['admin']['moderators'].split(',')]
    b = name.lower() in mod_names
    return b
