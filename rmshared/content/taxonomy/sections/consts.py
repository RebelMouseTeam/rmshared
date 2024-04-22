from typing import AbstractSet

from enumclasses import enumclass


class VISIBILITY:
    @enumclass()
    class STATUS:
        LISTED: 'VISIBILITY.STATUS' = object()
        UNLISTED: 'VISIBILITY.STATUS' = object()
        PRIVATE: 'VISIBILITY.STATUS' = object()

        ALL: AbstractSet['VISIBILITY.STATUS'] = frozenset({LISTED, UNLISTED, PRIVATE})
