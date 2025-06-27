from db.session import SessionLocal
from db.models import World
from sqlalchemy import select

import lightbulb

loader = lightbulb.Loader()

@loader.command
class DeleteWorld(
    lightbulb.SlashCommand,
    name="delete-world",
    description="Deletes the world associated with the discord server"
):
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        session = SessionLocal()

        try:
            stmt = select(World).where(World.discord_server_id==str(ctx.guild_id))
            result = session.execute(stmt)
            world = result.scalar_one_or_none()

            if world is None:
                await ctx.respond("World has not been created yet!")
            
            session.delete(world)
            session.commit()
            await ctx.respond("World deleted succesfully")
        except Exception as e:
            session.rollback()
            print(f"Error deleting world! {e}")
        finally:
            session.close()

