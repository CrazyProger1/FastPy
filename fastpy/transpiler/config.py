from ..config import JsonConfig, CONFIG_FOLDER
from ..filesystem import FileSystem as Fs

transpiler_config = JsonConfig(
    filepath=Fs.join(CONFIG_FOLDER, 'transpiler.json'),
    authoload=True
)

TRANSPILER_CLASS_PATH = transpiler_config[
    'transpiler_class'
]  # Transpailer classpath to import, by default - fastpy.transpiler.transpilers.Transpiler

CPP_TEMPLATES_DIR = transpiler_config['cpp_templates_dir']  # folder of C++ templates
CPP_MAIN_TEMPLATE_PATH = transpiler_config['cpp_main_template']  # main C++ template filename
CPP_TEMPLATE_PATH = transpiler_config['cpp_template']  # module C++ template filename

NODE_TRANSPILING = transpiler_config['node_transpiling']  # node transpiling data

builtin_config = JsonConfig(
    filepath=Fs.join(CONFIG_FOLDER, 'builtin.json'),
    authoload=True
)

BUILTIN_TYPES: dict = builtin_config['builtin_types']
BUILTIN_FUNCTIONS: dict = builtin_config['builtin_functions']

operators_config = JsonConfig(
    filepath=Fs.join(CONFIG_FOLDER, 'operators.json'),
    authoload=True
)

OPERATORS_EQUIVALENTS = operators_config['fastpy_cpp_equivalents']  # C++ equivalents of FastPy operators
