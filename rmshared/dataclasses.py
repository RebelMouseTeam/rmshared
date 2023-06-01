import dataclasses
import functools
import operator


def total_ordering(cls):
    def __lt__(self, other):
        if other is None:
            return False
        elif dataclasses.is_dataclass(other):
            self_tuple = get_dataclass_key(self)
            other_tuple = get_dataclass_key(other)
            return self_tuple < other_tuple
        else:
            return self.__class__ < other.__class__

    def get_dataclass_key(dc: dataclasses.dataclass) -> tuple:
        attrs = zip(map(operator.attrgetter('name'), dataclasses.fields(dc)), dataclasses.astuple(dc))
        return (dc.__class__.__module__, dc.__class__.__qualname__) + tuple(attrs)

    setattr(cls, '__lt__', __lt__)
    return functools.total_ordering(cls)
