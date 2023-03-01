from typing import Collection

from rmshared.content.taxonomy.mappers.abc import ILabels
from rmshared.content.taxonomy.mappers.abc import IRanges
from rmshared.content.taxonomy.mappers.abc import IFields


class Labels(ILabels):
    def __init__(self, mappers: Collection[ILabels]):
        assert len(mappers) > 0
        self.mappers = mappers

    def map_label(self, label):
        for mapper in self.mappers:
            try:
                return mapper.map_label(label)
            except LookupError:
                pass
        else:
            raise LookupError(['mapper_not_found', label])


class Ranges(IRanges):
    def __init__(self, mappers: Collection[IRanges]):
        assert len(mappers) > 0
        self.mappers = mappers

    def map_range(self, range_):
        for mapper in self.mappers:
            try:
                return mapper.map_range(range_)
            except LookupError:
                pass
        else:
            raise LookupError(['mapper_not_found', range_])


class Fields(IFields):
    def __init__(self, mappers: Collection[IFields]):
        assert len(mappers) > 0
        self.mappers = mappers

    def map_field(self, field):
        for mapper in self.mappers:
            try:
                return mapper.map_field(field)
            except LookupError:
                pass
        else:
            raise LookupError(['mapper_not_found', field])
