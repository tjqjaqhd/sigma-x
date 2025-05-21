"""플러그인 로더."""

from importlib import import_module
from pathlib import Path

from sigma.utils.logger import logger


def load_plugins(directory: str = "plugins") -> None:
    """plugins 디렉터리의 모듈을 동적으로 로드합니다."""

    plugin_path = Path(directory)
    if not plugin_path.exists():
        logger.warning("플러그인 디렉터리가 존재하지 않습니다: %s", directory)
        return

    for file in plugin_path.glob("*.py"):
        if file.name == "__init__.py":
            continue
        module_name = f"{directory.replace('/', '.')}" + f".{file.stem}"
        try:
            import_module(module_name)
            logger.info("플러그인 로드: %s", module_name)
        except Exception as exc:  # pragma: no cover - 로드 실패 경로
            logger.exception("플러그인 로드 실패: %s", exc)

    logger.info("플러그인 로드 완료")
