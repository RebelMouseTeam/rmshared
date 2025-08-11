from collections.abc import Collection
from typing import Any


class UnknownScopeError(LookupError):
    def __init__(self, scope: str):
        super().__init__(f'Unknown scope: `{scope}`')
        self.scope = scope


class UnknownFieldError(LookupError):
    def __init__(self, scope: str, field: str):
        super().__init__(f'Unknown field: `{scope}.{field}`')
        self.scope = scope
        self.field = field


class DeprecatedFieldError(LookupError):
    def __init__(self, scope: str, field: str):
        super().__init__(f'Field `{scope}.{field}` is deprecated and will be removed in future versions')
        self.scope = scope
        self.field = field


class NotSupportedFieldError(LookupError):
    def __init__(self, scope: str, field: str):
        super().__init__(f'Field `{scope}.{field}` is not supported yet')
        self.scope = scope
        self.field = field


class CustomFieldScopeError(LookupError):
    def __init__(self, scope: str):
        super().__init__(f'Custom field does not exist in scope: `{scope}`')
        self.scope = scope


class NotIdFieldError(LookupError):
    def __init__(self, scope: str, field: str):
        super().__init__(f'Field `{scope}.{field}` is not an ID field')
        self.scope = scope
        self.field = field


class NotBadgeFieldError(LookupError):
    def __init__(self, scope: str, field: str):
        super().__init__(f'Field `{scope}.{field}` is not a boolean field')
        self.scope = scope
        self.field = field


class NotSingleValueFieldError(LookupError):
    def __init__(self, scope: str, field: str):
        super().__init__(f'Field `{scope}.{field}` is either boolean or can contain more than one value')
        self.scope = scope
        self.field = field


class NotMultiValueFieldError(LookupError):
    def __init__(self, scope: str, field: str):
        super().__init__(f'Field `{scope}.{field}` is either boolean or contain exactly one value')
        self.scope = scope
        self.field = field


class UnknownEventError(LookupError):
    def __init__(self, scope: str, event: str):
        super().__init__(f'Unknown event: `{scope}.{event}`')
        self.scope = scope
        self.event = event


class DeprecatedEventError(LookupError):
    def __init__(self, scope: str, event: str):
        super().__init__(f'Event `{scope}.{event}` is deprecated and will be removed in future versions')
        self.scope = scope
        self.event = event


class NotSupportedEventError(LookupError):
    def __init__(self, scope: str, event: str):
        super().__init__(f'Event `{scope}.{event}` is not supported yet')
        self.scope = scope
        self.event = event


class VariablesAreNotSupportedError(ValueError):
    def __init__(self):
        super().__init__(f'Variables are not supported in this context')


class VariableValuesOfDifferentTypesError(TypeError):
    def __init__(self, types: Collection[type]):
        super().__init__(f'Expected all variable values have the same type. Got: {", ".join(t.__name__ for t in types)}')
        self.types = types


class VariableAliasError(LookupError):
    def __init__(self, alias: str, arguments: Collection[str] = ()):
        super().__init__(f'Variable alias `{alias}` is not defined. Available aliases: {", ".join(arguments)}')
        self.alias = alias
        self.arguments = arguments


class ArgumentIndexError(LookupError):
    def __init__(self, index: int, arguments: int):
        super().__init__(f'Argument index {index} is out of range (1-{arguments}')
        self.index = index
        self.arguments = arguments


class ArgumentCanBeOptionalError(LookupError):
    def __init__(self, alias: str, yields: Collection[Any]):
        super().__init__(f'Argument `{alias}` can be optional. Yields: {", ".join(yields)}')
        self.alias = alias
        self.yields = yields


class ArgumentNotOptionalError(LookupError):
    def __init__(self, alias: str, yields: Collection[Any]):
        super().__init__(f'Argument `{alias}` is not optional. Yields: {", ".join(yields)}')
        self.alias = alias
        self.yields = yields


class ArgumentNotDefinedError(LookupError):
    def __init__(self, alias: str):
        super().__init__(f'Argument `{alias}` is not defined in the current context')
        self.alias = alias


class ArgumentNotFoundError(LookupError):
    def __init__(self, alias: str):
        super().__init__(f'Argument `{alias}` is not found in the current context')
        self.alias = alias


class ArgumentNotUsedError(LookupError):
    def __init__(self, alias: str):
        super().__init__(f'Argument `{alias}` is not used in the current context')
        self.alias = alias
