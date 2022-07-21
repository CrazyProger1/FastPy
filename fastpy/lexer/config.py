from ..config import JsonConfig, CONFIG_FOLDER
import os

lexer_config = JsonConfig(
    filepath=os.path.join(CONFIG_FOLDER, 'lexer.json'),
    authoload=True
)

operators_config = JsonConfig(
    filepath=os.path.join(CONFIG_FOLDER, 'operators.json'),
    authoload=True
)

OPERATORS = operators_config['operators']
