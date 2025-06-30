from db.session import SessionLocal
from db.models import World, Character
from sqlalchemy import select
from sqlalchemy.orm import Session

import lightbulb

loader = lightbulb.Loader()

@loader.command
class ViewAllCharacters(
    lightbulb.SlashCommand,
    name="view-all-characters",
    description="Let's you view every character in the world"
):
    @lightbulb.invoke
    async def invoke(self, ctx:lightbulb.Context) -> None:
        session: Session = SessionLocal()
        try:
            stmt = select(World).where(World.discord_server_id == str(ctx.guild_id))
            result = session.execute(stmt)
            world = result.scalar_one_or_none()

            if world is None:
                await ctx.respond("World has not been created yet!")
                return
            
            characters: list(Character) = world.characters

            message = ""

            for character in characters:
                message += f"{character.name}\n"
            
            if len(message) == 0:
                await ctx.respond("There are no characters in your world")
            else:
                await ctx.respond(message)
        except Exception as e:
            session.rollback()
            print(f"Error occured: {e}")
            await ctx.respond("Failed to view characters")
        finally:
            session.close()


