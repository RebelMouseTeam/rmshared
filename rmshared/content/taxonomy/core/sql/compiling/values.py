from __future__ import annotations

from collections.abc import Mapping
from typing import Type
from typing import TypeVar

from rmshared.sql import compiling

from rmshared.content.taxonomy.core.sql.compiling.abc import IValues

S = TypeVar('S', str, int, float)


class Values(IValues[str | int | float]):
    def __init__(self):
        self.scalar_to_make_tree_func_map: Mapping[Type[S], compiling.MakeTreeFunc[S]] = {
            str: self._make_string,
            int: self._make_number,
            float: self._make_number,
        }

    def make_tree_from_value(self, value: str | int | float):
        return self.scalar_to_make_tree_func_map[type(value)](value)

    @staticmethod
    def _make_string(value: str) -> compiling.ITree:
        return compiling.terminals.String(value)

    @staticmethod
    def _make_number(value: int | float) -> compiling.ITree:
        return compiling.terminals.Number(value)
