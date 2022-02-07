class Interaction:
    def __init__(self, client, data):
        self.data = data.get("data")
        self.id = data["id"]
        self.type = data["type"]
        self.application_id = data["application_id"]
        self.guild_id = data.get("guild_id")
        self.channel_id = data.get("channel_id")
        self.member = data.get("member") or data.get("user")
        self.token = data["token"]
        self.message = data.get("message")
        self._http = client.http
        self.command = InteractionCommand(self.data)

    async def send(self, content=None, *, embed=None):
        data = {}
        if content is not None:
            data["content"] = content
        if embed is not None:
            data["embeds"] = [embed]
        payload = {
            "type": 4,
            "data": data
        }
        await self._http.request("POST", f"/interactions/{self.id}/{self.token}/callback", json=payload)

class InteractionCommand:
    def __init__(self, data):
        self.name = data["name"]
        self.id = data["id"]
        if data.get("options"):
            self.options = InteractionCommandOptions(data["options"])

class InteractionCommandOptions:
    def __init__(self, data):
        self.data = data

    def get(self, name: str):
        data = None
        for option in self.data:
            if option["name"] == name:
                data = option["value"]
        return data