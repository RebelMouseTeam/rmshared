from __future__ import annotations

from rmshared.content.taxonomy.sql.descriptors import events
from rmshared.content.taxonomy.sql.descriptors import fields
from rmshared.content.taxonomy.sql.descriptors.abc import IRegistry
from rmshared.content.taxonomy.sql.descriptors.registry import Registry


class Factory:
    @staticmethod
    def make_registry() -> IRegistry:
        return Registry(descriptors=fields.FIELDS + events.EVENTS)
