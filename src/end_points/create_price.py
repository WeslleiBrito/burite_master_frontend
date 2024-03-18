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
    async def create_price_nfe(url_: str, code_nf):
        async with (aiohttp.ClientSession() as session):
            async with session.post(url_, json=code_nf) as response:
                content_type = response.headers.get('Content-Type', '').split(';')[0]

                if content_type == 'application/json':
                    # Se for JSON, processa normalmente
                    response_itens = await response.json()
                    return response_itens
                elif content_type == 'text/html':
                    # Se for texto, lida com a mensagem de erro
                    error_message = await response.text()
                    print("Erro:", error_message)
                    # Retorne None ou outro valor indicando um erro, ou levante uma exceção, conforme necessário
                    return None
                else:
                    # Se for outro tipo de conteúdo, lide com ele conforme necessário
                    print("Conteúdo desconhecido:", content_type)
                    # Retorne None ou outro valor indicando um erro, ou levante uma exceção, conforme necessário
                    return None


if __name__ == "__main__":
    prices = Prices()
    url = 'http://192.168.0.112:3004/price-formation'
    data = {
        "products": [
            {
                "codeProduct": 23321,
                "cost": 9,
                "profitPercentage": 5,
                "discount": 10,
                "quantity": 200
            },
            {
                "codeProduct": 23323,
                "cost": 12,
                "profitPercentage": 5,
                "quantity": 100,
                "discount": 10
            }
        ]
    }
    nf = {
        "codeNF": "126115"
    }
    result = asyncio.run(prices.create_price_nfe(url_=url, code_nf=nf))

    print(result)
