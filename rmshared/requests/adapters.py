from typing import Dict

from aiohttp import web_request

from rmshared.tools import ItemGetter

from rebelmouse.requests.interfaces import IDataAdapter, IRequest


class StubDataAdapter(IDataAdapter):
    async def get_argument(self, path, default):
        return default


class DictDataAdapter(IDataAdapter):
    def __init__(self, delegate: IDataAdapter, data: Dict):
        self.delegate = delegate
        self.data = data

    async def get_argument(self, path, default):
        if path is IRequest.PAYLOAD:
            return self.data

        value_getter = ItemGetter(path)
        try:
            return value_getter(self.data)
        except LookupError:
            return await self.delegate.get_argument(path, default)


class AioHttpRequestDataAdapter(IDataAdapter):
    NOT_LOADED = object()

    def __init__(self, delegate: IDataAdapter, request: web_request.Request):
        self.delegate = delegate
        self.request = request
        self.data = self.NOT_LOADED

    async def get_argument(self, path, default):
        if path is IRequest.PAYLOAD:
            return await self._get_or_load_json_data()

        try:
            return self.request.match_info[path]
        except LookupError:
            pass

        try:
            value = self.request.query.getall(path)
        except LookupError:
            pass
        else:
            return self.ListValue(value=value)

        try:
            value = (await self.request.post()).getall(path)
        except LookupError:
            pass
        else:
            return self.ListValue(value)

        try:
            data = await self._get_or_load_json_data()
        except (TypeError, ValueError):
            return await self.delegate.get_argument(path, default)
        else:
            return await DictDataAdapter(self.delegate, data).get_argument(path, default)

    async def _get_or_load_json_data(self) -> Dict:
        if self.data is not self.NOT_LOADED:
            return self.data
        elif self.request.can_read_body:
            self.data = await self.request.json()
            return self.data
        else:
            raise TypeError()
