from __future__ import annotations

from typing import TypeAlias

from rmshared.content.taxonomy import core
from rmshared.content.taxonomy import variables

from rmshared.content.taxonomy.sql.parsing import exceptions
from rmshared.content.taxonomy.sql.parsing.lark.abc import IFilters
from rmshared.content.taxonomy.sql.parsing.lark.abc import IContextManager

TF: TypeAlias = core.filters.Filter
TL: TypeAlias = core.labels.Label
TR: TypeAlias = core.ranges.Range
TS: TypeAlias = str | int | float

TO: TypeAlias = variables.Operator
TV: TypeAlias = variables.values.Value


class ConstantFilters(IFilters[TF, TL, TR, TS]):
    def make_constant_value(self, scalar):
        return scalar

    def make_variable_value(self, ref, index):
        raise exceptions.VariablesAreNotSupportedError()

    def resolve_reference_by_index(self, index):
        raise exceptions.VariablesAreNotSupportedError()

    def resolve_reference_by_alias(self, alias):
        raise exceptions.VariablesAreNotSupportedError()

    def make_return_badge_label(self, field):
        return core.labels.Badge(field=field)

    def make_return_empty_label(self, field):
        return core.labels.Empty(field=field)

    def make_return_value_label(self, field, value):
        return core.labels.Value(field=field, value=value)

    def make_return_between_range(self, field, min_value, max_value):
        return core.ranges.Between(field=field, min_value=min_value, max_value=max_value)

    def make_return_less_than_range(self, field, value):
        return core.ranges.LessThan(field=field, value=value)

    def make_return_more_than_range(self, field, value):
        return core.ranges.MoreThan(field=field, value=value)

    def make_return_any_label_filter(self, labels):
        return core.filters.AnyLabel(labels=labels)

    def make_return_no_labels_filter(self, labels):
        return core.filters.NoLabels(labels=labels)

    def make_return_any_range_filter(self, ranges):
        return core.filters.AnyRange(ranges=ranges)

    def make_return_no_ranges_filter(self, ranges):
        return core.filters.NoRanges(ranges=ranges)

    def make_return_nothing(self):
        raise exceptions.VariablesAreNotSupportedError()

    def validate_return_filter(self, filter_):
        return filter_

    def validate_switch_filter(self, filter_):
        raise exceptions.VariablesAreNotSupportedError()


class VariableFilters(IFilters[TO[TF], TO[TL], TO[TR], TV]):
    def __init__(self, arguments: IContextManager.IArguments):
        self.arguments = arguments

    def resolve_reference_by_index(self, index):
        return self.arguments.resolve_reference_by_index(index)

    def resolve_reference_by_alias(self, alias):
        return self.arguments.resolve_reference_by_alias(alias)

    def make_constant_value(self, scalar):
        return variables.values.Constant(value=scalar)

    def make_variable_value(self, ref, index):
        return variables.values.Variable(ref=ref, index=index)

    def make_return_badge_label(self, field):
        return variables.operators.Return(cases=(
            core.labels.Badge(field=field),
        ))

    def make_return_empty_label(self, field):
        return variables.operators.Return(cases=(
            core.labels.Empty(field=field),
        ))

    def make_return_value_label(self, field, value):
        return variables.operators.Return(cases=(
            core.labels.Value(field=field, value=value),
        ))

    def make_return_between_range(self, field, min_value, max_value):
        return variables.operators.Return(cases=(
            core.ranges.Between(field=field, min_value=min_value, max_value=max_value),
        ))

    def make_return_less_than_range(self, field, value):
        return variables.operators.Return(cases=(
            core.ranges.LessThan(field=field, value=value),
        ))

    def make_return_more_than_range(self, field, value):
        return variables.operators.Return(cases=(
            core.ranges.MoreThan(field=field, value=value),
        ))

    def make_return_any_label_filter(self, labels):
        return variables.operators.Return(cases=(
            core.filters.AnyLabel(labels=labels),
        ))

    def make_return_no_labels_filter(self, labels):
        return variables.operators.Return(cases=(
            core.filters.NoLabels(labels=labels),
        ))

    def make_return_any_range_filter(self, ranges):
        return variables.operators.Return(cases=(
            core.filters.AnyRange(ranges=ranges),
        ))

    def make_return_no_ranges_filter(self, ranges):
        return variables.operators.Return(cases=(
            core.filters.NoRanges(ranges=ranges),
        ))

    def make_return_nothing(self):
        return variables.operators.Return(cases=())

    def validate_return_filter(self, filter_):
        assert isinstance(filter_, variables.operators.Return)
        arguments_ = self.ValidationArguments(self.arguments)
        constraint = variables.validation.constraints.ReturnFilter(arguments_, filter_)
        try:
            constraint.validate()
        except constraint.InvalidArgumentYieldsError as e:
            raise exceptions.ArgumentCanBeOptionalError(alias=e.alias, yields=frozenset(map(str, e.actual_yields))) from e
        else:
            return filter_

    def validate_switch_filter(self, filter_):
        assert isinstance(filter_, variables.operators.Switch)
        arguments_ = self.ValidationArguments(self.arguments)
        constraint = variables.validation.constraints.SwitchFilter(arguments_, filter_)
        try:
            constraint.validate()
        except constraint.InvalidArgumentYieldsError as e:
            raise exceptions.ArgumentNotOptionalError(alias=e.ref.alias, yields=frozenset(map(str, e.actual_yields))) from e
        except constraint.UndefinedAnyYieldVariableError as e:
            raise exceptions.ArgumentNotDefinedError(alias=e.ref.alias) from e
        except constraint.MissingValueYieldVariableError as e:
            raise exceptions.ArgumentNotFoundError(alias=e.ref.alias) from e
        else:
            return filter_

    class ValidationArguments(variables.validation.IArguments):
        def __init__(self, arguments: IContextManager.IArguments):
            self.arguments = arguments

        def get_yields(self, ref):
            return self.arguments.get_yields(ref)
