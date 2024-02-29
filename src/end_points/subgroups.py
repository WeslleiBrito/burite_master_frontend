import aiohttp
import asyncio


class Subgroup:

    @staticmethod
    async def get_resume_subgroups(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()


async def main():
    url = 'http://localhost:3003/subgroup'
    subgroup = Subgroup()
    data = await subgroup.get_resume_subgroups(url)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
