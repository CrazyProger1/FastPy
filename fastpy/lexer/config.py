from ..config import JsonConfig, CONFIG_FOLDER
import os
import pydoc

lexer_config = JsonConfig(
    filepath=os.path.join(CONFIG_FOLDER, 'lexer.json'),
    authoload=True
)

COMMENT_START_SYMBOL = lexer_config['comment_start']
TOKEN_CLASS = lexer_config['token_class']
LEXER_CLASS = lexer_config['lexer_class']

operators_config = JsonConfig(
    filepath=os.path.join(CONFIG_FOLDER, 'operators.json'),
    authoload=True
)

OPERATORS = operators_config['operators']
