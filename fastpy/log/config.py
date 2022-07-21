import logging

from ..config import JsonConfig, CONFIG_FOLDER
import os

logging_config = JsonConfig(os.path.join(CONFIG_FOLDER, 'logging.json'), authoload=True)

# logger config
APP_NAME = logging_config['app_name']
LEVEL = logging_config['level']

# formatter config
FORMAT = logging_config['format']
