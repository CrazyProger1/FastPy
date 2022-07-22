from ..config import JsonConfig, CONFIG_FOLDER
import os

parser_config = JsonConfig(
    filepath=os.path.join(CONFIG_FOLDER, 'parser.json'),
    authoload=True
)

AST_CLASS_PATH = parser_config['ast_class']  # Abstract Syntax Tree class path to import
PARSER_CLASS_PATH = parser_config['parser_class']  # Main parser class path to import
NODE_PARSING = parser_config.get('node_parsing', {})  # Node parsing info
