from __future__ import annotations

from collections.abc import Callable
from collections.abc import Iterable
from collections.abc import Iterator
from collections.abc import Mapping
from collections.abc import Set
from typing import Type
from typing import TypeVar

from rmshared.tools import ensure_map_is_complete

from rmshared.content.taxonomy import core
from rmshared.content.taxonomy.variables import arguments
from rmshared.content.taxonomy.variables import operators
from rmshared.content.taxonomy.variables import values
from rmshared.content.taxonomy.variables.abc import Argument
from rmshared.content.taxonomy.variables.abc import Operator
from rmshared.content.taxonomy.variables.abc import Reference
from rmshared.content.taxonomy.variables.validation import exceptions
from rmshared.content.taxonomy.variables.validation.abc import IArguments
from rmshared.content.taxonomy.variables.validation.abc import IConstraint

A = TypeVar('A', bound=Argument)
O = TypeVar('O', bound=Operator)
R = TypeVar('R', bound=Reference)


class SwitchFilter(IConstraint):
    def __init__(self, arguments_: IArguments, filter_: operators.Switch[core.filters.Filter]):
        self.arguments = arguments_
        self.filter = filter_
        self.yield_to_validate_case_func: Mapping[Type[A], Callable[[O, R], None]] = ensure_map_is_complete(A, {
            arguments.Any: self._validate_any_yield_case,
            arguments.Empty: self._validate_empty_yield_case,
            arguments.Value: self._validate_value_yield_case,
        })
        self.finder = VariablesFinder()

    def validate(self):
        self._validate_switch_yields(self.filter)
        self._validate_nested_operators(self.filter)
        self._validate_cases()

    def _validate_switch_yields(self, operator: operators.Switch) -> None:
        valid_yields = frozenset(operator.cases.keys())
        actual_yields = self.arguments.get_yields(self.filter.ref)
        if valid_yields != actual_yields:
            raise self.InvalidArgumentYieldsError(operator.ref, valid_yields, actual_yields)

    def _validate_nested_operators(self, operator: operators.Switch) -> None:
        nested_operators = frozenset(map(type, operator.cases.values()))
        if nested_operators != {operators.Return}:
            raise self.NestedOperatorsNotSupportedError(operator)

    def _validate_cases(self) -> None:
        for yield_, return_filter in self.filter.cases.items():
            assert isinstance(return_filter, operators.Return)
            self.yield_to_validate_case_func[yield_](return_filter, self.filter.ref)
            self._validate_nested_variable_references(return_filter, self.filter.ref)

    def _validate_any_yield_case(self, return_filter: operators.Return, switch_ref: R) -> None:
        if switch_ref in self.finder.stream_variable_references(operator=return_filter):
            raise self.UndefinedAnyYieldVariableError(switch_ref)

    def _validate_empty_yield_case(self, return_filter: operators.Return, switch_ref: R) -> None:
        if switch_ref in self.finder.stream_variable_references(operator=return_filter):
            raise self.UndefinedEmptyYieldVariableError(switch_ref)

    def _validate_value_yield_case(self, return_filter: operators.Return, switch_ref: R) -> None:
        if switch_ref not in self.finder.stream_variable_references(operator=return_filter):
            raise self.MissingValueYieldVariableError(switch_ref)

    def _validate_nested_variable_references(self, operator: operators.Return, switch_ref: R) -> None:
        for ref in self.finder.stream_variable_references(operator):
            if ref == switch_ref:
                continue

            yields = self.arguments.get_yields(ref)
            if yields != ReturnFilter.VALID_YIELDS:
                raise self.InvalidArgumentYieldsError(ref, valid_yields=ReturnFilter.VALID_YIELDS, actual_yields=yields)

    class NestedOperatorsNotSupportedError(exceptions.ValidationError):
        def __init__(self, operator: operators.Operator):
            super().__init__(f'Nested operators are not supported: `{operator}`')
            self.operator = operator

    class InvalidArgumentYieldsError(exceptions.ValidationError):
        def __init__(self, ref: R, valid_yields: Set[Type[A]], actual_yields: Set[Type[A]]):
            super().__init__(f'Invalid yields for variable `{ref.alias}`: expected {valid_yields}, got {actual_yields}')
            self.ref = ref
            self.valid_yields = valid_yields
            self.actual_yields = actual_yields

    class UndefinedAnyYieldVariableError(exceptions.ValidationError):
        def __init__(self, ref: R):
            super().__init__(f'Unexpected variable `{ref.alias}` in `Any` yield case')
            self.ref = ref

    class UndefinedEmptyYieldVariableError(exceptions.ValidationError):
        def __init__(self, ref: R):
            super().__init__(f'Unexpected variable `{ref.alias}` in `Empty` yield case')
            self.ref = ref

    class MissingValueYieldVariableError(exceptions.ValidationError):
        def __init__(self, ref: R):
            super().__init__(f'Missing variable `{ref.alias}` in `Value` yield case')
            self.ref = ref


class VariablesFinder:
    def stream_variable_references(self, operator: operators.Return[core.filters.Filter]) -> Iterator[R]:
        for value in self._stream_variable_values_from_filter(operator):
            if isinstance(value, values.Variable):
                yield value.ref

    def _stream_variable_values_from_filter(self, operator: operators.Return[core.filters.Filter]) -> Iterator[values.Value]:
        for filter_ in operator.cases:
            if isinstance(filter_, core.filters.AnyLabel):
                yield from self._stream_variable_values_from_labels(filter_.labels)
            elif isinstance(filter_, core.filters.NoLabels):
                yield from self._stream_variable_values_from_labels(filter_.labels)
            elif isinstance(filter_, core.filters.AnyRange):
                yield from self._stream_variable_values_from_ranges(filter_.ranges)
            elif isinstance(filter_, core.filters.NoRanges):
                yield from self._stream_variable_values_from_ranges(filter_.ranges)
            else:
                raise NotImplementedError(f'Unexpected filter type: {type(filter_)}')

    @staticmethod
    def _stream_variable_values_from_labels(operators_: Iterable[operators.Operator[core.labels.Label]]) -> Iterator[values.Value]:
        for operator in operators_:
            assert isinstance(operator, operators.Return)
            for label in operator.cases:
                if isinstance(label, core.labels.Value):
                    yield label.value

    @staticmethod
    def _stream_variable_values_from_ranges(operators_: Iterable[operators.Operator[core.ranges.Range]]) -> Iterator[values.Value]:
        for operator in operators_:
            assert isinstance(operator, operators.Return)
            for range_ in operator.cases:
                if isinstance(range_, core.ranges.Between):
                    yield range_.min_value
                    yield range_.max_value
                elif isinstance(range_, core.ranges.LessThan):
                    yield range_.value
                elif isinstance(range_, core.ranges.MoreThan):
                    yield range_.value


class ReturnFilter(IConstraint):
    VALID_YIELDS = frozenset({
        arguments.Value,
    })

    def __init__(self, arguments_: IArguments, filter_: operators.Return[core.filters.Filter]):
        self.arguments = arguments_
        self.filter = filter_
        self.finder = VariablesFinder()

    def validate(self):
        for ref in self.finder.stream_variable_references(operator=self.filter):
            yields = self.arguments.get_yields(ref)
            if yields != self.VALID_YIELDS:
                raise self.InvalidArgumentYieldsError(ref.alias, valid_yields=self.VALID_YIELDS, actual_yields=yields)

    class InvalidArgumentYieldsError(exceptions.ValidationError):
        def __init__(self, alias: str, valid_yields: Set[Type[A]], actual_yields: Set[Type[A]]):
            super().__init__(f'Invalid yields for variable `{alias}`: expected {valid_yields}, got {actual_yields}')
            self.alias = alias
            self.valid_yields = valid_yields
            self.actual_yields = actual_yields
