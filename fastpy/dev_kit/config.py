from ..config import JsonConfig, CONFIG_FOLDER
from ..filesystem import FileSystem as Fs

builtin_config = JsonConfig(
    filepath=Fs.join(CONFIG_FOLDER, 'builtin.json'),
    authoload=True
)

BUILTIN_TYPES = builtin_config['builtin_types']
BUILTIN_FUNCTIONS = builtin_config['builtin_functions']
