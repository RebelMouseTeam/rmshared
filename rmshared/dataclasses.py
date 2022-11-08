import dataclasses
import functools


def total_ordering(cls):
    def __lt__(self, other):
        if other is None:
            return False
        elif dataclasses.is_dataclass(other):
            self_tuple = (self.__class__.__module__, self.__class__.__qualname__) + dataclasses.astuple(self)
            other_tuple = (other.__class__.__module__, self.__class__.__qualname__) + dataclasses.astuple(other)
            return self_tuple < other_tuple
        else:
            return self.__class__ < other.__class__

    setattr(cls, '__lt__', __lt__)
    return functools.total_ordering(cls)
