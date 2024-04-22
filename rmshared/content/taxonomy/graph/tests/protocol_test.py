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

    def test_it_should_make_and_jsonify_sections(self, protocol: Protocol):
        section_1 = protocol.make_section(data=fixtures.SECTION_1_DATA)
        assert section_1 == fixtures.SECTION_1

        data_1 = protocol.jsonify_section(section_1)
        assert data_1 == fixtures.SECTION_1_DATA

        section_2 = protocol.make_section(data=fixtures.SECTION_2_DATA)
        assert section_2 == fixtures.SECTION_2

        data_2 = protocol.jsonify_section(section_2)
        assert data_2 == fixtures.SECTION_2_DATA

    def test_it_should_make_and_jsonify_user_profiles(self, protocol: Protocol):
        user_profile_1 = protocol.make_user_profile(data=fixtures.USER_PROFILE_1_DATA)
        assert user_profile_1 == fixtures.USER_PROFILE_1

        data_1 = protocol.jsonify_user_profile(user_profile_1)
        assert data_1 == fixtures.USER_PROFILE_1_DATA
