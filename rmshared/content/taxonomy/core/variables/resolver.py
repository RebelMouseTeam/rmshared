from itertools import chain
from typing import Any
from typing import Callable
from typing import Iterator
from typing import TypeVar

from rmshared.content.taxonomy import visitors as taxonomy_visitors

from rmshared.content.taxonomy.core import filters
from rmshared.content.taxonomy.core import labels
from rmshared.content.taxonomy.core import ranges
from rmshared.content.taxonomy.core import expander
from rmshared.content.taxonomy.core.variables import values
from rmshared.content.taxonomy.core.variables import operators
from rmshared.content.taxonomy.core.variables.abc import Operator
from rmshared.content.taxonomy.core.variables.abc import Scalar
from rmshared.content.taxonomy.core.variables.abc import IResolver

T = TypeVar('T')


class Resolver(IResolver[Operator[filters.Filter], filters.Filter]):
    def dereference_filters(self, filters_, arguments_):
        factory = self.Factory(arguments_)
        visitor_ = factory.make_visitor()
        return chain.from_iterable(visitor_.visit_filters(filters_))

    class Factory:
        def __init__(self, arguments_: IResolver.IArguments):
            self.delegate = expander.Factory()
            self.arguments = arguments_
            self.operators = self.Operators(arguments_)

        def make_visitor(self) -> taxonomy_visitors.IVisitor:
            builder = taxonomy_visitors.Builder()
            builder.customize_filters(self._make_filters, dependencies=(taxonomy_visitors.ILabels, taxonomy_visitors.IRanges))
            builder.customize_labels(self._make_labels, dependencies=(taxonomy_visitors.IFields, taxonomy_visitors.IValues))
            builder.customize_ranges(self._make_ranges, dependencies=(taxonomy_visitors.IFields, taxonomy_visitors.IValues))
            builder.customize_values(self._make_values, dependencies=())
            builder.customize_orders(self.delegate.make_orders, dependencies=())
            builder.customize_fields(self.delegate.make_fields, dependencies=())
            return builder.make_visitor()

        def _make_filters(self, labels_: taxonomy_visitors.ILabels, ranges_: taxonomy_visitors.IRanges) -> taxonomy_visitors.IFilters:
            delegate = self.delegate.make_filters(labels_, ranges_)
            instance = taxonomy_visitors.composites.Filters()
            instance.add_filter(operators.Switch[filters.Filter], self.SwitchFilters(instance, self.operators))
            instance.add_filter(operators.Return[filters.Filter], self.ReturnFilters(delegate, self.operators))
            return taxonomy_visitors.fallbacks.Filters(instance, delegate, exceptions=(LookupError, ))

        def _make_labels(self, fields_: taxonomy_visitors.IFields, values_: taxonomy_visitors.IValues) -> taxonomy_visitors.ILabels:
            delegate = self.delegate.make_labels(fields_, values_)
            instance = taxonomy_visitors.composites.Labels()
            instance.add_label(operators.Switch[labels.Label], self.SwitchLabels(instance, self.operators))
            instance.add_label(operators.Return[labels.Label], self.ReturnLabels(delegate, self.operators))
            return taxonomy_visitors.fallbacks.Labels(instance, delegate, exceptions=(LookupError, ))

        def _make_ranges(self, fields_: taxonomy_visitors.IFields, values_: taxonomy_visitors.IValues) -> taxonomy_visitors.IRanges:
            delegate = self.delegate.make_ranges(fields_, values_)
            instance = taxonomy_visitors.composites.Ranges()
            instance.add_range(operators.Switch[ranges.Range], self.SwitchRanges(instance, self.operators))
            instance.add_range(operators.Return[ranges.Range], self.ReturnRanges(delegate, self.operators))
            return taxonomy_visitors.fallbacks.Ranges(instance, delegate, exceptions=(LookupError, ))

        def _make_values(self) -> taxonomy_visitors.IValues:
            delegate = self.delegate.make_values()
            instance = taxonomy_visitors.composites.Values()
            instance.add_value(values.Variable, self.ResolveVariable(self.arguments))
            instance.add_value(values.Constant, self.ResolveConstant())
            return taxonomy_visitors.fallbacks.Values(instance, delegate, exceptions=(LookupError, ))

        class SwitchFilters(taxonomy_visitors.IFilters[operators.Switch[filters.Filter], Iterator[filters.Filter]]):
            def __init__(self, delegate: taxonomy_visitors.IFilters[Operator, Iterator[filters.Filter]], operators_: 'Resolver.Factory.Operators'):
                self.delegate = delegate
                self.operators = operators_

            def visit_filter(self, filter_: operators.Switch[filters.Filter]) -> Iterator[filters.Filter]:
                return self.operators.visit_switch(filter_, self.delegate.visit_filter)

        class ReturnFilters(taxonomy_visitors.IFilters[operators.Return[filters.Filter], Iterator[filters.Filter]]):
            def __init__(self, delegate: taxonomy_visitors.IFilters[filters.Filter, Iterator[filters.Filter]], operators_: 'Resolver.Factory.Operators'):
                self.delegate = delegate
                self.operators = operators_

            def visit_filter(self, filter_: operators.Return[filters.Filter]) -> Iterator[filters.Filter]:
                return self.operators.visit_return(filter_, self.delegate.visit_filter)

        class SwitchLabels(taxonomy_visitors.ILabels[operators.Switch[labels.Label], Iterator[labels.Label]]):
            def __init__(self, delegate: taxonomy_visitors.ILabels[Operator, Iterator[labels.Label]], operators_: 'Resolver.Factory.Operators'):
                self.delegate = delegate
                self.operators = operators_

            def visit_label(self, label: operators.Switch[labels.Label]) -> Iterator[labels.Label]:
                return self.operators.visit_switch(label, self.delegate.visit_label)

        class ReturnLabels(taxonomy_visitors.ILabels[operators.Return[labels.Label], Iterator[labels.Label]]):
            def __init__(self, delegate: taxonomy_visitors.ILabels[labels.Label, Iterator[labels.Label]], operators_: 'Resolver.Factory.Operators'):
                self.delegate = delegate
                self.operators = operators_

            def visit_label(self, label: operators.Return[labels.Label]) -> Iterator[labels.Label]:
                return self.operators.visit_return(label, self.delegate.visit_label)

        class SwitchRanges(taxonomy_visitors.IRanges[operators.Switch[ranges.Range], Iterator[ranges.Range]]):
            def __init__(self, delegate: taxonomy_visitors.IRanges[Operator, Iterator[ranges.Range]], operators_: 'Resolver.Factory.Operators'):
                self.delegate = delegate
                self.operators = operators_

            def visit_range(self, range_: operators.Switch[ranges.Range]) -> Iterator[ranges.Range]:
                return self.operators.visit_switch(range_, self.delegate.visit_range)

        class ReturnRanges(taxonomy_visitors.IRanges[operators.Return[ranges.Range], Iterator[ranges.Range]]):
            def __init__(self, delegate: taxonomy_visitors.IRanges[ranges.Range, Iterator[ranges.Range]], operators_: 'Resolver.Factory.Operators'):
                self.delegate = delegate
                self.operators = operators_

            def visit_range(self, range_: operators.Return[ranges.Range]) -> Iterator[ranges.Range]:
                return self.operators.visit_return(range_, self.delegate.visit_range)

        class ResolveVariable(taxonomy_visitors.IValues[values.Variable, Scalar]):
            def __init__(self, arguments: IResolver.IArguments):
                self.arguments = arguments

            def visit_value(self, value_: values.Variable) -> Scalar:
                return self.arguments.get_value(value_.ref.alias, value_.index)

        class ResolveConstant(taxonomy_visitors.IValues[values.Constant, Scalar]):
            def visit_value(self, value_: values.Constant) -> Scalar:
                return value_.value

        class Operators:
            def __init__(self, arguments: IResolver.IArguments):
                self.arguments = arguments

            def visit_switch(self, operator: operators.Switch[T], visit_case: Callable[[Operator[T]], Any]) -> Iterator[T]:
                argument = self.arguments.get_argument(operator.ref.alias)
                try:
                    operator = operator.cases[type(argument)]
                except LookupError:
                    return []
                else:
                    return visit_case(operator)

            @staticmethod
            def visit_return(operator: operators.Return[T], visit_case: Callable[[T], Any]) -> Iterator[T]:
                return chain.from_iterable(map(visit_case, operator.cases))
