from __future__ import annotations

import importlib
import os
from types import ModuleType
from typing import Type

from .strategy import BaseStrategy


def _find_strategy_class(module: ModuleType) -> Type[BaseStrategy]:
    """모듈에서 BaseStrategy 서브클래스를 탐색한다."""
    for obj in module.__dict__.values():
        if isinstance(obj, type) and issubclass(obj, BaseStrategy) and obj is not BaseStrategy:
            return obj
    raise ImportError("No strategy class found")


def load_strategy(name: str, package: str = "src.strategies") -> BaseStrategy:
    """지정한 이름의 전략 클래스를 로드해 인스턴스로 반환한다."""
    module = importlib.import_module(f"{package}.{name}")
    cls = _find_strategy_class(module)
    return cls()


def list_strategies(package: str = "src.strategies") -> list[str]:
    """패키지 내 존재하는 전략 모듈 목록을 반환한다."""
    spec = importlib.util.find_spec(package)
    if spec is None or not spec.submodule_search_locations:
        return []
    directory = spec.submodule_search_locations[0]
    result = []
    for fname in os.listdir(directory):
        if fname.startswith("_") or not fname.endswith(".py"):
            continue
        result.append(fname[:-3])
    return sorted(result)
