import os

from ..config import JsonConfig, CONFIG_FOLDER
from ..filesystem import FileSystem as Fs

analyzer_config = JsonConfig(
    filepath=os.path.join(CONFIG_FOLDER, 'analyzer.json'),
    authoload=True
)

ANALYZER_CLASS_PATH: str = analyzer_config['semantic_analyzer_class']  # analyzer class path to import
NODE_ANALYZING: dict = analyzer_config['node_analyzing']  # node analyzing data

builtin_config = JsonConfig(
    filepath=Fs.join(CONFIG_FOLDER, 'builtin.json'),
    authoload=True
)

BUILTIN_TYPES = builtin_config['builtin_types']
BUILTIN_FUNCTIONS = builtin_config['builtin_functions']
