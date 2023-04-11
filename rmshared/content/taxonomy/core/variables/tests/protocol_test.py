from pytest import fixture

from rmshared.content.taxonomy.core.variables import protocol
from rmshared.content.taxonomy.core.variables.abc import IProtocol
from rmshared.content.taxonomy.core.variables.tests import fixtures


class TestProtocol:
    NOW = 1440000000

    @fixture
    def protocol_(self) -> IProtocol:
        return protocol.Factory().make_protocol()

    def test_it_should_make_filters(self, protocol_: IProtocol):
        filters_ = tuple(protocol_.make_filters(data=self.FILTERS_DATA))
        assert filters_ == fixtures.FILTERS

    def test_it_should_jsonify_filters(self, protocol_: IProtocol):
        data = tuple(protocol_.jsonify_filters(filters_=fixtures.FILTERS))
        assert data == self.FILTERS_DATA

    FILTERS_DATA = (
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
                    {'value': {'field': {'post-regular-section': {}}, 'value': '$$1[1]'}},
                ]}],
            },
        }},
        {'$switch': {
            '$ref': '$$2',
            '$cases': {
                '$any': [],
                '$none': [{'no_labels': [
                    {'empty': {'field': {'private-post': {}}}},
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
                        {'value': {'field': {'post-primary-tag': {}}, 'value': '$$3[1]'}},
                        {'value': {'field': {'post-primary-tag': {}}, 'value': '$$3[2]'}},
                    ],
                },
            }},
        ]},
        {'$switch': {
            '$ref': '$$4',
            '$cases': {
                '$': [{'any_range': [
                    {'field': {'post-modified-at': {}}, 'min': '$$4[2]', 'max': '$$5[1]'},
                ]}],
            },
        }},
        {'no_ranges': [
            {'$switch': {
                '$ref': '$$5',
                '$cases': {
                    '$': [
                        {'field': {'post-modified-at': {}}, 'min': '$$4[1]'},
                        {'field': {'post-published-at': {}}, 'min': 100, 'max': '$$5[2]'},
                    ],
                },
            }},
        ]},
    )
