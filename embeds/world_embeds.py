from db.models import World
import hikari

def CreateWorldEmbed(name, description, image, thumbnail):
    return hikari.Embed(title=name, description=description).set_image(hikari.URL(url=image)).set_thumbnail(hikari.URL(url=thumbnail))