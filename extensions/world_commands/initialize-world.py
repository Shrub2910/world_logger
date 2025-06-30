from db.session import SessionLocal
from db.models import World
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import lightbulb

loader = lightbulb.Loader()

@loader.command
class InitializeWorld(
    lightbulb.SlashCommand,
    name="initialize-world",
    description="This command sets up the discord server to be a new world"
):
    name = lightbulb.string("name", "The name of your world", min_length=3)
    description = lightbulb.string("description", "The description of your world", min_length=3)

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        session: Session = SessionLocal()

        new_world = World(
            discord_server_id=str(ctx.guild_id),
            name=self.name,
            description=self.description
        )

        try:
            session.add(new_world)
            session.commit()
            await ctx.respond("Succesfully initialized world!")
        except IntegrityError:
            session.rollback()
            await ctx.respond("World already created in this server!")
        except Exception as e:
            session.rollback()
            print(f"Failed to insert {e}")
        finally:
            session.close()










