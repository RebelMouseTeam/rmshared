from unittest.mock import Mock
from unittest.mock import call
from pytest import fixture

from rmshared.content.taxonomy.core import events
from rmshared.content.taxonomy.core.sql.compiling.abc import IDescriptors
from rmshared.content.taxonomy.core.sql.compiling.events import Events


class TestEvents:
    @fixture
    def events_(self, descriptors: IDescriptors) -> Events:
        return Events(descriptors)

    @fixture
    def descriptors(self) -> Mock | IDescriptors:
        return Mock(spec=IDescriptors)

    def test_it_should_compile_event(self, events_: Events, descriptors: Mock | IDescriptors):
        descriptors.get_event_alias = Mock(return_value='events.user_login')

        event = events.Event(name='user_login')
        tree = events_.make_tree_from_event(event)
        compiled = list(tree.compile())

        assert compiled == ['events.user_login']
        assert descriptors.get_event_alias.call_args_list == [call(event)]
