from rebelmouse.requests.interfaces import IRequest, IDataAdapter


class Request(IRequest):
    def __init__(self, adapter: IDataAdapter):
        self.adapter = adapter

    async def get_argument(self, cast_func, path, default=IRequest.MISSED):
        value = await self.adapter.get_argument(path, default)
        if value is IRequest.MISSED:
            raise self.MissingArgumentException('{}_is_missing'.format(path))

        if not isinstance(value, self.adapter.ListValue):
            return self._cast_value(cast_func, path, value)

        try:
            list_value = self._cast_value(cast_func, path, value.value)
        except self.InvalidArgumentException:
            pass
        else:
            if isinstance(list_value, list):
                return list_value

        try:
            value = value.value[0]
        except IndexError as e:
            raise self.MissingArgumentException('{}_is_missing'.format(path)) from e
        else:
            return self._cast_value(cast_func, path, value)

    def _cast_value(self, cast_func, name, value):
        try:
            return cast_func(value)
        except (ValueError, TypeError, AttributeError, LookupError) as e:
            raise self.InvalidArgumentException('{}_is_invalid'.format(name)) from e
