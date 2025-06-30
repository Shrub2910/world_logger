from db.session import SessionLocal
from db.models import World, Character
from sqlalchemy import select
from sqlalchemy.orm import Session

import lightbulb

loader = lightbulb.Loader()

@loader.command
class AddCharacter(
    lightbulb.SlashCommand,
    name="add-character",
    description="Adds a character to your world."
):
    name = lightbulb.string("name", "Name of your character.")
    description = lightbulb.string("description", "Description of your character.")


    @lightbulb.invoke
    async def invoke(self, ctx:lightbulb.Context) -> None:
        session: Session = SessionLocal()
        try:
            stmt = select(World).where(World.discord_server_id == str(ctx.guild_id))
            result = session.execute(stmt)
            world = result.scalar_one_or_none()

            if world is None:
                await ctx.respond("Cannot create a character without a world!")
                return
            
            new_character = Character(
                name=self.name,
                description=self.description,
                world=world
            )

            session.add(new_character)
            session.commit()
            await ctx.respond("Succesfully created new character.")
        except Exception as e:
            session.rollback()
            print(f"Error occured: {e}")
            await ctx.respond("Error occured whilst making new character.")
        finally:
            session.close()
            

