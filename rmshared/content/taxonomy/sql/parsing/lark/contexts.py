from __future__ import annotations

from abc import ABCMeta
from contextlib import contextmanager
from functools import cached_property

from rmshared.content.taxonomy.sql.parsing.lark.abc import IFilters
from rmshared.content.taxonomy.sql.parsing.lark.abc import IContext
from rmshared.content.taxonomy.sql.parsing.lark.abc import IContextManager
from rmshared.content.taxonomy.sql.parsing.lark.fields import Fields
from rmshared.content.taxonomy.sql.parsing.lark.filters import ConstantFilters
from rmshared.content.taxonomy.sql.parsing.lark.filters import VariableFilters


class ContextManager(IContextManager):
    def __init__(self):
        self.context: IContext = GlobalContext.make_instance()

    @contextmanager
    def set_taxonomy_scope(self, scope):
        self.context = self.context.set_scope(scope)
        yield
        self.context = self.context.get_parent()

    @contextmanager
    def use_taxonomy_constant_filters(self):
        self.context = self.context.use_constant_filters()
        yield
        self.context = self.context.get_parent()

    @contextmanager
    def use_taxonomy_variable_filters(self, arguments):
        self.context = self.context.use_variable_filters(arguments)
        yield
        self.context = self.context.get_parent()


class BaseContext(IContext, metaclass=ABCMeta):
    def __init__(self, parent: IContext):
        self.parent = parent

    @property
    def fields(self):
        return self.parent.fields

    @property
    def filters(self):
        return self.parent.filters

    def set_scope(self, scope):
        return ScopedContext(scope, parent=self)

    def use_constant_filters(self):
        filters_ = ConstantFilters()
        return FilteredContext(filters_, parent=self)

    def use_variable_filters(self, arguments):
        filters_ = VariableFilters(arguments)
        return FilteredContext(filters_, parent=self)

    def get_parent(self):
        return self.parent


class GlobalContext(BaseContext):
    @classmethod
    def make_instance(cls) -> GlobalContext:
        return cls(parent=EmptyContext())


class ScopedContext(BaseContext):
    def __init__(self, scope: IContextManager.Scope, parent: IContext):
        self.scope = scope
        super().__init__(parent)

    @cached_property
    def fields(self):
        return Fields.make_instance(self.scope)


class FilteredContext(BaseContext):
    def __init__(self, filters: IFilters, parent: IContext):
        self.filters_ = filters
        super().__init__(parent)

    @property
    def filters(self):
        return self.filters_


class EmptyContext(IContext):
    @property
    def fields(self):
        raise RuntimeError('Cannot resolve fields in empty context')

    @property
    def filters(self):
        raise RuntimeError('Cannot resolve filters in empty context')

    def set_scope(self, scope):
        raise RuntimeError('Cannot set scope in empty context')

    def use_constant_filters(self):
        raise RuntimeError('Cannot use constant filters in empty context')

    def use_variable_filters(self, arguments):
        raise RuntimeError('Cannot use variable filters in empty context')

    def get_parent(self):
        raise RuntimeError('Cannot get parent in empty context')
