from db.session import SessionLocal
from db.models import World
from sqlalchemy import select
from sqlalchemy.orm import Session

import lightbulb

loader = lightbulb.Loader()

@loader.command
class EditWorld(
    lightbulb.SlashCommand,
    name="edit-world",
    description="Allows you to edit the name and description of the world."
):
    name = lightbulb.string("name", "The new name of the world.", min_length=3, default="")
    description = lightbulb.string("description", "The new description of the world.", min_length=3, default="")

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        session: Session = SessionLocal()

        try:
            stmt = select(World).where(World.discord_server_id == str(ctx.guild_id))
            result = session.execute(stmt)
            world = result.scalar_one_or_none()

            if world is None:
                await ctx.respond("World has not been created yet!")
                return 
            
            if len(self.name) >= 3:
                world.name = self.name
            
            if len(self.description) >=3:
                world.description = self.description

            session.commit()
            await ctx.respond("Succesfully updated world!")
        except Exception as e:
            session.rollback()
            print(f"Error has occured: {e}")
            await ctx.respond("Error updating world!")
        finally:
            session.close()

        
    
        