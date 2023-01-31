from rmshared.content.taxonomy.variables.abc import Variable
from rmshared.content.taxonomy.variables.producers.abc import ILabelsProducer

from rmshared.content.taxonomy.posts import labels


class PrimarySections(ILabelsProducer):
    def produce_labels(self, variable: Variable[int, int]):
        if variable.labels.none:
            yield labels.NoPrimarySections()
        for section_id in variable.values:
            yield labels.PrimarySection(section_id)


class RegularSections(ILabelsProducer):
    def produce_labels(self, variable: Variable[int, int]):
        if variable.labels.none:
            yield labels.NoRegularSections()
        for section_id in variable.values:
            yield labels.RegularSection(section_id)
