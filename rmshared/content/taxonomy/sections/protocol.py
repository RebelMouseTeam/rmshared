from typing import Any
from typing import Callable
from typing import Mapping
from typing import Type

from rmshared.tools import ensure_map_is_complete

from rmshared.typings import read_only

from rmshared.tools import invert_dict
from rmshared.tools import parse_name_and_info

from rmshared.content.taxonomy.sections import access
from rmshared.content.taxonomy.sections import consts
from rmshared.content.taxonomy.sections.abc import IProtocol


class Protocol(IProtocol):
    def __init__(self):
        self.read_access_kind_to_id_map: Mapping[Type[access.Kind], str] = ensure_map_is_complete(access.Kind, {
            access.Public: 'public',
            access.Restricted: 'restricted',
        })
        self.read_access_kind_from_id_map: Mapping[str, Type[access.Kind]] = invert_dict(self.read_access_kind_to_id_map)
        self.read_access_kind_to_make_func_map: Mapping[Type[access.Kind], Callable[[Mapping[str, Any]], ...]] = ensure_map_is_complete(access.Kind, {
            access.Public: lambda _: access.Public(),
            access.Restricted: self._make_restricted_read_access_kind,
        })
        self.read_access_kind_to_jsonify_info_func_map: Mapping[Type[access.Kind], Callable[[access.Kind], Mapping]] = ensure_map_is_complete(access.Kind, {
            access.Public: lambda _: {},
            access.Restricted: self._jsonify_restricted_read_access_kind_info,
        })

    def make_section_read_access_kind(self, data):
        name, info = parse_name_and_info(data)
        return self.read_access_kind_to_make_func_map[self.read_access_kind_from_id_map[name]](dict(info))

    def jsonify_section_read_access_kind(self, kind):
        name = self.read_access_kind_to_id_map[type(kind)]
        info = self.read_access_kind_to_jsonify_info_func_map[type(kind)](kind)
        return {name: info}

    @staticmethod
    def _make_restricted_read_access_kind(data: Mapping[str, Any]) -> access.Restricted:
        return access.Restricted(is_inherited=bool(data['is_inherited']))

    @staticmethod
    def _jsonify_restricted_read_access_kind_info(kind: access.Restricted) -> Mapping[str, Any]:
        return {'is_inherited': kind.is_inherited}

    def make_section_visibility_status(self, data):
        name, info = parse_name_and_info(data)
        assert not info
        return self.VISIBILITY_STATUS_FROM_ID_MAP[name]

    def jsonify_section_visibility_status(self, status):
        return {self.VISIBILITY_STATUS_TO_ID_MAP[status]: {}}

    VISIBILITY_STATUS_TO_ID_MAP = read_only({
        consts.VISIBILITY.STATUS.LISTED: 'listed',
        consts.VISIBILITY.STATUS.PRIVATE: 'private',
        consts.VISIBILITY.STATUS.UNLISTED: 'unlisted',
    })
    VISIBILITY_STATUS_FROM_ID_MAP = invert_dict(VISIBILITY_STATUS_TO_ID_MAP)
    assert frozenset(VISIBILITY_STATUS_FROM_ID_MAP.values()) == consts.VISIBILITY.STATUS.ALL
