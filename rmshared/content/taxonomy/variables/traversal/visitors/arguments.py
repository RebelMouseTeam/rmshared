from typing import Any

from rmshared.content.taxonomy.variables.traversal.visitors.abc import IArguments


class Arguments(IArguments):
    def __init__(self, delegate: Any):
        self.delegate = delegate

    def visit_argument(self, argument):
        isinstance(self.delegate, IArguments) and self.delegate.visit_argument(argument)
