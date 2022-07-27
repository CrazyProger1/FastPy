from ..config import JsonConfig, CONFIG_FOLDER
from ..filesystem import FileSystem as Fs

transpiler_config = JsonConfig(
    filepath=Fs.join(CONFIG_FOLDER, 'transpiler.json'),
    authoload=True
)

TRANSPILER_CLASS_PATH = transpiler_config['transpiler_class']

CPP_TEMPLATES_DIR = transpiler_config['cpp_templates_dir']

CPP_MAIN_TEMPLATE_PATH = transpiler_config['cpp_main_template']
