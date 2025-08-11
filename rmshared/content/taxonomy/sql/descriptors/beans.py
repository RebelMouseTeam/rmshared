from collections.abc import Sequence
from collections.abc import Set
from dataclasses import dataclass
from typing import Generic
from typing import TypeVar

from rmshared.content.taxonomy.sql.descriptors import scopes
from rmshared.content.taxonomy.sql.descriptors import options

Subject = TypeVar('Subject')


@dataclass(frozen=True)
class Descriptor(Generic[Subject]):
    scope: scopes.Scope
    subject: Subject
    aliases: Sequence[str]
    options: Set[options.Option]
