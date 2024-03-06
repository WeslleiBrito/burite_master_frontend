import aiohttp
import asyncio
import locale
from datetime import datetime, timedelta

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


class Subgroup:

    @staticmethod
    async def get_resume_subgroups(url):
        async with (aiohttp.ClientSession() as session):
            async with session.get(url) as response:
                response_itens = await response.json()

                for index, item in enumerate(response_itens):
                    updated_at = datetime.strptime(response_itens[index]["updatedAt"], '%Y-%m-%dT%H:%M:%S.000Z')

                    new_date = datetime(year=updated_at.year, month=updated_at.month, day=updated_at.day,
                                        hour=updated_at.hour, minute=updated_at.minute, second=updated_at.second
                                        ) - timedelta(hours=3)

                    response_itens[index]["updatedAt"] = new_date.strftime('%d/%m/%Y %H:%M:%S')
                    response_itens[index]["fixedUnitExpense"] = locale.currency(
                        response_itens[index]["fixedUnitExpense"],
                        symbol=False
                    )
                return response_itens


async def main():
    url = 'http://192.168.0.112:3004/subgroup'
    subgroup = Subgroup()
    data = await subgroup.get_resume_subgroups(url)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
