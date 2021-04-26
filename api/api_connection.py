import aiohttp
from urllib.parse import urljoin


class ApiConnection:
    def __init__(self, base):
        self.base_url = base

    async def get(self, endpoint):
        url = urljoin(self.base_url, endpoint)
        # issue with ssl certs overridden by ssl=false
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.get(url) as r:
                json = await r.json()
                return json
