from db.session import SessionLocal
from db.models import World, Character
from sqlalchemy import select
from sqlalchemy.orm import Session
from embeds import CreateMultipleCharacterEmbeds

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

            embeds = CreateMultipleCharacterEmbeds(characters, world.name)
            await ctx.respond(embeds=embeds)
        
        except Exception as e:
            session.rollback()
            print(f"Error occured: {e}")
            await ctx.respond("Failed to view characters")
        finally:
            session.close()


