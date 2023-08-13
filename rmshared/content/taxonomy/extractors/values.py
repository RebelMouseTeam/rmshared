from typing import Any
from typing import Callable
from typing import Iterable
from typing import Mapping
from typing import Type
from typing import TypeVar

from rmshared.tools import ItemGetter

from rmshared.content.taxonomy import core

from rmshared.content.taxonomy.extractors.abc import Scalar
from rmshared.content.taxonomy.extractors.abc import IValuesExtractor

Field = TypeVar('Field', bound=core.fields.Field)


class ValuesExtractor(IValuesExtractor):
    def __init__(
            self,
            field_name_to_system_values_streamer_map: Mapping[str, Callable[[], Iterable[Scalar]]],
            field_name_to_custom_values_getter_map: Mapping[str, Callable[[], Mapping[str, Any]]]
    ):
        self.field_name_to_values_extractor_map = field_name_to_system_values_streamer_map
        self.field_name_to_custom_values_getter_map = field_name_to_custom_values_getter_map
        self.field_to_values_extractor_map: Mapping[Type[Field], Callable[[Field], Iterable[Scalar]]] = {
            core.fields.System: self._extract_system_field_values,
            core.fields.Custom: self._extract_custom_field_values,
        }

    def extract_values(self, field):
        return iter(self.field_to_values_extractor_map[type(field)](field))

    def _extract_system_field_values(self, field: core.fields.System) -> Iterable[Scalar]:
        return self.field_name_to_values_extractor_map[field.name]()

    def _extract_custom_field_values(self, field: core.fields.Custom) -> Iterable[Scalar]:
        try:
            item = ItemGetter(field.path)(self.field_name_to_custom_values_getter_map[field.name]())
        except LookupError:
            return []

        if isinstance(item, str):
            return [item]
        elif isinstance(item, Iterable):
            return filter(None, item)
        else:
            return filter(None, [item])
