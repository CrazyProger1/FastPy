import fastpy
import os

CONFIG_FOLDER = 'config'

# argparse config
ARGPARSE_CONFIG = fastpy.JsonConfig(os.path.join(CONFIG_FOLDER, 'argparse.json'))
