from pytest import fixture

from rmshared.content.taxonomy.graph.protocol import Protocol
from rmshared.content.taxonomy.graph.tests import fixtures


class TestProtocol:
    NOW = 1440000000

    @fixture
    def protocol(self) -> Protocol:
        return Protocol()

    def test_it_should_make_and_jsonify_posts(self, protocol: Protocol):
        post = protocol.make_post(data=fixtures.POST_1_DATA)
        assert post == fixtures.POST_1

        data = protocol.jsonify_post(post)
        assert data == fixtures.POST_1_DATA
