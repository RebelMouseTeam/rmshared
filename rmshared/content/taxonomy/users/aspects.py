from rmshared.tools import ensure_map_is_complete

from rmshared.content.taxonomy.users import consts
from rmshared.content.taxonomy.users import statuses
from rmshared.content.taxonomy.users.abc import IAspects


class Aspects(IAspects):
    def __init__(self):
        self.user_status_to_factory_func_map = ensure_map_is_complete(statuses.Status, {
            statuses.Active: lambda _: 'active',
            statuses.Pending: lambda _: 'pending',
            statuses.Inactive: self._map_inactive_user_profile_status,
        })

    def map_user_profile_status(self, status):
        return self.user_status_to_factory_func_map[type(status)](status)

    @staticmethod
    def _map_inactive_user_profile_status(status: statuses.Inactive) -> str:
        return f'inactive(banned={str(status.is_banned).lower()})'

    def map_user_status(self, status):
        return self.USER_STATUS_TO_ID_MAP[status]

    USER_STATUS_TO_ID_MAP = {
        consts.USER.STATUS.ACTIVE: 'active',
        consts.USER.STATUS.INACTIVE: 'inactive',
    }
    assert set(USER_STATUS_TO_ID_MAP.keys()) == consts.USER.STATUS.ALL
