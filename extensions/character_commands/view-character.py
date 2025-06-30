from db.session import SessionLocal
from db.models import World, Character
from sqlalchemy import select
from sqlalchemy.orm import Session
from embeds import CreateCharacterEmbed

import lightbulb

loader = lightbulb.Loader()

@loader.command
class ViewCharacter(
    lightbulb.SlashCommand,
    name="view-character",
    description="Allows you to see information about an individual character."
):
    name = lightbulb.string("name", "The name of the character")

    @lightbulb.invoke
    async def invoke(self, ctx:lightbulb.Context):
        session: Session = SessionLocal()
        try:
            stmt = select(World).where(World.discord_server_id == str(ctx.guild_id))
            result = session.execute(stmt)
            world: World = result.scalar_one_or_none()

            if world is None:
                await ctx.respond("World has not been created yet!")
                return
            
            stmt = select(Character).where(Character.name == self.name, Character.world_id == world.id)
            result = session.execute(stmt)
            character: Character = result.scalar_one_or_none()

            if character is None:
                await ctx.respond("There is no character with that name!")
                return
            
            await ctx.respond(CreateCharacterEmbed(character.name, character.description, character.image, character.thumbnail))
        except Exception as e:
            session.rollback()
            print(f"Error occured {e}")
            await ctx.respond("Error whilst viewing character")
        finally:
            session.close()
