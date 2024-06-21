"""
JSON settings parser
"""
import json
from os import path, getenv


class Settings:
    def __init__(self, _path: str = path.join(path.dirname(path.dirname(path.dirname(__file__))), 'settings.json')):
        self._path = _path

        for key, value in self._load().items():
            self.__dict__[key] = value

        if len(self.__dict__['cookie_path']) == 0:
            self.__dict__['cookie_path'] = f"{getenv('LOCALAPPDATA')}/Google/Chrome/User Data"

    def _load(self) -> dict:
        with open(self._path, "r", encoding="utf-8") as file:
            return json.load(file)

