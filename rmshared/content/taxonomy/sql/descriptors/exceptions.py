from typing import Any
from typing import Type

from rmshared.content.taxonomy.sql.descriptors import scopes


class SubjectNotFoundException(LookupError):
    def __init__(self, subject: Any):
        super().__init__(f'Descriptor not found for subject "{subject}"')
        self.subject = subject


class DescriptorNotFoundException(LookupError):
    def __init__(self, alias: str, scope: scopes.Scope, subject_type: Type[Any]):
        super().__init__(f'Descriptor not found for alias "{alias}" in scope "{scope}" among subjects of type "{subject_type}"')
        self.alias = alias
        self.scope = scope
        self.subject_type = subject_type
