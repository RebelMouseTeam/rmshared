from rmshared.content.taxonomy.core import traversal
from rmshared.content.taxonomy.core.sql.compiling.abc import IDescriptors
from rmshared.content.taxonomy.core.sql.compiling.abc import IAssembler
from rmshared.content.taxonomy.core.sql.compiling.filters import Filters
from rmshared.content.taxonomy.core.sql.compiling.labels import Labels
from rmshared.content.taxonomy.core.sql.compiling.ranges import Ranges
from rmshared.content.taxonomy.core.sql.compiling.fields import Fields
from rmshared.content.taxonomy.core.sql.compiling.events import Events
from rmshared.content.taxonomy.core.sql.compiling.values import Values


class Assembler(IAssembler):
    def __init__(self, descriptors: IDescriptors):
        self.descriptors = descriptors
        self.traversal = traversal.Factory.make_instance().make_composite()

    def make_filters(self, labels_, ranges_):
        return Filters(labels_, ranges_)

    def make_labels(self, fields_, values_):
        return Labels(fields_, values_, self.traversal)

    def make_ranges(self, fields_, values_):
        return Ranges(fields_, values_, self.traversal)

    def make_fields(self):
        return Fields(self.descriptors)

    def make_events(self):
        return Events(self.descriptors)

    def make_values(self):
        return Values()
