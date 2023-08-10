from pytest import fixture

from rmshared.content.taxonomy.graph.protocol import Protocol
from rmshared.content.taxonomy.graph.tests import fixtures


class TestProtocol:
    NOW = 1440000000

    @fixture
    def protocol(self) -> Protocol:
        return Protocol()

    def test_it_should_make_and_jsonify_posts(self, protocol: Protocol):
        post_1 = protocol.make_post(data=fixtures.POST_1_DATA)
        assert post_1 == fixtures.POST_1

        data_1 = protocol.jsonify_post(post_1)
        assert data_1 == fixtures.POST_1_DATA

        post_2 = protocol.make_post(data=fixtures.POST_2_DATA)
        assert post_2 == fixtures.POST_2

        data_2 = protocol.jsonify_post(post_2)
        assert data_2 == fixtures.POST_2_DATA
