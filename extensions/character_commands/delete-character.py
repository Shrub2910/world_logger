from db.session import SessionLocal
from db.models import World, Character
from sqlalchemy import select
from sqlalchemy.orm import Session

import lightbulb

loader = lightbulb.Loader()

@loader.command
class DeleteCharacter(
    lightbulb.SlashCommand,
    name="delete-character",
    description="Deletes the chosen character"
):
    name = lightbulb.string("name", "Name of the charcter to be deleted.")

    @lightbulb.invoke
    async def invoke(self, ctx:lightbulb.Context) -> None:

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
                await ctx.respond("There is no character with this name!")
                return

            session.delete(character)
            session.commit()

            await ctx.respond("Succesfully deleted character!")
        except Exception as e:
            session.rollback()
            print(f"Error occured: {e}")
            await ctx.respond("Error occured whilst deleting character")
        finally:
            session.close()
