import aiohttp
import asyncio
import locale
from datetime import datetime

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


class Prices:

    @staticmethod
    async def create_price_product(url_, data_nf: any):
        async with (aiohttp.ClientSession() as session):
            async with session.post(url_, json=data_nf) as response:
                response_itens = await response.json()

                return response_itens

    @staticmethod
    async def create_price_nfe(url_: str, commission=None):
        async with (aiohttp.ClientSession() as session):
            async with session.post(url_, json=commission) as response:
                response_itens = await response.json()
                return response_itens

