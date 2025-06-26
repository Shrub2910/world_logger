from config import BOT_TOKEN
from db.session import engine
from db.models.base import Base

import db.models

Base.metadata.create_all(bind=engine)

import hikari
import lightbulb



bot = hikari.GatewayBot(BOT_TOKEN)
client = lightbulb.client_from_app(bot)

bot.subscribe(hikari.StartingEvent, client.start)

@client.register()
class TestCommand(lightbulb.SlashCommand, name="test", description="This is a test command."):
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        await ctx.respond("Hi!")

bot.run()

