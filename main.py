from lib.api import Client
from lib.types import Interaction
from lib.translate import translate
from lib.events import Event
from os import getenv
import traceback

client = Client()
app = Event(client.loop)

@client.on("ready")
async def ready():
    print("ready")
    print(client.user)
    data = {
        "type": 3,
        "name": "test"
    }

@client.on("interaction_create")
async def interaction_create(data):
    interaction = Interaction(client, data)
    if interaction.type == 2:
        # 翻訳
        app.dispatch(interaction.data["name"], interaction)
                     
@app.on("japanese")
async def japanese(interaction):
    await translate(interaction, "ja")

@app.on("english")
async def english(interaction):
    await translate(interaction, "en")

@app.on("italian")
async def italian(interaction):
    await translate(interaction, "it")

client.loop.run_until_complete(client.start(getenv("token")))