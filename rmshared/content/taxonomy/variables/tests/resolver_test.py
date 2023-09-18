from sys import maxsize
from typing import Mapping

from pytest import fixture

from rmshared.typings import read_only

from rmshared.content.taxonomy import core

from rmshared.content.taxonomy.variables import arguments
from rmshared.content.taxonomy.variables.abc import Argument
from rmshared.content.taxonomy.variables.resolver import Resolver
from rmshared.content.taxonomy.variables.tests import fixtures


class TestServerResolver:
    NOW = 1440000000

    @fixture
    def resolver(self) -> Resolver:
        return Resolver()

    def test_it_should_dereference_filters(self, resolver: Resolver):
        filters_ = tuple(resolver.dereference_filters(operators_=fixtures.FILTERS, arguments_=self.Arguments({
            '$1': arguments.Empty(),
            '$2': arguments.Value(values=tuple()),
            '$3': arguments.Value(values=('tag-1', 'tag-2')),
            '$4': arguments.Value(values=(100, 200)),
            '$5': arguments.Value(values=(300, maxsize)),
        })))

        assert filters_ == (
            core.filters.AnyLabel(labels=(
                core.labels.Value(field=core.fields.System('post-id'), value=123),
            )),
            core.filters.AnyLabel(labels=(
                core.labels.Empty(field=core.fields.System('post-regular-section')),
            )),
            core.filters.AnyLabel(labels=(
                core.labels.Badge(field=core.fields.System('private-post')),
            )),
            core.filters.AnyLabel(labels=(
                core.labels.Value(field=core.fields.System('post-id'), value=123),
                core.labels.Value(field=core.fields.System('post-primary-tag'), value='tag-1'),
                core.labels.Value(field=core.fields.System('post-primary-tag'), value='tag-2'),
            )),
            core.filters.AnyRange(ranges=(
                core.ranges.Between(field=core.fields.System('post-modified-at'), min_value=200, max_value=300),
            )),
            core.filters.NoRanges(ranges=(
                core.ranges.MoreThan(field=core.fields.System('post-modified-at'), value=100),
                core.ranges.Between(field=core.fields.System('post-published-at'), min_value=100, max_value=maxsize),
            )),
        )

        filters_ = tuple(resolver.dereference_filters(operators_=read_only(fixtures.FILTERS), arguments_=self.Arguments({
            '$1': arguments.Value(values=(567,)),
            '$2': arguments.Any(),
            '$3': arguments.Empty(),
            '$4': arguments.Empty(),
            '$5': arguments.Any(),
        })))

        assert filters_ == (
            core.filters.AnyLabel(labels=(
                core.labels.Value(field=core.fields.System('post-id'), value=123),
            )),
            core.filters.AnyLabel(labels=(
                core.labels.Value(field=core.fields.System('post-regular-section'), value=567),
            )),
            core.filters.AnyLabel(labels=(
                core.labels.Value(field=core.fields.System('post-id'), value=123),
                core.labels.Empty(field=core.fields.System('post-primary-tag')),
            )),
        )

    class Arguments(Resolver.IArguments):
        def __init__(self, alias_to_argument_map: Mapping[str, Argument]):
            self.alias_to_argument_map = alias_to_argument_map

        def get_argument(self, alias):
            return self.alias_to_argument_map[alias]

        def get_value(self, alias: str, index: int):
            argument = self.alias_to_argument_map[alias]
            assert isinstance(argument, arguments.Value)
            return argument.values[index - 1]
