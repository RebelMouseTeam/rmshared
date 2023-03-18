from typing import Iterable
from typing import Type

from rmshared.content.taxonomy.protocols.abc import ILabels


class Labels(ILabels):
    def __init__(self, delegate: ILabels, fallback: ILabels, exceptions: Iterable[Type[Exception]]):
        self.delegate = delegate
        self.fallback = fallback
        self.exceptions = tuple(exceptions)

    def make_label(self, data):
        try:
            return self.delegate.make_label(data)
        except self.exceptions:
            return self.fallback.make_label(data)

    def jsonify_label(self, label):
        try:
            return self.delegate.jsonify_label(label)
        except self.exceptions:
            return self.fallback.jsonify_label(label)
