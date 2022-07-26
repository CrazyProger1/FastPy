from ..config import JsonConfig, CONFIG_FOLDER
from fastpy.import_tools import import_class
import os
import pydoc

lexer_config = JsonConfig(
    filepath=os.path.join(CONFIG_FOLDER, 'lexer.json'),
    authoload=True
)

COMMENT_START_SYMBOL = lexer_config['comment_start']
TOKEN_CLASS_PATH = lexer_config['token_class']  # Token classpath to import, by default - fastpy.lexer.tokens.Token
LEXER_CLASS_PATH = lexer_config['lexer_class']  # Lexer classpath to import, by default - fastpy.lexer.tokens.Token
TOKEN_DETECTION = lexer_config.get('token_detection', {})  # token detection data

operators_config = JsonConfig(
    filepath=os.path.join(CONFIG_FOLDER, 'operators.json'),
    authoload=True
)

OPERATORS = operators_config['operators']  # dict of operators and it names
SIMILAR_OPERATORS = operators_config['similar_operators']  # dict of operators and lists of similar operators
