from typing import Callable
from typing import Mapping
from typing import Type

from rmshared.tools import ensure_map_is_complete

from rmshared.typings import read_only

from rmshared.content.taxonomy.sections import access
from rmshared.content.taxonomy.sections import consts
from rmshared.content.taxonomy.sections.abc import IAspects


class Aspects(IAspects):
    def __init__(self):
        self.read_access_kind_to_factory_func_map: Mapping[Type[access.Kind], Callable[[access.Kind], str]] = ensure_map_is_complete(access.Kind, {
            access.Public: lambda _: 'public()',
            access.Restricted: self._make_restricted_read_access_kind,
        })

    def map_section_read_access_kind(self, kind):
        return self.read_access_kind_to_factory_func_map[type(kind)](kind)

    @staticmethod
    def _make_restricted_read_access_kind(kind: access.Restricted) -> str:
        return f'restricted(inherited={str(kind.is_inherited).lower()})'

    def map_section_visibility_status(self, status):
        return self.SECTION_STATUS_TO_ID_MAP[status]

    SECTION_STATUS_TO_ID_MAP = read_only({
        consts.VISIBILITY.STATUS.LISTED: 'listed()',
        consts.VISIBILITY.STATUS.PRIVATE: 'private()',
        consts.VISIBILITY.STATUS.UNLISTED: 'unlisted()',
    })
    assert frozenset(SECTION_STATUS_TO_ID_MAP.keys()) == consts.VISIBILITY.STATUS.ALL
