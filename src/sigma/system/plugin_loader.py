"""플러그인 로더."""

from importlib import import_module
from pathlib import Path
from src.sigma.utils.logger import logger
from src.sigma.plugins.plugin_base import PluginBase
import inspect

plugins = []


def load_plugins(directory: str = "sigma/plugins") -> None:
    """sigma/plugins 디렉터리의 PluginBase 상속 플러그인을 동적으로 로드 및 등록/실행한다."""
    plugin_path = Path(directory)
    if not plugin_path.exists():
        logger.warning("플러그인 디렉터리가 존재하지 않습니다: %s", directory)
        return
    for file in plugin_path.glob("*.py"):
        if file.name == "__init__.py" or file.name == "plugin_base.py":
            continue
        module_name = f"{directory.replace('/', '.')}" + f".{file.stem}"
        try:
            module = import_module(module_name)
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, PluginBase) and obj is not PluginBase:
                    plugin_instance = obj()
                    plugins.append(plugin_instance)
                    plugin_instance.on_load()
                    logger.info("플러그인 로드 및 on_load 실행: %s", obj.__name__)
        except Exception as exc:
            logger.exception("플러그인 로드 실패: %s", exc)
    logger.info("플러그인 로드 완료")


def run_all_plugins(*args, **kwargs):
    for plugin in plugins:
        try:
            plugin.run(*args, **kwargs)
            logger.info("플러그인 실행: %s", plugin.name)
        except Exception as exc:
            logger.exception("플러그인 실행 실패: %s", exc)
