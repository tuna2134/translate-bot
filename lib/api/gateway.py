import json
import asyncio

class HeartBeat:
    def __init__(self, ws):
        self.ws = ws

    async def send_beat(self):
        await self.ws.send({
            "op": 1,
            "d": self.ws.sequence
        })

    async def start_beat(self):
        while not self.ws.closed:
            await self.send_beat()
            await asyncio.sleep(10)

class DiscordGateway:
    def __init__(self, ws, client):
        self.ws = ws
        self.client = client
        self.closed = ws.closed
        
    @classmethod
    async def start_gateway(cls, client):
        ws = await client.http.connect("wss://gateway.discord.gg")
        self = cls(ws, client)
        await self.receive()
        return self

    async def send(self, data):
        return await self.ws.send(json.dumps(data))

    async def receive(self):
        text = await self.ws.recv()
        data = json.loads(text)
        self.sequence = data["s"]
        if data["op"] == 10:
            token = self.client.http.token
            await self.send({
                "op": 2,
                "d": {
                    "token": token,
                    "intents": 513,
                    "properties": {
                        "$os": "linux",
                        "$browser": "discord.py",
                        "$device": "discord.py"
                    }
                }
            })
            self.heartbeat = HeartBeat(self)
            await self.heartbeat.send_beat()
            self.client.loop.create_task(self.heartbeat.start_beat())

        elif data["op"] == 0:
            if data["t"] == "READY":
                self.client.dispatch(data["t"])
            else:
                self.client.dispatch(data["t"], data["d"])