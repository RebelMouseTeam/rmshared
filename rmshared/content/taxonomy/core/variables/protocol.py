import re

from typing import Any
from typing import Callable
from typing import Mapping
from typing import Type
from typing import TypeVar

from rmshared.tools import invert_dict
from rmshared.tools import map_dict
from rmshared.tools import unless_none
from rmshared.typings import read_only

from rmshared.content.taxonomy import protocols as base_protocols
from rmshared.content.taxonomy.core import filters
from rmshared.content.taxonomy.core import orders
from rmshared.content.taxonomy.core import labels
from rmshared.content.taxonomy.core import ranges
from rmshared.content.taxonomy.core import fields
from rmshared.content.taxonomy.core import protocol
from rmshared.content.taxonomy.core.variables import arguments
from rmshared.content.taxonomy.core.variables import operators
from rmshared.content.taxonomy.core.variables import values
from rmshared.content.taxonomy.core.variables.abc import Argument
from rmshared.content.taxonomy.core.variables.abc import Operator
from rmshared.content.taxonomy.core.variables.abc import Reference
from rmshared.content.taxonomy.core.variables.abc import IProtocol

T = TypeVar('T')


class Factory:
    def __init__(self):
        self.delegate = protocol.Factory()  # TODO: inject as an interface
        self.variables = self.Variables()
        self.operators = self.Operators(self.variables)

    def make_protocol(self) -> IProtocol:
        builder = base_protocols.Builder()
        builder.customize_filters(self.make_filters, dependencies=(base_protocols.ILabels, base_protocols.IRanges))
        builder.customize_orders(self.make_orders, dependencies=(base_protocols.IFields,))
        builder.customize_labels(self.make_labels, dependencies=(base_protocols.IFields, base_protocols.IValues))
        builder.customize_ranges(self.make_ranges, dependencies=(base_protocols.IFields, base_protocols.IValues))
        builder.customize_fields(self.make_fields, dependencies=())
        builder.customize_values(self.make_values, dependencies=())
        instance = builder.make_protocol()
        instance = self.Protocol(instance, self.variables)
        return instance

    def make_filters(self, labels_: base_protocols.ILabels, ranges_: base_protocols.IRanges) -> base_protocols.IFilters[Operator[filters.Filter]]:
        delegate = self.delegate.make_filters(labels_, ranges_)
        instance = base_protocols.Filters()
        # TODO: consider `fallback = base_protocols.fallbacks.Filters(delegate=delegate, fallback=instance)` for {'$switch': {...: {'$<operator>': ...}}}
        instance.add_filter(operators.Switch[filters.Filter], self.SwitchFiltersProtocol(delegate, self.operators))
        # TODO: consider `instance.add_filter(operators.Return[filters.Filter], self.ReturnFiltersProtocol(delegate, self.operators))` for {'$return': ...}
        return base_protocols.fallbacks.Filters(delegate=instance, fallback=self.ReturnFiltersFallback(delegate), exceptions=(LookupError,))

    def make_orders(self, fields_: base_protocols.IFields) -> base_protocols.IOrders[orders.Order]:
        return self.delegate.make_orders(fields_)

    def make_labels(self, fields_: base_protocols.IFields, values_: base_protocols.IValues) -> base_protocols.ILabels[Operator[labels.Label]]:
        delegate = self.delegate.make_labels(fields_, values_)
        instance = base_protocols.Labels()
        # TODO: consider `fallback = base_protocols.fallbacks.Labels(delegate=delegate, fallback=instance)` for {'$switch': {...: {'$<operator>': ...}}}
        instance.add_label(operators.Switch[labels.Label], self.SwitchLabelsProtocol(delegate, self.operators))
        # TODO: consider `instance.add_label(operators.Return[labels.Label], self.ReturnLabelsProtocol(delegate, self.operators))` for {'$return': ...}
        return base_protocols.fallbacks.Labels(delegate=instance, fallback=self.ReturnLabelsFallback(delegate), exceptions=(LookupError,))

    def make_ranges(self, fields_: base_protocols.IFields, values_: base_protocols.IValues) -> base_protocols.IRanges[Operator[ranges.Range]]:
        delegate = self.delegate.make_ranges(fields_, values_)
        instance = base_protocols.Ranges()
        # TODO: consider `fallback = base_protocols.fallbacks.Ranges(delegate=delegate, fallback=instance)` for {'$switch': {...: {'$<operator>': ...}}}
        instance.add_range(operators.Switch[ranges.Range], self.SwitchRangesProtocol(delegate, self.operators))
        # TODO: consider `instance.add_range(operators.Return[ranges.Range], self.ReturnRangesProtocol(delegate, self.operators))` for {'$return': ...}
        return base_protocols.fallbacks.Ranges(delegate=instance, fallback=self.ReturnRangesFallback(delegate), exceptions=(LookupError,))

    def make_fields(self) -> base_protocols.IFields[fields.Field]:
        return self.delegate.make_fields()

    def make_values(self) -> base_protocols.IValues:
        instance = base_protocols.Values()
        instance.add_value(self.VariableValueProtocol(self.variables))
        instance.add_value(self.ConstantValueProtocol(self.delegate.make_values()))
        return instance

    class SwitchFiltersProtocol(base_protocols.composites.IFilters.IProtocol[operators.Switch[filters.Filter]]):
        def __init__(self, delegate: base_protocols.IFilters[filters.Filter], operators_: 'Factory.Operators'):
            self.delegate = delegate
            self.operators = operators_

        def get_keys(self):
            return self.operators.get_switch_keys()

        def make_filter(self, data) -> operators.Switch[filters.Filter]:
            return self.operators.make_switch(data, self.delegate.make_filter)

        def jsonify_filter(self, filter_: operators.Switch[filters.Filter]):
            return self.operators.jsonify_switch(filter_, self.delegate.jsonify_filter)

    class ReturnFiltersProtocol(base_protocols.composites.IFilters.IProtocol[operators.Return[filters.Filter]]):
        def __init__(self, delegate: base_protocols.IFilters[filters.Filter], operators_: 'Factory.Operators'):
            self.delegate = delegate
            self.operators = operators_

        def get_keys(self):
            return self.operators.get_return_keys()

        def make_filter(self, data) -> operators.Return[filters.Filter]:
            return self.operators.make_return(data, self.delegate.make_filter)

        def jsonify_filter(self, filter_: operators.Return[filters.Filter]):
            return self.operators.jsonify_return(filter_, self.delegate.jsonify_filter)

    class ReturnFiltersFallback(base_protocols.IFilters[Operator[filters.Filter]]):
        def __init__(self, delegate: base_protocols.IFilters[filters.Filter]):
            self.delegate = delegate

        def make_filter(self, data) -> operators.Return[filters.Filter]:
            return operators.Return[filters.Filter](cases=(self.delegate.make_filter(data),))

        def jsonify_filter(self, filter_: Operator[filters.Filter]):
            assert isinstance(filter_, operators.Return)
            assert len(filter_.cases) == 1, filter_
            return self.delegate.jsonify_filter(filter_.cases[0])

    class SwitchLabelsProtocol(base_protocols.composites.ILabels.IProtocol[operators.Switch[labels.Label]]):
        def __init__(self, delegate: base_protocols.ILabels[labels.Label], operators_: 'Factory.Operators'):
            self.delegate = delegate
            self.operators = operators_

        def get_keys(self):
            return self.operators.get_switch_keys()

        def make_label(self, data) -> operators.Switch[labels.Label]:
            return self.operators.make_switch(data, self.delegate.make_label)

        def jsonify_label(self, label_: operators.Switch[labels.Label]):
            return self.operators.jsonify_switch(label_, self.delegate.jsonify_label)

    class ReturnLabelsProtocol(base_protocols.composites.ILabels.IProtocol[operators.Return[labels.Label]]):
        def __init__(self, delegate: base_protocols.ILabels[labels.Label], operators_: 'Factory.Operators'):
            self.delegate = delegate
            self.operators = operators_

        def get_keys(self):
            return self.operators.get_return_keys()

        def make_label(self, data) -> operators.Return[labels.Label]:
            return self.operators.make_return(data, self.delegate.make_label)

        def jsonify_label(self, label_: operators.Return[labels.Label]):
            return self.operators.jsonify_return(label_, self.delegate.jsonify_label)

    class ReturnLabelsFallback(base_protocols.ILabels[Operator[labels.Label]]):
        def __init__(self, delegate: base_protocols.ILabels[labels.Label]):
            self.delegate = delegate

        def make_label(self, data) -> operators.Return[labels.Label]:
            return operators.Return[labels.Label](cases=(self.delegate.make_label(data),))

        def jsonify_label(self, label: Operator[labels.Label]):
            assert isinstance(label, operators.Return)
            assert len(label.cases) == 1, label
            return self.delegate.jsonify_label(label.cases[0])

    class SwitchRangesProtocol(base_protocols.composites.IRanges.IProtocol[operators.Switch[ranges.Range]]):
        def __init__(self, delegate: base_protocols.IRanges[ranges.Range], operators_: 'Factory.Operators'):
            self.delegate = delegate
            self.operators = operators_

        def get_keys(self):
            return self.operators.get_switch_keys()

        def make_range(self, data) -> operators.Switch[ranges.Range]:
            return self.operators.make_switch(data, self.delegate.make_range)

        def jsonify_range(self, range_: operators.Switch[ranges.Range]):
            return self.operators.jsonify_switch(range_, self.delegate.jsonify_range)

    class ReturnRangesProtocol(base_protocols.composites.IRanges.IProtocol[operators.Return[ranges.Range]]):
        def __init__(self, delegate: base_protocols.IRanges[ranges.Range], operators_: 'Factory.Operators'):
            self.delegate = delegate
            self.operators = operators_

        def get_keys(self):
            return self.operators.get_return_keys()

        def make_range(self, data) -> operators.Return[ranges.Range]:
            return self.operators.make_return(data, self.delegate.make_range)

        def jsonify_range(self, range_: operators.Return[ranges.Range]):
            return self.operators.jsonify_return(range_, self.delegate.jsonify_range)

    class ReturnRangesFallback(base_protocols.IRanges[Operator[ranges.Range]]):
        def __init__(self, delegate: base_protocols.IRanges[ranges.Range]):
            self.delegate = delegate

        def make_range(self, data) -> operators.Return[ranges.Range]:
            return operators.Return[ranges.Range](cases=(self.delegate.make_range(data),))

        def jsonify_range(self, range_: Operator[ranges.Range]):
            assert isinstance(range_, operators.Return)
            assert len(range_.cases) == 1, range_
            return self.delegate.jsonify_range(range_.cases[0])

    class VariableValueProtocol(base_protocols.composites.IValues.IProtocol[values.Variable]):
        def __init__(self, variables: 'Factory.Variables'):
            self.variables = variables

        def get_types(self):
            return {values.Variable}

        def make_value(self, data: Any) -> values.Variable:
            ref, index = self.variables.make_variable(data=str(data))
            return values.Variable(ref, index)

        def jsonify_value(self, value: values.Variable) -> str:
            return self.variables.jsonify_variable(value.ref, value.index)

    class ConstantValueProtocol(base_protocols.composites.IValues.IProtocol[values.Constant]):
        def __init__(self, delegate: base_protocols.IValues[ranges.Range]):
            self.delegate = delegate

        def get_types(self):
            return {values.Constant}

        def make_value(self, data) -> values.Constant:
            return values.Constant(value=self.delegate.make_value(data))

        def jsonify_value(self, value: values.Constant):
            return self.delegate.jsonify_value(value.value)

    class Operators:
        def __init__(self, variables: 'Factory.Variables'):
            self.variables = variables

        @staticmethod
        def get_switch_keys():
            return {'$switch'}

        def make_switch(self, data: Mapping[str, Any], make_case: Callable[[Any], T]) -> operators.Switch[T]:
            def make_return(operator_data: Any) -> operators.Return[T]:
                return operators.Return(cases=tuple(map(make_case, operator_data)))

            return operators.Switch[T](
                ref=self.variables.make_reference(data['$switch']['$ref']),
                cases=read_only(self._make_cases(data['$switch']['$cases'], make_return)),
            )

        def jsonify_switch(self, operator: operators.Switch[T], jsonify_case: Callable[[T], Any]) -> Mapping[str, Any]:
            def jsonify_operator(operator_: Operator[T]) -> Any:
                assert isinstance(operator_, operators.Return)
                return list(map(jsonify_case, operator_.cases))

            return {'$switch': {
                '$ref': self.variables.jsonify_reference(operator.ref),
                '$cases': self._jsonify_cases(operator.cases, jsonify_operator),
            }}

        def _make_cases(self, data, make_case):
            return map_dict(data, map_key_func=self.variables.make_argument, map_value_func=make_case)

        def _jsonify_cases(self, cases, jsonify_case):
            return map_dict(cases, map_key_func=self.variables.jsonify_argument, map_value_func=jsonify_case)

        @staticmethod
        def get_return_keys():
            return {'$return'}

        @staticmethod
        def make_return(data: Mapping[str, Any], make_case: Callable[[Any], T]) -> operators.Return[T]:
            return operators.Return[T](
                cases=tuple(map(make_case, data['$return']))
            )

        @staticmethod
        def jsonify_return(operator: operators.Return[T], jsonify_case: Callable[[T], Any]) -> Mapping[str, Any]:
            return {'$return': list(map(jsonify_case, operator.cases))}

    class Protocol(IProtocol):
        def __init__(self, delegate: base_protocols.IProtocol, variables: 'Factory.Variables'):
            self.delegate = delegate
            self.variables = variables

        def make_filters(self, data):
            return self.delegate.make_filters(data)

        def jsonify_filters(self, filters_):
            return self.delegate.jsonify_filters(filters_)

        def make_order(self, data):
            return self.delegate.make_order(data)

        def jsonify_order(self, order):
            return self.delegate.jsonify_order(order)

        def make_field(self, data):
            return self.delegate.make_field(data)

        def jsonify_field(self, field):
            return self.delegate.jsonify_field(field)

        def make_event(self, data):
            return self.delegate.make_event(data)

        def jsonify_event(self, event):
            return self.delegate.jsonify_event(event)

        def make_argument(self, data):
            return self.variables.make_argument(data)

        def jsonify_argument(self, argument):
            return self.variables.jsonify_argument(argument)

    class Variables:
        ALIAS_REGEX = re.compile(r'^\$(?P<alias>\$\d+)$')
        VALUE_REGEX = re.compile(r'^\$(?P<alias>\$\d+)(?:\[(?P<index>\d+)])?$')

        def __init__(self):
            self.argument_to_argument_name_map: Mapping[Type[Argument], str] = {
                arguments.Value: '$',
                arguments.Empty: '$none',
                arguments.Any: '$any',
            }
            self.argument_name_to_argument_map = invert_dict(self.argument_to_argument_name_map)

        def make_argument(self, data):
            return self.argument_name_to_argument_map[data]

        def jsonify_argument(self, argument):
            return self.argument_to_argument_name_map[argument]

        def make_reference(self, data):
            if isinstance(data, str) and (match := self.ALIAS_REGEX.match(data)):
                return Reference(alias=match.group('alias'))
            else:
                raise ValueError(['invalid_reference', data])

        @staticmethod
        def jsonify_reference(ref: Reference) -> str:
            return f'${ref.alias}'

        def make_variable(self, data):
            if isinstance(data, str) and (match := self.VALUE_REGEX.match(data)):
                alias = str(match.group('alias'))
                index = unless_none(int, if_none=1)(match.group('index'))
                return Reference(alias=alias), index
            else:
                raise ValueError(['invalid_variable', data])

        @staticmethod
        def jsonify_variable(ref: Reference, index: int) -> str:
            return f'${ref.alias}[{index}]'
