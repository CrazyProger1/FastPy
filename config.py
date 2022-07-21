import fastpy
import os

# argparse config
ARGPARSE_CONFIG = fastpy.config.JsonConfig(
    filepath=os.path.join(fastpy.config.CONFIG_FOLDER, 'argparse.json'),
    authoload=True
)
