from rmshared.content.taxonomy.core.traversal.abc import IAssembler
from rmshared.content.taxonomy.core.traversal.filters import Filters
from rmshared.content.taxonomy.core.traversal.labels import Labels
from rmshared.content.taxonomy.core.traversal.ranges import Ranges
from rmshared.content.taxonomy.core.traversal.events import Events


class Assembler(IAssembler):
    def make_filters(self, labels, ranges):
        return Filters(labels, ranges)

    def make_labels(self):
        return Labels()

    def make_ranges(self):
        return Ranges()

    def make_events(self):
        return Events()
