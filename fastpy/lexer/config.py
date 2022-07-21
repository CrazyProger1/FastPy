from ..config import JsonConfig, CONFIG_FOLDER
import os

lexer_config = JsonConfig(os.path.join(CONFIG_FOLDER, 'lexer.json'), authoload=True)
