from ..config import JsonConfig, CONFIG_FOLDER
import os

parser_config = JsonConfig(
    filepath=os.path.join(CONFIG_FOLDER, 'parser.json'),
    authoload=True
)

AST_CLASS_PATH: str = parser_config[
    'ast_class'
]  # Abstract Syntax Tree classpath to import, by default - fastpy.parser.ast.AST

PARSER_CLASS_PATH: str = parser_config[
    'parser_class'
]  # main parser classpath to import, by default - fastpy.parser.parsers.Parser

NODE_PARSING: dict = parser_config.get('node_parsing', {})  # node parsing data

operators_config = JsonConfig(
    filepath=os.path.join(CONFIG_FOLDER, 'operators.json'),
    authoload=True
)

BIN_OP_NAMES: list = operators_config['binary_operator_names']  # names of binary operators
LOGIC_OP_NAMES: list = operators_config['logic_operator_names']  # names of logic operators
