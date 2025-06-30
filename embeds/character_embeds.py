from db.models import Character
import hikari

def CreateCharacterEmbed(name, description, image, thumbnail):
    embed = hikari.Embed(title=name, description=description).set_image(hikari.URL(url=image)).set_thumbnail(hikari.URL(url=thumbnail))
    return embed

def CreateMultipleCharacterEmbeds(characters, world_name):
    embeds = []

    top_embed = hikari.Embed(title=f"Characters of {world_name}")
    embeds.append(top_embed)

    for character in characters:
        embeds.append(CreateCharacterEmbed(character.name, character.description, character.image, character.thumbnail))
    
    return embeds

