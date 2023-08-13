from typing import Any
from typing import Callable
from typing import Mapping
from typing import Type
from typing import TypeVar

from rmshared.tools import invert_dict
from rmshared.tools import parse_name_and_info
from rmshared.tools import ensure_map_is_complete

from rmshared.content.taxonomy.users import consts
from rmshared.content.taxonomy.users import statuses
from rmshared.content.taxonomy.users.abc import IProtocol

Status = TypeVar('Status', bound=statuses.Status)


class Protocol(IProtocol):
    def __init__(self):
        self.user_profile_status_to_id_map: Mapping[Type[Status], str] = ensure_map_is_complete(statuses.Status, {
            statuses.Active: 'active',
            statuses.Pending: 'pending',
            statuses.Inactive: 'inactive',
        })
        self.user_profile_status_from_id_map: Mapping[str, Type[Status]] = invert_dict(self.user_profile_status_to_id_map)
        self.user_profile_status_to_make_func_map: Mapping[Type[Status], Callable[[Mapping[str, Any]], Status]] = ensure_map_is_complete(statuses.Status, {
            statuses.Active: lambda _: statuses.Active(),
            statuses.Pending: lambda _: statuses.Pending(),
            statuses.Inactive: self._make_inactive_user_profile_status,
        })
        self.user_profile_status_to_jsonify_info_func_map = ensure_map_is_complete(statuses.Status, {
            statuses.Active: lambda _: {},
            statuses.Pending: lambda _: {},
            statuses.Inactive: self._jsonify_inactive_user_profile_status_info,
        })

    def make_user_status(self, data):
        name, info = parse_name_and_info(data)
        assert not info
        return self.USER_STATUS_FROM_ID_MAP[name]

    def jsonify_user_status(self, status):
        return {self.USER_STATUS_TO_ID_MAP[status]: {}}

    USER_STATUS_TO_ID_MAP = {
        consts.USER.STATUS.ACTIVE: 'active',
        consts.USER.STATUS.INACTIVE: 'inactive',
    }
    USER_STATUS_FROM_ID_MAP = invert_dict(USER_STATUS_TO_ID_MAP)
    assert frozenset(USER_STATUS_FROM_ID_MAP.values()) == consts.USER.STATUS.ALL

    def make_user_profile_status(self, data):
        name, info = parse_name_and_info(data)
        return self.user_profile_status_to_make_func_map[self.user_profile_status_from_id_map[name]](dict(info))

    def jsonify_user_profile_status(self, status):
        name = self.user_profile_status_to_id_map[type(status)]
        info = self.user_profile_status_to_jsonify_info_func_map[type(status)](status)
        return {name: info}

    @staticmethod
    def _make_inactive_user_profile_status(info: Mapping[str, Any]) -> statuses.Inactive:
        return statuses.Inactive(is_banned=bool(info['is_banned']))

    @staticmethod
    def _jsonify_inactive_user_profile_status_info(status: statuses.Inactive) -> Mapping[str, Any]:
        return {'is_banned': status.is_banned}
