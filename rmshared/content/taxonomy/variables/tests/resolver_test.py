from sys import maxsize
from typing import Mapping

from pytest import fixture

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
            'variable_1': arguments.Empty(),
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

        filters_ = tuple(resolver.dereference_filters(operators_=fixtures.FILTERS, arguments_=self.Arguments({
            'variable_1': arguments.Value(values=(567,)),
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

    def test_it_should_dereference_filters_partially(self, resolver: Resolver):
        arguments_0 = self.Arguments({})
        arguments_1 = self.Arguments({
            'variable_1': arguments.Value(values=(567,)),
            '$1': arguments.Value(values=(567,)),
        })
        arguments_2 = self.Arguments({
            'variable_1': arguments.Value(values=(567,)),
            '$1': arguments.Value(values=(567,)),
            '$2': arguments.Any(),
        })
        arguments_3 = self.Arguments({
            'variable_1': arguments.Value(values=(567,)),
            '$1': arguments.Value(values=(567,)),
            '$2': arguments.Any(),
            '$3': arguments.Empty(),
        })
        arguments_4 = self.Arguments({
            'variable_1': arguments.Value(values=(567,)),
            '$1': arguments.Value(values=(567,)),
            '$2': arguments.Any(),
            '$3': arguments.Empty(),
            '$4': arguments.Value(values=(100, 200)),
        })
        arguments_5 = self.Arguments({
            'variable_1': arguments.Value(values=(567,)),
            '$1': arguments.Value(values=(567,)),
            '$2': arguments.Any(),
            '$3': arguments.Empty(),
            '$4': arguments.Value(values=(100, 200)),
            '$5': arguments.Value(values=(300, maxsize)),
        })

        filters_0, operators_0 = resolver.dereference_filters_partially(operators_=fixtures.FILTERS, arguments_=arguments_0)
        filters_1, operators_1 = resolver.dereference_filters_partially(operators_=fixtures.FILTERS, arguments_=arguments_1)
        filters_2, operators_2 = resolver.dereference_filters_partially(operators_=fixtures.FILTERS, arguments_=arguments_2)
        filters_3, operators_3 = resolver.dereference_filters_partially(operators_=fixtures.FILTERS, arguments_=arguments_3)
        filters_4, operators_4 = resolver.dereference_filters_partially(operators_=fixtures.FILTERS, arguments_=arguments_4)
        filters_5, operators_5 = resolver.dereference_filters_partially(operators_=fixtures.FILTERS, arguments_=arguments_5)

        expected_by_post_id_filter = core.filters.AnyLabel(labels=(
            core.labels.Value(field=core.fields.System('post-id'), value=123),
        ))
        expected_by_regular_section_filter = core.filters.AnyLabel(labels=(
            core.labels.Value(field=core.fields.System('post-regular-section'), value=567),
        ))
        expected_by_no_primary_tags_filter = core.filters.AnyLabel(labels=(
            core.labels.Value(field=core.fields.System('post-id'), value=123),
            core.labels.Empty(field=core.fields.System('post-primary-tag')),
        ))

        assert tuple(filters_0) == (
            expected_by_post_id_filter,
        )
        assert tuple(operators_0) == tuple(fixtures.FILTERS[1:])

        assert tuple(filters_1) == (
            expected_by_post_id_filter,
            expected_by_regular_section_filter,
        )
        assert tuple(operators_1) == tuple(fixtures.FILTERS[2:])

        assert tuple(filters_2) == (
            expected_by_post_id_filter,
            expected_by_regular_section_filter,
        )
        assert tuple(operators_2) == tuple(fixtures.FILTERS[3:])

        assert tuple(filters_3) == (
            expected_by_post_id_filter,
            expected_by_regular_section_filter,
            expected_by_no_primary_tags_filter,
        )
        assert tuple(operators_3) == tuple(fixtures.FILTERS[4:])

        assert tuple(filters_4) == (
            expected_by_post_id_filter,
            expected_by_regular_section_filter,
            expected_by_no_primary_tags_filter,
        )
        assert tuple(operators_4) == tuple(fixtures.FILTERS[4:])

        assert tuple(filters_5) == (
            expected_by_post_id_filter,
            expected_by_regular_section_filter,
            expected_by_no_primary_tags_filter,
            core.filters.AnyRange(ranges=(
                core.ranges.Between(field=core.fields.System('post-modified-at'), min_value=200, max_value=300),
            )),
            core.filters.NoRanges(ranges=(
                core.ranges.MoreThan(field=core.fields.System('post-modified-at'), value=100),
                core.ranges.Between(field=core.fields.System('post-published-at'), min_value=100, max_value=maxsize),
            )),
        )
        assert tuple(operators_5) == tuple()

    class Arguments(Resolver.IArguments):
        def __init__(self, alias_to_argument_map: Mapping[str, Argument]):
            self.alias_to_argument_map = alias_to_argument_map

        def get_argument(self, alias):
            try:
                return self.alias_to_argument_map[alias]
            except LookupError as e:
                raise self.ArgumentNotFoundException(alias) from e
