import os
import json
from .config import *


class JsonConfig(Config):
    def __init__(self, filepath: str, authoload: bool = True):
        self._filepath = None
        self._config = None
        self._config_type: type[list | dict] | None = None

        self.set_filepath(filepath)

        if authoload:
            self.load()

    @property
    def type(self):
        return self._config_type

    def set_filepath(self, filepath: str) -> None:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f'File "{filepath}" not found')

        self._filepath = filepath

    def load(self):
        with open(self._filepath, 'r') as cf:
            self._config = json.load(cf)
            self._config_type = type(self._config)

    def save(self):
        with open(self._filepath, 'w') as cf:
            if self._config:
                json.dump(self._config, cf)

    def __getitem__(self, item) -> any:
        if self._config:
            return self._config[item]
        else:
            raise

    def __iter__(self):
        if issubclass(self._config_type, dict):
            return iter(self._config.items())

        elif issubclass(self._config_type, list):
            return iter(self._config)

    def __repr__(self):
        if self._config:
            return json.dumps(self._config, indent=4, sort_keys=True)

        return 'Not loaded'
