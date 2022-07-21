import fastpy
import os

CONFIG_FOLDER = 'config'

# argparse config
ARGPARSE_CONFIG = fastpy.JsonConfig(
    filepath=os.path.join(CONFIG_FOLDER, 'argparse.json'),
    authoload=True
)
