from lib.api import Client
from lib.types import Interaction
from async_google_trans_new import AsyncTranslator
from os import getenv

client = Client()
g = AsyncTranslator()

@client.on("ready")
async def ready():
    print("ready")
    print(client.user)

@client.on("interaction_create")
async def interaction_create(data):
    interaction = Interaction(client, data)
    if interaction.type == 2:
        if interaction.data["name"] == "japanese":
            m = interaction.data["resolved"]["messages"][interaction.data['target_id']]
            content = m["content"]
            try:
                result = await g.translate(content, "ja")
            except Exception as e:
                result = f"エラーが発生しました\n{e}"
            await interaction.send(embed = {
                "title": "translate",
                "fields": [
                    {
                        "name": "before",
                        "value": content
                    },
                    {
                        "name": "after",
                        "value": result
                    }
                ]
            })

client.loop.run_until_complete(client.start(getenv("token")))