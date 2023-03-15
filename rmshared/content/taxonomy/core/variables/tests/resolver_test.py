from sys import maxsize
from typing import Mapping
from typing import TypeVar

from pytest import fixture

from rmshared.typings import read_only

from rmshared.content.taxonomy.core import filters
from rmshared.content.taxonomy.core import labels
from rmshared.content.taxonomy.core import ranges
from rmshared.content.taxonomy.core import fields

from rmshared.content.taxonomy.core.variables import arguments
from rmshared.content.taxonomy.core.variables.resolver import Resolver
from rmshared.content.taxonomy.core.variables.tests import fixtures

Scalar = TypeVar('Scalar', str, int, float)


class TestServerResolver:
    NOW = 1440000000

    @fixture
    def resolver(self) -> Resolver:
        return Resolver()

    def test_it_should_dereference_filters(self, resolver: Resolver):
        filters_ = tuple(resolver.dereference_filters(filters_=read_only(fixtures.FILTERS), arguments_=self.Arguments({
            '$1': arguments.Empty(),
            '$2': arguments.Value(values=tuple()),
            '$3': arguments.Value(values=('tag-1', 'tag-2')),
            '$4': arguments.Value(values=(100, 200)),
            '$5': arguments.Value(values=(300, maxsize)),
        })))

        assert filters_ == (
            filters.AnyLabel(labels=(
                labels.Value(field=fields.System('post-id'), value=123),
            )),
            filters.AnyLabel(labels=(
                labels.Empty(field=fields.System('post-regular-section')),
            )),
            filters.AnyLabel(labels=(
                labels.Badge(field=fields.System('private-post')),
            )),
            filters.AnyLabel(labels=(
                labels.Value(field=fields.System('post-id'), value=123),
                labels.Value(field=fields.System('post-primary-tag'), value='tag-1'),
                labels.Value(field=fields.System('post-primary-tag'), value='tag-2'),
            )),
            filters.AnyRange(ranges=(
                ranges.Between(field=fields.System('post-modified-at'), min_value=200, max_value=300),
            )),
            filters.NoRanges(ranges=(
                ranges.MoreThan(field=fields.System('post-modified-at'), value=100),
                ranges.Between(field=fields.System('post-published-at'), min_value=100, max_value=maxsize),
            )),
        )

        from pprint import pprint
        pprint([1, fixtures.FILTERS])

        filters_ = tuple(resolver.dereference_filters(filters_=read_only(fixtures.FILTERS), arguments_=self.Arguments({
            '$1': arguments.Value(values=(567,)),
            '$2': arguments.Any(),
            '$3': arguments.Empty(),
            '$4': arguments.Empty(),
            '$5': arguments.Any(),
        })))

        assert filters_ == (
            filters.AnyLabel(labels=(
                labels.Value(field=fields.System('post-id'), value=123),
            )),
            filters.AnyLabel(labels=(
                labels.Value(field=fields.System('post-regular-section'), value=567),
            )),
            filters.AnyLabel(labels=(
                labels.Value(field=fields.System('post-id'), value=123),
                labels.Empty(field=fields.System('post-primary-tag')),
            )),
            filters.NoRanges(ranges=tuple()),
        )

    class Arguments(Resolver.IArguments):
        def __init__(self, alias_to_argument_map: Mapping[str, arguments.Argument]):
            self.alias_to_argument_map = alias_to_argument_map

        def get_argument(self, alias: str) -> arguments.Argument:
            return self.alias_to_argument_map[alias]

        def get_value(self, alias: str, index: int) -> Scalar:
            argument = self.alias_to_argument_map[alias]
            assert isinstance(argument, arguments.Value)
            return argument.values[index - 1]
