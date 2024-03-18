import aiohttp
import asyncio
import locale
from datetime import datetime

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


class ListPurchasesAll:

    @staticmethod
    async def list_prices(url_):
        async with (aiohttp.ClientSession() as session):
            async with session.get(url_) as response:
                response_itens = await response.json()

                return response_itens


# if __name__ == "__main__":
#     prices = Prices()
#     url = 'http://192.168.0.112:3004/price-formation'
#     data = {
#         "products": [
#             {
#                 "codeProduct": 23321,
#                 "cost": 9,
#                 "profitPercentage": 5,
#                 "discount": 10,
#                 "quantity": 200
#             },
#             {
#                 "codeProduct": 23323,
#                 "cost": 12,
#                 "profitPercentage": 5,
#                 "quantity": 100,
#                 "discount": 10
#             }
#         ]
#     }
#     nf = {
#         "codeNF": "126115"
#     }
#     result = asyncio.run(prices.list_prices(url_=url))
# 
#     print(result)
