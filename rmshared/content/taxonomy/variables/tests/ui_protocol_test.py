from pytest import fixture

from rmshared.content.taxonomy import core
from rmshared.content.taxonomy.variables import protocols
from rmshared.content.taxonomy.variables.tests import fixtures


class TestUiProtocol:
    NOW = 1440000000

    @fixture
    def protocol(self) -> core.protocols.IComposite:
        return protocols.Factory.make_instance_for_ui().make_composite()

    def test_it_should_make_filters(self, protocol: core.protocols.IComposite):
        filters_ = tuple(map(protocol.make_filter, self.FILTERS_DATA))
        assert filters_ == fixtures.FILTERS

    def test_it_should_jsonify_filters(self, protocol: core.protocols.IComposite):
        data = tuple(map(protocol.jsonify_filter, fixtures.FILTERS))
        assert data == self.FILTERS_DATA

    FILTERS_DATA = (
        {'$return': [{'any_label': [
            {'value': {'field': {'post-id': {}}, 'value': 123}},
        ]}]},
        {'$switch': {
            '$ref': '$$1',
            '$cases': {
                '$none': [{'any_label': [
                    {'empty': {'field': {'post-regular-section': {}}}},
                ]}],
                '$each': [{'any_label': [
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
                '$each': [{'any_label': [
                    {'badge': {'field': {'private-post': {}}}},
                ]}],
            },
        }},
        {'$switch': {
            '$ref': '$$3',
            '$cases': {
                '$any': [{'any_label': [
                    {'value': {'field': {'post-id': {}}, 'value': 123}},
                ]}],
                '$none': [{'any_label': [
                    {'value': {'field': {'post-id': {}}, 'value': 123}},
                    {'empty': {'field': {'post-primary-tag': {}}}},
                ]}],
                '$each': [{'any_label': [
                    {'value': {'field': {'post-id': {}}, 'value': 123}},
                    {'value': {'field': {'post-primary-tag': {}}, 'value': '$$3[1]'}},
                    {'value': {'field': {'post-primary-tag': {}}, 'value': '$$3[2]'}},
                ]}],
            },
        }},
        {'$switch': {
            '$ref': '$$4',
            '$cases': {
                '$each': [{'any_range': [
                    {'field': {'post-modified-at': {}}, 'min': '$$4[2]', 'max': '$$5[1]'},
                ]}],
            },
        }},
        {'$switch': {
            '$ref': '$$5',
            '$cases': {
                '$each': [{'no_ranges': [
                    {'field': {'post-modified-at': {}}, 'min': '$$4[1]'},
                    {'field': {'post-published-at': {}}, 'min': 100, 'max': '$$5[2]'},
                ]}],
            },
        }},
    )
