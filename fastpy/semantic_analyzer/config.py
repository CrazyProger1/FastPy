from ..config import JsonConfig, CONFIG_FOLDER
import os

analyzer_config = JsonConfig(
    filepath=os.path.join(CONFIG_FOLDER, 'analyzer.json'),
    authoload=True
)

ANALYZER_CLASS_PATH: str = analyzer_config['semantic_analyzer_class']  # analyzer class path to import
NODE_ANALYZING: dict = analyzer_config['node_analyzing']
