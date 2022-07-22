from ..config import JsonConfig, CONFIG_FOLDER
import os

parser_config = JsonConfig(
    filepath=os.path.join(CONFIG_FOLDER, 'parser.json'),
    authoload=True
)

AST_CLASS_PATH = parser_config['ast_class']
PARSER_CLASS_PATH = parser_config['parser_class']
NODE_PARSING = parser_config.get('node_parsing', {})
