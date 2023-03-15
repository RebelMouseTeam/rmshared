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

from rmshared.content.taxonomy.core0 import server as core0_server
from rmshared.content.taxonomy.core0.abc import Label
from rmshared.content.taxonomy.core0.abc import Range
from rmshared.content.taxonomy.core0.abc import Filter

from rmshared.content.taxonomy.core0.variables import ranges
from rmshared.content.taxonomy.core0.variables import labels
from rmshared.content.taxonomy.core0.variables import filters
from rmshared.content.taxonomy.core0.variables import arguments
from rmshared.content.taxonomy.core0.variables.abc import Cases
from rmshared.content.taxonomy.core0.variables.abc import Argument
from rmshared.content.taxonomy.core0.variables.abc import Constant
from rmshared.content.taxonomy.core0.variables.abc import Reference
from rmshared.content.taxonomy.core0.variables.abc import Variable
from rmshared.content.taxonomy.core0.variables.abc import IProtocol


class Protocol(IProtocol, core0_server.Protocol):
    Case = TypeVar('Case')

    def __init__(self):
        super().__init__()
        self.filters = self.Filters(self)
        self.labels = self.Labels(self)
        self.ranges = self.Ranges(self)
        self.arguments = self.Arguments()
        self.variables = self.Variables()

    def make_argument(self, data: str) -> Type[Argument]:
        return self.arguments.make_argument(data)

    def jsonify_argument(self, argument: Type[Argument]) -> str:
        return self.arguments.jsonify_argument(argument)

    def _make_cases(self, data: Mapping[str, Any], make_case: Callable[[Any], 'Protocol.Case']):
        case_map = map_dict(data, map_key_func=self.arguments.make_argument, map_value_func=make_case)
        return Cases(cases=read_only(case_map))

    def _jsonify_cases(self, cases: Cases, jsonify_case: Callable[['Protocol.Case'], Any]) -> Mapping[str, Any]:
        return dict(map_dict(cases.cases, map_key_func=unless_none(self.arguments.jsonify_argument), map_value_func=jsonify_case))

    class Filters(core0_server.Protocol.Filters):
        def __init__(self, protocol: 'Protocol'):
            super().__init__(protocol)
            self.protocol = cast('Protocol', self.protocol)
            self.filter_to_filter_name_map = merge_dicts(self.filter_to_filter_name_map, {
                filters.Switch: '$switch',
            })
            self.filter_name_to_filter_map = merge_dicts(self.filter_name_to_filter_map, invert_dict(self.filter_to_filter_name_map))
            self.filter_to_factory_func_map = merge_dicts(self.filter_to_factory_func_map, {
                filters.Switch: self._make_switch_filter,
            })
            self.filter_to_jsonify_func_map = merge_dicts(self.filter_to_jsonify_func_map, {
                filters.Switch: self._jsonify_switch_filter_info,
            })

        def _make_switch_filter(self, data: Mapping[str, Any]) -> filters.Switch:
            return filters.Switch(
                ref=self.protocol.variables.make_reference(data['$ref']),
                cases=self.protocol._make_cases(data['$cases'], self._make_case),
            )

        def _jsonify_switch_filter_info(self, filter_: filters.Switch) -> Mapping[str, Any]:
            return {
                '$ref': self.protocol.variables.jsonify_reference(filter_.ref),
                '$cases': self.protocol._jsonify_cases(filter_.cases, self._jsonify_case),
            }

        def _make_case(self, data: Sequence[Mapping[str, Any]]) -> Sequence[Filter]:
            return list(map(self.make_filter, data))

        def _jsonify_case(self, filters_: Sequence[Filter]) -> Sequence[Mapping[str, Any]]:
            return list(map(self.jsonify_filter, filters_))

    class Labels(core0_server.Protocol.Labels):
        def __init__(self, protocol: 'Protocol'):
            super().__init__(protocol)
            self.protocol = cast('Protocol', self.protocol)
            self.label_to_label_name_map = merge_dicts(self.label_to_label_name_map, {
                labels.Value: 'value',
                labels.Switch: '$switch',
            })
            self.label_name_to_label_map = merge_dicts(self.label_name_to_label_map, invert_dict(self.label_to_label_name_map))
            self.label_to_factory_func_map = merge_dicts(self.label_to_factory_func_map, {
                labels.Value: self._make_value_label,
                labels.Switch: self._make_switch_label,
            })
            self.label_to_jsonify_func_map = merge_dicts(self.label_to_jsonify_func_map, {
                labels.Value: self._jsonify_value_variable_label_info,
                labels.Switch: self._jsonify_switch_label_info,
            })

        def _make_value_label(self, data: Mapping[str, Any]) -> Label:
            if str(data['value']).startswith('$'):
                field = self.protocol.fields.make_field(data['field'])
                value = self.protocol.variables.make_variable(data['value'])
                return labels.Value(field, value)
            else:
                return super()._make_value_label(data)

        def _jsonify_value_variable_label_info(self, label: labels.Value) -> Mapping[str, Any]:
            return {
                'field': self.protocol.fields.jsonify_field(label.field),
                'value': self.protocol.variables.jsonify_variable(label.value),
            }

        def _make_switch_label(self, data: Mapping[str, Any]) -> labels.Switch:
            return labels.Switch(
                ref=self.protocol.variables.make_reference(data['$ref']),
                cases=self.protocol._make_cases(data['$cases'], self._make_case),
            )

        def _jsonify_switch_label_info(self, label: labels.Switch) -> Mapping[str, Any]:
            return {
                '$ref': self.protocol.variables.jsonify_reference(label.ref),
                '$cases': self.protocol._jsonify_cases(label.cases, self._jsonify_case),
            }

        def _make_case(self, data: Sequence[Mapping[str, Any]]) -> Sequence[Label]:
            return list(map(self._make_label, data))

        def _jsonify_case(self, labels_: Sequence[Label]) -> Sequence[Mapping[str, Any]]:
            return list(map(self.jsonify_label, labels_))

    class Ranges(core0_server.Protocol.Ranges):
        def __init__(self, protocol: 'Protocol'):
            super().__init__(protocol)
            self.protocol = cast('Protocol', self.protocol)
            self.range_to_jsonify_func_map = merge_dicts(self.range_to_jsonify_func_map, {
                ranges.LessThan: self._jsonify_less_than_variable_range,
                ranges.MoreThan: self._jsonify_more_than_variable_range,
                ranges.Between: self._jsonify_between_variable_range,
                ranges.Switch: self._jsonify_switch_range,
            })

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

        def _jsonify_switch_range(self, range_: ranges.Switch) -> Mapping[str, Any]:
            return {
                '$switch': {
                    '$ref': self.protocol.variables.jsonify_reference(range_.ref),
                    '$cases': self.protocol._jsonify_cases(range_.cases, self._jsonify_case),
                },
            }

        def _make_case(self, data: Sequence[Mapping[str, Any]]) -> Sequence[Range]:
            return list(map(self._make_range, data))

        def _jsonify_case(self, ranges_: Sequence[Range]) -> Sequence[Mapping[str, Any]]:
            return list(map(self.jsonify_range, ranges_))

        def _make_less_than_range(self, data: Mapping[str, Any]) -> Range:
            if str(data['max']).startswith('$'):
                field = self.protocol.fields.make_field(data['field'])
                value = self.protocol.variables.make_variable(data['max'])
                return ranges.LessThan(field, value)
            else:
                return super()._make_less_than_range(data)

        def _jsonify_less_than_variable_range(self, range_: ranges.LessThan) -> Mapping[str, Any]:
            return {
                'field': self.protocol.fields.jsonify_field(range_.field),
                'max': self.protocol.variables.jsonify_variable(range_.value),
            }

        def _make_more_than_range(self, data: Mapping[str, Any]) -> Range:
            if str(data['min']).startswith('$'):
                field = self.protocol.fields.make_field(data['field'])
                value = self.protocol.variables.make_variable(data['min'])
                return ranges.MoreThan(field, value)
            else:
                return super()._make_more_than_range(data)

        def _jsonify_more_than_variable_range(self, range_: ranges.MoreThan) -> Mapping[str, Any]:
            return {
                'field': self.protocol.fields.jsonify_field(range_.field),
                'min': self.protocol.variables.jsonify_variable(range_.value),
            }

        def _make_between_range(self, data: Mapping[str, Any]) -> Range:
            if str(data['min']).startswith('$') or str(data['max']).startswith('$'):
                field = self.protocol.fields.make_field(data['field'])
                min_value = self.protocol.variables.make_variable_or_constant(data['min'])
                max_value = self.protocol.variables.make_variable_or_constant(data['max'])
                return ranges.Between(field, min_value, max_value)
            else:
                return super()._make_between_range(data)

        def _jsonify_between_variable_range(self, range_: ranges.Between) -> Mapping[str, Any]:
            return {
                'field': self.protocol.fields.jsonify_field(range_.field),
                'min': self.protocol.variables.jsonify_variable_or_constant(range_.min_value),
                'max': self.protocol.variables.jsonify_variable_or_constant(range_.max_value),
            }

    class Arguments:
        def __init__(self):
            self.argument_to_argument_name_map: Mapping[Type[Argument], str] = {
                arguments.Value: '$',
                arguments.Empty: '$none',
                arguments.Any: '$any',
            }
            self.argument_name_to_argument_map = invert_dict(self.argument_to_argument_name_map)

        def make_argument(self, data: str) -> Type[Argument]:
            return self.argument_name_to_argument_map[data]

        def jsonify_argument(self, argument: Type[Argument]) -> str:
            return self.argument_to_argument_name_map[argument]

    class Variables:
        ALIAS_REGEX = re.compile(r'^\$(?P<alias>\$\d+)$')
        VALUE_REGEX = re.compile(r'^\$(?P<alias>\$\d+)(?:\[(?P<index>\d+)])?$')

        def make_reference(self, data: Any) -> Reference:
            if isinstance(data, str) and (match := self.ALIAS_REGEX.match(data)):
                return Reference(alias=match.group('alias'))
            else:
                raise ValueError(['invalid_reference', data])

        @staticmethod
        def jsonify_reference(ref: Reference) -> str:
            return f'${ref.alias}'

        def make_variable(self, data: Any) -> Variable:
            def fallback():
                raise ValueError(['invalid_reference_value', data])

            return self._make_variable_or(data, fallback)

        @staticmethod
        def jsonify_variable(variable: Variable) -> str:
            return f'${variable.ref.alias}[{variable.index}]'

        def make_variable_or_constant(self, data: Any) -> Variable | Constant:
            return self._make_variable_or(data, fallback=lambda: Constant(value=data))

        def _make_variable_or(self, data: Any, fallback: Callable[[], Constant]) -> Variable | Constant:
            if not isinstance(data, str):
                return fallback()
            elif match := self.VALUE_REGEX.match(data):
                alias = str(match.group('alias'))
                index = unless_none(int, if_none=1)(match.group('index'))
                return Variable(ref=Reference(alias), index=index)
            else:
                return fallback()

        def jsonify_variable_or_constant(self, variable_or_constant: Variable | Constant) -> Any:
            if isinstance(variable_or_constant, Constant):
                return variable_or_constant.value
            elif isinstance(variable_or_constant, Variable):
                return self.jsonify_variable(variable_or_constant)
            else:
                raise ValueError(variable_or_constant)
