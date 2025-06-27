from config import BOT_TOKEN, TEST_GUILD
from db.session import engine
from db.models.base import Base

import db.models

Base.metadata.create_all(bind=engine)

import hikari
import lightbulb

import extensions

print(BOT_TOKEN)
print(TEST_GUILD)

bot = hikari.GatewayBot(BOT_TOKEN, intents=hikari.Intents.ALL)
client = lightbulb.client_from_app(bot)

@bot.listen(hikari.StartingEvent)
async def on_starting(_: hikari.StartingEvent) -> None:
    await client.load_extensions_from_package(package=extensions, recursive=True)
    await client.start()

bot.run()

