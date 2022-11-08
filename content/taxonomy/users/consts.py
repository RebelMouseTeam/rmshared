from typing import AbstractSet

from enumclasses import enumclass


class USER:
    @enumclass()
    class STATUS:
        ACTIVE: 'USER.STATUS' = object()
        INACTIVE: 'USER.STATUS' = object()

        ALL: AbstractSet['USER.STATUS'] = frozenset([ACTIVE, INACTIVE])
