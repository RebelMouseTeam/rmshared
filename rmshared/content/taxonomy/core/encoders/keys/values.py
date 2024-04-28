from typing import Any

from rmshared.content.taxonomy.core.encoders.abc import IValues


class Values(IValues[Any, str]):
    def encode_value(self, value):
        return str(value)
