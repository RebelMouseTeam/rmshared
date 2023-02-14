from pytest import fixture

from rmshared.typings import read_only

from rmshared.content.taxonomy.core import filters as core_filters
from rmshared.content.taxonomy.core import labels as core_labels
from rmshared.content.taxonomy.core import fields as core_fields

from rmshared.content.taxonomy.core.variables import arguments
from rmshared.content.taxonomy.core.variables import filters
from rmshared.content.taxonomy.core.variables import labels
from rmshared.content.taxonomy.core.variables import ranges
from rmshared.content.taxonomy.core.variables.abc import Cases
from rmshared.content.taxonomy.core.variables.abc import Constant
from rmshared.content.taxonomy.core.variables.abc import Variable
from rmshared.content.taxonomy.core.variables.abc import Reference
from rmshared.content.taxonomy.core.variables.protocol import Protocol


class TestServerProtocol:
    NOW = 1440000000

    @fixture
    def protocol(self) -> Protocol:
        return Protocol()

    def test_it_should_parse_filters(self, protocol: Protocol):
        filters_ = frozenset(protocol.make_filters(data=[
            {'any_label': [
                {'value': {'field': {'post-id': {}}, 'value': 123}},
            ]},
            {'$switch': {
                '$ref': '$$1',
                '$cases': {
                    '$none': [{'any_label': [
                        {'empty': {'field': {'post-regular-section': {}}}},
                    ]}],
                    '$': [{'any_label': [
                        {'value': {'field': {'post-regular-section': {}}, 'value': '$$1'}},
                    ]}],
                },
            }},
            {'$switch': {
                '$ref': '$$2',
                '$cases': {
                    '$any': [],
                    '$none': [{'no_labels': [
                        {'badge': {'field': {'private-post': {}}}},
                    ]}],
                    '$': [{'any_label': [
                        {'badge': {'field': {'private-post': {}}}},
                    ]}],
                },
            }},
            {'any_label': [
                {'value': {'field': {'post-id': {}}, 'value': 123}},
                {'$switch': {
                    '$ref': '$$3',
                    '$cases': {
                        '$none': [
                            {'empty': {'field': {'post-primary-tag': {}}}},
                        ],
                        '$': [
                            {'value': {'field': {'post-primary-tag': {}}, 'value': '$$3'}},
                            {'value': {'field': {'post-primary-tag': {}}, 'value': '$$3[2]'}},
                        ],
                    },
                }},
            ]},
            {'$switch': {
                '$ref': '$$4',
                '$cases': {
                    '$': [{'any_range': [
                        {'field': {'post-modified-at': {}}, 'min': '$$4[1]', 'max': '$$3'},
                    ]}],
                },
            }},
            {'no_ranges': [
                {'$switch': {
                    '$ref': '$$5',
                    '$cases': {
                        '$': [
                            {'field': {'post-modified-at': {}}, 'min': '$$5[1]'},
                            {'field': {'post-published-at': {}}, 'min': 100, 'max': '$$5[2]'},
                        ],
                    },
                }},
            ]},
        ]))
        assert filters_ == frozenset({
            core_filters.AnyLabel(labels=(
                core_labels.Value(field=core_fields.System('post-id'), value=123),
            )),
            filters.Switch(
                ref=Reference('$1'),
                cases=Cases(cases=read_only({
                    arguments.Empty: [
                        core_filters.AnyLabel(labels=(core_labels.Empty(field=core_fields.System('post-regular-section')), ))
                    ],
                    arguments.Value: [
                        core_filters.AnyLabel(labels=(
                            labels.Value(field=core_fields.System('post-regular-section'), value=Variable(ref=Reference('$1'), index=1)),
                        )),
                    ],
                }))
            ),
            filters.Switch(
                ref=Reference('$2'),
                cases=Cases(cases=read_only({
                    arguments.Any: [],
                    arguments.Empty: [
                        core_filters.NoLabels(labels=(core_labels.Badge(field=core_fields.System('private-post')),)),
                    ],
                    arguments.Value: [
                        core_filters.AnyLabel(labels=(core_labels.Badge(field=core_fields.System('private-post')),)),
                    ],
                }))
            ),
            core_filters.AnyLabel(labels=(
                core_labels.Value(field=core_fields.System('post-id'), value=123),
                labels.Switch(
                    ref=Reference('$3'),
                    cases=Cases(cases=read_only({
                        arguments.Empty: [
                            core_labels.Empty(field=core_fields.System('post-primary-tag')),
                        ],
                        arguments.Value: [
                            labels.Value(field=core_fields.System('post-primary-tag'), value=Variable(ref=Reference('$3'), index=1)),
                            labels.Value(field=core_fields.System('post-primary-tag'), value=Variable(ref=Reference('$3'), index=2)),
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
                                field=core_fields.System('post-modified-at'),
                                min_value=Variable(ref=Reference('$4'), index=1),
                                max_value=Variable(ref=Reference('$3'), index=1)
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
                                field=core_fields.System('post-modified-at'),
                                value=Variable(ref=Reference('$5'), index=1),
                            ),
                            ranges.Between(
                                field=core_fields.System('post-published-at'),
                                min_value=Constant(100),
                                max_value=Variable(ref=Reference('$5'), index=2),
                            ),
                        ],
                    })),
                ),
            )),
        })
