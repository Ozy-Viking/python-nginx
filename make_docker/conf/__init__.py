import os
from pathlib import Path
import sys
import importlib


class Setting:
    def __init__(self, mod_path=None):
        if mod_path is None:
            mod_path = os.environ.get("MAKE_DOCKER_SETTINGS", "make_docker.settings")
        self.MAKE_DOCKER_SETTINGS: str = mod_path

        # deepcode ignore AttributeLoadOnNone: None is blocked.
        if self.MAKE_DOCKER_SETTINGS.split(".")[0] in sys.modules:
            # deepcode ignore CodeInjection: If statement validates settings module name.
            settings_module = importlib.import_module(mod_path)
            active_settings_name = [x for x in dir(settings_module) if x.isupper()]
            active_setting_items: dict[str, str] = dict()
            for key in active_settings_name:
                active_setting_items[key] = settings_module.__getattribute__(key)
        else:
            raise ImportError("Invalid MAKE_DOCKER_SETTINGS environment varable.")
        self.__dict__ = active_setting_items
        self.__dir__: list[str] = dir(self) + list(active_setting_items.keys())


setting = Setting()

BASE_PATH: Path = Path(__file__).parent.parent.parent
BUILD_PATH: Path = BASE_PATH / "build"
NGINX_BUILD: Path = BUILD_PATH / "nginx"

__all__: list[str] = [
    "BASE_PATH",
    "BUILD_PATH",
    "NGINX_BUILD",
    "setting",
]
