from db.session import SessionLocal
from db.models import World
from sqlalchemy import select
from sqlalchemy.orm import Session
from embeds import CreateWorldEmbed


import lightbulb

loader = lightbulb.Loader()

@loader.command
class ViewWorld(
    lightbulb.SlashCommand,
    name="view-world",
    description="Provides information about the world associated with the discord server"
):
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        session: Session = SessionLocal()
        try:
            stmt = select(World).where(World.discord_server_id==str(ctx.guild_id))
            result = session.execute(stmt)
            world = result.scalar_one_or_none()

            if world:
                await ctx.respond(CreateWorldEmbed(world.name, world.description, world.image, world.thumbnail))
            else:
                await ctx.respond("World has not been created yet!")
        finally:
            session.close()
