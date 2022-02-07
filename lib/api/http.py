from websockets import connect
from aiohttp import ClientSession
import asyncio
import json

class ApiError(Exception):
    pass

class NotFoundError(ApiError):
    pass

class DiscordClientHttp:
    def __init__(self, client):
        self.base = "https://discord.com/api/v9"
        self.session = ClientSession(loop = client.loop)

    def _token(self, token:str):
        self.token = token

    async def connect(self, url):
        return await connect(url)

    async def json_or_text(self, r):
        if r.headers["Content-Type"] == "text/html":
            return r.text
        elif r.headers["Content-Type"] == "application/json":
            return await r.json()
        
    async def request(self, method, path, *args, **kwargs):
        headers = {
            "Authorization": f"Bot {self.token}"
        }
        if kwargs.get("json"):
            headers["Content-Type"] = "application/json"
        kwargs["headers"] = headers
        for i in range(5):
            async with self.session.request(method, self.base + path, *args, **kwargs) as r:
                if r.status == 404:
                    raise NotFoundError("Not found")
                elif r.status == 200 or r.status == 204:
                    return await self.json_or_text(r)
                elif r.status == 500 or r.status == 400:
                    data = await r.json()
                    raise ApiError(data["message"])
                elif r.status == 429:
                    if r.headers.get("X-RateLimit-Global"):
                        raise ApiError("Rate limit")
                    else:
                        await asyncio.sleep(int(r.headers["Retry-After"]))