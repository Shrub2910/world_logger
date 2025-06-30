from db.session import SessionLocal
from db.models import World, Character
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import lightbulb

loader = lightbulb.Loader()

@loader.command
class EditCharacter(
    lightbulb.SlashCommand,
    name="edit-character",
    description="Edit a character's properties"
):
    name = lightbulb.string("name", "The name of the character")
    new_name = lightbulb.string("new-name", "The new name of the character", min_length=3, default="")
    new_description = lightbulb.string("new-description", "The new description of the character", min_length=3, default="")
    new_image = lightbulb.string("new-image", "Image of your character.", default="")
    new_thumbnail = lightbulb.string("new-thumbnail", "Thumbnail of your character.", default="")

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context):
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
            
            if len(self.new_name) >= 3:
                character.name = self.new_name
            
            if len(self.new_description) >= 3:
                character.description = self.new_description

            if self.new_image != "":
                character.image = self.new_image

            if self.new_thumbnail != "":
                character.thumbnail = self.new_thumbnail

            session.commit()
            await ctx.respond("Succesfully updated character!")
        except IntegrityError:
            await ctx.respond("Character with this name already exists!")
        except Exception as e:
            session.rollback()
            print(f"Error occured: {e}")
            await ctx.respond("Error occured editing character!")
        finally:
            session.close()
