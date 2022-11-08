from typing import Dict

from aiohttp import web_request

from rebelmouse.requests import adapters
from rebelmouse.requests.interfaces import IRequest
from rebelmouse.requests.request import Request


class Factory:
    @classmethod
    def make_request_from_dict(cls, data: Dict) -> IRequest:
        adapter = adapters.StubDataAdapter()
        adapter = adapters.DictDataAdapter(adapter, data)
        return Request(adapter)

    @classmethod
    def make_request_from_aiohttp_request(cls, aiohttp_request: web_request.Request) -> IRequest:
        adapter = adapters.StubDataAdapter()
        adapter = adapters.AioHttpRequestDataAdapter(adapter, aiohttp_request)
        return Request(adapter)
