from ..config import JsonConfig, CONFIG_FOLDER
import os

transpiler_config = JsonConfig(
    filepath=os.path.join(CONFIG_FOLDER, 'transpiler.json'),
    authoload=True
)

TRANSPILER_CLASS_PATH = transpiler_config['transpiler_class']
