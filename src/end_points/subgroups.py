import aiohttp
import asyncio
import locale
from datetime import datetime

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


class Subgroup:

    @staticmethod
    async def get_resume_subgroups(url):
        async with (aiohttp.ClientSession() as session):
            async with session.get(url) as response:
                response_itens = await response.json()

                for index, item in enumerate(response_itens):
                    updated_at = datetime.strptime(response_itens[index]["updatedAt"], '%Y-%m-%dT%H:%M:%S.000Z')

                    response_itens[index]["updatedAt"] = updated_at

                return response_itens
