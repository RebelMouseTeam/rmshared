from rmshared.content.taxonomy import core
from rmshared.content.taxonomy.mappers.abc import IFields
from rmshared.content.taxonomy.mappers.abc import IRanges


class Ranges(IRanges):
    def __init__(self, fields: IFields):
        self.fields = fields

    def map_range(self, range_):
        field = self.fields.map_field(range_.field)
        if None not in {range_.min_value, range_.max_value}:
            return core.ranges.Between(field, min_value=range_.min_value, max_value=range_.max_value)
        elif range_.max_value is not None:
            return core.ranges.LessThan(field, value=range_.max_value)
        elif range_.min_value is not None:
            return core.ranges.MoreThan(field, value=range_.min_value)
        else:
            return []
