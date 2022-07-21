from ..config import JsonConfig, CONFIG_FOLDER
from fastpy.import_tools import import_class
import os
import pydoc

lexer_config = JsonConfig(
    filepath=os.path.join(CONFIG_FOLDER, 'lexer.json'),
    authoload=True
)

COMMENT_START_SYMBOL = lexer_config['comment_start']
TOKEN_CLASS = lexer_config['token_class']
LEXER_CLASS = lexer_config['lexer_class']
TOKEN_DETECTION = lexer_config.get('tokens_detection', {})

operators_config = JsonConfig(
    filepath=os.path.join(CONFIG_FOLDER, 'operators.json'),
    authoload=True
)

OPERATORS = operators_config['operators']
SIMILAR_OPERATORS = operators_config['similar_operators']
