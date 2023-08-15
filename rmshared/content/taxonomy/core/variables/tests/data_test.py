from pytest import fixture

from rmshared.content.taxonomy.core.variables import data
from rmshared.content.taxonomy.core.variables.abc import IProtocol
from rmshared.content.taxonomy.core.variables.tests import fixtures


class TestData:
    NOW = 1440000000

    @fixture
    def protocol_(self) -> IProtocol:
        return data.Factory().make_protocol()

    def test_it_should_make_filters(self, protocol_: IProtocol):
        filters_ = tuple(protocol_.make_filters(data=self.FILTERS_DATA))
        assert filters_ == fixtures.FILTERS

    def test_it_should_jsonify_filters(self, protocol_: IProtocol):
        data_ = tuple(protocol_.jsonify_filters(filters_=fixtures.FILTERS))
        assert data_ == self.FILTERS_DATA

    FILTERS_DATA = (
        {'@return': {'@cases': [
            {'any_label': [
                {'@return': {'@cases': [
                    {'value': {'field': {'post-id': {}}, 'value': {'@constant': 123}}},
                ]}},
            ]},
        ]}},
        {'@switch': {
            '@ref': {'alias': '$1'},
            '@cases': {
                '@empty': {'@return': {'@cases': [
                    {'any_label': [
                        {'@return': {'@cases': [
                            {'empty': {'field': {'post-regular-section': {}}}},
                        ]}},
                    ]},
                ]}},
                '@value': {'@return': {'@cases': [
                    {'any_label': [
                        {'@return': {'@cases': [
                            {'value': {'field': {'post-regular-section': {}}, 'value': {'@variable': {'ref': {'alias': '$1'}, 'index': 1}}}},
                        ]}},
                    ]},
                ]}},
            },
        }},
        {'@switch': {
            '@ref': {'alias': '$2'},
            '@cases': {
                '@any': {'@return': {'@cases': []}},
                '@empty': {'@return': {'@cases': [
                    {'no_labels': [
                        {'@return': {'@cases': [
                            {'empty': {'field': {'private-post': {}}}},
                        ]}},
                    ]},
                ]}},
                '@value': {'@return': {'@cases': [
                    {'any_label': [
                        {'@return': {'@cases': [
                            {'badge': {'field': {'private-post': {}}}},
                        ]}},
                    ]},
                ]}},
            },
        }},
        {'@switch': {
            '@ref': {'alias': '$3'},
            '@cases': {
                '@any': {'@return': {'@cases': [
                    {'any_label': [
                        {'@return': {'@cases': [
                            {'value': {'field': {'post-id': {}}, 'value': {'@constant': 123}}},
                        ]}},
                    ]},
                ]}},
                '@empty': {'@return': {'@cases': [
                    {'any_label': [
                        {'@return': {'@cases': [
                            {'value': {'field': {'post-id': {}}, 'value': {'@constant': 123}}},
                        ]}},
                        {'@return': {'@cases': [
                            {'empty': {'field': {'post-primary-tag': {}}}},
                        ]}},
                    ]},
                ]}},
                '@value': {'@return': {'@cases': [
                    {'any_label': [
                        {'@return': {'@cases': [
                            {'value': {'field': {'post-id': {}}, 'value': {'@constant': 123}}},
                        ]}},
                        {'@return': {'@cases': [
                            {'value': {'field': {'post-primary-tag': {}}, 'value': {'@variable': {'ref': {'alias': '$3'}, 'index': 1}}}},
                        ]}},
                        {'@return': {'@cases': [
                            {'value': {'field': {'post-primary-tag': {}}, 'value': {'@variable': {'ref': {'alias': '$3'}, 'index': 2}}}},
                        ]}},
                    ]},
                ]}},
            },
        }},
        {'@switch': {
            '@ref': {'alias': '$4'},
            '@cases': {
                '@value': {'@return': {'@cases': [
                    {'any_range': [
                        {'@return': {'@cases': [{
                            'field': {'post-modified-at': {}},
                            'min': {'@variable': {'ref': {'alias': '$4'}, 'index': 2}},
                            'max': {'@variable': {'ref': {'alias': '$5'}, 'index': 1}},
                        }]}},
                    ]},
                ]}},
            },
        }},
        {'@switch': {
            '@ref': {'alias': '$5'},
            '@cases': {
                '@value': {'@return': {'@cases': [{'no_ranges': [
                    {'@return': {'@cases': [
                        {'field': {'post-modified-at': {}}, 'min': {'@variable': {'ref': {'alias': '$4'}, 'index': 1}}},
                    ]}},
                    {'@return': {'@cases': [
                        {'field': {'post-published-at': {}}, 'min': {'@constant': 100}, 'max': {'@variable': {'ref': {'alias': '$5'}, 'index': 2}}},
                    ]}},
                ]}]}},
            },
        }},
    )
