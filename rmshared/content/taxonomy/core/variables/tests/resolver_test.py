from sys import maxsize
from typing import Mapping

from pytest import fixture

from rmshared.typings import read_only

from rmshared.content.taxonomy.core import filters as core_filters
from rmshared.content.taxonomy.core import labels as core_labels
from rmshared.content.taxonomy.core import ranges as core_ranges
from rmshared.content.taxonomy.core.abc import Field
from rmshared.content.taxonomy.core.abc import Scalar

from rmshared.content.taxonomy.core.variables import arguments
from rmshared.content.taxonomy.core.variables import filters
from rmshared.content.taxonomy.core.variables import labels
from rmshared.content.taxonomy.core.variables import ranges
from rmshared.content.taxonomy.core.variables.abc import Cases
from rmshared.content.taxonomy.core.variables.abc import Argument
from rmshared.content.taxonomy.core.variables.abc import Constant
from rmshared.content.taxonomy.core.variables.abc import Variable
from rmshared.content.taxonomy.core.variables.abc import Reference
from rmshared.content.taxonomy.core.variables.resolver import Resolver


class TestServerResolver:
    NOW = 1440000000

    @fixture
    def resolver(self) -> Resolver:
        return Resolver()

    def test_it_should_dereference_filters(self, resolver: Resolver):
        filters_with_references = [
            core_filters.AnyLabel(labels=(
                core_labels.Value(field=Field('post-id'), value=123),
            )),
            filters.Switch(
                ref=Reference('$1'),
                cases=Cases(cases=read_only({
                    arguments.Empty: [
                        core_filters.AnyLabel(labels=(core_labels.Empty(field=Field('post-regular-section')),))
                    ],
                    arguments.Value: [
                        core_filters.AnyLabel(labels=(labels.Value(field=Field('post-regular-section'), value=Variable(ref=Reference('$1'), index=1)),)),
                    ],
                }))
            ),
            filters.Switch(
                ref=Reference('$2'),
                cases=Cases(cases=read_only({
                    arguments.Any: [],
                    arguments.Empty: [
                        core_filters.NoLabels(labels=(core_labels.Badge(field=Field('private-post')),)),
                    ],
                    arguments.Value: [
                        core_filters.AnyLabel(labels=(core_labels.Badge(field=Field('private-post')),)),
                    ],
                }))
            ),
            core_filters.AnyLabel(labels=(
                core_labels.Value(field=Field('post-id'), value=123),
                labels.Switch(
                    ref=Reference('$3'),
                    cases=Cases(cases=read_only({
                        arguments.Empty: [
                            core_labels.Empty(field=Field('post-primary-tag')),
                        ],
                        arguments.Value: [
                            labels.Value(field=Field('post-primary-tag'), value=Variable(ref=Reference('$3'), index=1)),
                            labels.Value(field=Field('post-primary-tag'), value=Variable(ref=Reference('$3'), index=2)),
                        ],
                    }))
                ),
            )),
            filters.Switch(
                ref=Reference('$4'),
                cases=Cases(cases=read_only({
                    arguments.Value: [
                        core_filters.AnyRange(ranges=(
                            ranges.Between(
                                field=Field('post-modified-at'),
                                min_value=Variable(ref=Reference('$4'), index=2),
                                max_value=Variable(ref=Reference('$5'), index=1)
                            ),
                        )),
                    ],
                }))
            ),
            core_filters.NoRanges(ranges=(
                ranges.Switch(
                    ref=Reference('$5'),
                    cases=Cases(cases=read_only({
                        arguments.Value: [
                            ranges.MoreThan(
                                field=Field('post-modified-at'),
                                value=Variable(ref=Reference('$4'), index=1),
                            ),
                            ranges.Between(
                                field=Field('post-published-at'),
                                min_value=Constant(100),
                                max_value=Variable(ref=Reference('$5'), index=2),
                            ),
                        ],
                    })),
                ),
            )),
        ]

        class Arguments(Resolver.IArguments):
            def __init__(self, alias_to_argument_map: Mapping[str, Argument]):
                self.alias_to_argument_map = alias_to_argument_map

            def get_argument(self, alias: str) -> 'Argument':
                return self.alias_to_argument_map[alias]

            def get_value(self, alias: str, index: int) -> Scalar:
                argument = self.alias_to_argument_map[alias]
                assert isinstance(argument, arguments.Value)
                return argument.values[index - 1]

        filters_ = tuple(resolver.dereference_filters(filters_=read_only(filters_with_references), arguments=Arguments({
            '$1': arguments.Empty(),
            '$2': arguments.Value(values=tuple()),
            '$3': arguments.Value(values=('tag-1', 'tag-2')),
            '$4': arguments.Value(values=(100, 200)),
            '$5': arguments.Value(values=(300, maxsize)),
        })))

        assert filters_ == (
            core_filters.AnyLabel(labels=(
                core_labels.Value(field=Field('post-id'), value=123),
            )),
            core_filters.AnyLabel(labels=(
                core_labels.Empty(field=Field('post-regular-section')),
            )),
            core_filters.AnyLabel(labels=(
                core_labels.Badge(field=Field('private-post')),
            )),
            core_filters.AnyLabel(labels=(
                core_labels.Value(field=Field('post-id'), value=123),
                core_labels.Value(field=Field('post-primary-tag'), value='tag-1'),
                core_labels.Value(field=Field('post-primary-tag'), value='tag-2'),
            )),
            core_filters.AnyRange(ranges=(
                core_ranges.Between(field=Field('post-modified-at'), min_value=200, max_value=300),
            )),
            core_filters.NoRanges(ranges=(
                core_ranges.MoreThan(field=Field('post-modified-at'), value=100),
                core_ranges.Between(field=Field('post-published-at'), min_value=100, max_value=maxsize),
            )),
        )

        filters_ = tuple(resolver.dereference_filters(filters_=read_only(filters_with_references), arguments=Arguments({
            '$1': arguments.Value(values=(567,)),
            '$2': arguments.Any(),
            '$3': arguments.Empty(),
            '$4': arguments.Empty(),
            '$5': arguments.Any(),
        })))

        assert filters_ == (
            core_filters.AnyLabel(labels=(
                core_labels.Value(field=Field('post-id'), value=123),
            )),
            core_filters.AnyLabel(labels=(
                core_labels.Value(field=Field('post-regular-section'), value=567),
            )),
            core_filters.AnyLabel(labels=(
                core_labels.Value(field=Field('post-id'), value=123),
                core_labels.Empty(field=Field('post-primary-tag')),
            )),
            core_filters.NoRanges(ranges=tuple()),
        )
