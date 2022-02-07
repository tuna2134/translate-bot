from .http import DiscordClientHttp
from .gateway import DiscordGateway
from asyncio import get_event_loop

class Client:
    def __init__(self):
        self.loop = get_event_loop() 
        self.http = DiscordClientHttp(self)
        self.listens = {}
        self.request = self.http.request

    def dispatch(self, name, *args, **kwargs):
        if name in self.listens:
            for coro in self.listens[name]:
                self.loop.create_task(coro(*args, **kwargs))

    def on(self, name:str):
        name = name.upper()
        def decorator(coro):
            if name in self.listens:
                self.listens[name].append(coro)
            else:
                self.listens[name] = [coro]
        return decorator

    async def login(self, token):
        self.http._token(token)
        self.user = await self.http.request("GET", "/users/@me")

    async def connect(self):
        self.ws = await DiscordGateway.start_gateway(self)
        while not self.ws.closed:
            await self.ws.receive()

    async def start(self, token):
        await self.login(token)
        await self.connect()