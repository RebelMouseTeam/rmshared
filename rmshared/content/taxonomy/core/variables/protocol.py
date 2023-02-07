import re

from typing import Any
from typing import Callable
from typing import Mapping
from typing import Sequence
from typing import Type
from typing import TypeVar
from typing import cast

from rmshared.tools import invert_dict
from rmshared.tools import map_dict
from rmshared.tools import merge_dicts
from rmshared.tools import parse_name_and_info
from rmshared.tools import unless_none
from rmshared.typings import read_only

from rmshared.content.taxonomy.core import server as core_server
from rmshared.content.taxonomy.core.abc import Label
from rmshared.content.taxonomy.core.abc import Range
from rmshared.content.taxonomy.core.abc import Filter

from rmshared.content.taxonomy.core.variables import ranges
from rmshared.content.taxonomy.core.variables import labels
from rmshared.content.taxonomy.core.variables import filters
from rmshared.content.taxonomy.core.variables import arguments
from rmshared.content.taxonomy.core.variables.abc import Cases
from rmshared.content.taxonomy.core.variables.abc import Argument
from rmshared.content.taxonomy.core.variables.abc import Constant
from rmshared.content.taxonomy.core.variables.abc import Reference
from rmshared.content.taxonomy.core.variables.abc import Variable


class Protocol(core_server.Protocol):
    Case = TypeVar('Case')

    def __init__(self):
        super().__init__()
        self.filters = self.Filters(self)
        self.labels = self.Labels(self)
        self.ranges = self.Ranges(self)
        self.arguments = self.Arguments()
        self.variables = self.Variables()

    def _make_cases(self, data: Mapping[str, Any], make_case: Callable[[Any], 'Protocol.Case']):
        case_map = map_dict(data, map_key_func=self.arguments.make_argument, map_value_func=make_case)
        return Cases(cases=read_only(case_map))

    class Filters(core_server.Protocol.Filters):
        def __init__(self, protocol: 'Protocol'):
            super().__init__(protocol)
            self.protocol = cast('Protocol', self.protocol)
            self.filter_name_to_filter_map = merge_dicts(self.filter_name_to_filter_map, invert_dict({
                filters.Switch: '$switch',
            }))
            self.filter_to_factory_func_map = merge_dicts(self.filter_to_factory_func_map, {
                filters.Switch: self._make_switch_filter,
            })

        def _make_switch_filter(self, data: Mapping[str, Any]) -> filters.Switch:
            return filters.Switch(
                ref=self.protocol.variables.make_reference(data['$ref']),
                cases=self.protocol._make_cases(data['$cases'], self._make_case),
            )

        def _make_case(self, data: Sequence[Mapping[str, Any]]) -> Sequence[Filter]:
            return tuple(map(self.make_filter, data))

    class Labels(core_server.Protocol.Labels):
        def __init__(self, protocol: 'Protocol'):
            super().__init__(protocol)
            self.protocol = cast('Protocol', self.protocol)
            self.label_name_to_label_map = merge_dicts(self.label_name_to_label_map, invert_dict({
                labels.Value: 'value',
                labels.Switch: '$switch',
            }))
            self.label_to_factory_func_map = merge_dicts(self.label_to_factory_func_map, {
                labels.Value: self._make_value_label,
                labels.Switch: self._make_switch_label,
            })

        def _make_value_label(self, data: Mapping[str, Any]) -> Label:
            if str(data['value']).startswith('$'):
                field = self.protocol.fields.make_field(data['field'])
                value = self.protocol.variables.make_variable(data['value'])
                return labels.Value(field, value)
            else:
                return super()._make_value_label(data)

        def _make_switch_label(self, data: Mapping[str, Any]) -> labels.Switch:
            return labels.Switch(
                ref=self.protocol.variables.make_reference(data['$ref']),
                cases=self.protocol._make_cases(data['$cases'], self._make_case),
            )

        def _make_case(self, data: Sequence[Mapping[str, Any]]) -> Sequence[Label]:
            return tuple(map(self._make_label, data))

    class Ranges(core_server.Protocol.Ranges):
        def __init__(self, protocol: 'Protocol'):
            super().__init__(protocol)
            self.protocol = cast('Protocol', self.protocol)

        def _make_range(self, data: Mapping[str, Any]) -> Range:
            if frozenset(data.keys()) == frozenset({'$switch'}):
                _, info = parse_name_and_info(data)
                return self._make_switch_range(info)
            else:
                return super()._make_range(data)

        def _make_switch_range(self, data: Mapping[str, Any]) -> ranges.Switch:
            return ranges.Switch(
                ref=self.protocol.variables.make_reference(data['$ref']),
                cases=self.protocol._make_cases(data['$cases'], self._make_case),
            )

        def _make_case(self, data: Sequence[Mapping[str, Any]]) -> Sequence[Range]:
            return tuple(map(self._make_range, data))

        def _make_less_than_range(self, data: Mapping[str, Any]) -> Range:
            if str(data['max']).startswith('$'):
                field = self.protocol.fields.make_field(data['field'])
                value = self.protocol.variables.make_variable(data['max'])
                return ranges.LessThan(field, value)
            else:
                return super()._make_less_than_range(data)

        def _make_more_than_range(self, data: Mapping[str, Any]) -> Range:
            if str(data['min']).startswith('$'):
                field = self.protocol.fields.make_field(data['field'])
                value = self.protocol.variables.make_variable(data['min'])
                return ranges.MoreThan(field, value)
            else:
                return super()._make_more_than_range(data)

        def _make_between_range(self, data: Mapping[str, Any]) -> Range:
            if str(data['min']).startswith('$') or str(data['max']).startswith('$'):
                field = self.protocol.fields.make_field(data['field'])
                min_value = self.protocol.variables.make_variable_or_constant(data['min'])
                max_value = self.protocol.variables.make_variable_or_constant(data['max'])
                return ranges.Between(field, min_value, max_value)
            else:
                return super()._make_between_range(data)

    class Arguments:
        def __init__(self):
            self.argument_name_to_argument_map = invert_dict({
                arguments.Value: '$',
                arguments.Empty: '$none',
                arguments.Any: '$any',
            })

        def make_argument(self, data: str) -> Type[Argument]:
            return self.argument_name_to_argument_map[data]

    class Variables:
        ALIAS_REGEX = re.compile(r'^\$(?P<alias>\$\d+)$')
        VALUE_REGEX = re.compile(r'^\$(?P<alias>\$\d+)(?:\[(?P<index>\d+)])?$')

        def make_reference(self, data: Any) -> Reference:
            if isinstance(data, str) and (match := self.ALIAS_REGEX.match(data)):
                return Reference(alias=match.group('alias'))
            else:
                raise ValueError(['invalid_reference', data])

        def make_variable(self, data: Any) -> Variable:
            def fallback():
                raise ValueError(['invalid_reference_value', data])

            return self._make_variable_or(data, fallback)

        def make_variable_or_constant(self, data: Any) -> Variable | Constant:
            return self._make_variable_or(data, fallback=lambda: Constant(data))

        def _make_variable_or(self, data: Any, fallback: Callable[[], Constant]) -> Variable | Constant:
            if not isinstance(data, str):
                return fallback()
            elif match := self.VALUE_REGEX.match(data):
                alias = str(match.group('alias'))
                index = unless_none(int, if_none=1)(match.group('index'))
                return Variable(ref=Reference(alias), index=index)
            else:
                return fallback()
