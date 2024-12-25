"""# Library for sending Discord Messages
"""
from io import BytesIO
from typing import Union
from discord.ext.commands import Context
import discord
import requests
from utils import file, messages, third_party_db

def _get_image(url: str) -> Union[discord.File, None]:
    """Depreceated, no longer needed
    """
    file_name = url.rsplit("/", 2)[-1]
    data = requests.get(url).content
    with BytesIO(data) as image:
        return discord.File(image, file_name)

async def send_profile_card(puuid, ctx: Context, icon_url: str, summoner_name: str, summoner_tagline: str, summoner_data: dict) -> None:
    dev_puuid = file.get_dev_puuid()
    if puuid in dev_puuid.keys():
        description = "**TOP DOG GOAT PLAYER**"
    else:
        description = "I got the %s!" % third_party_db.pick_random_name()
    card = discord.Embed(
        title=summoner_name + f"#{summoner_tagline}",
        description=description,
        color=0xCD7F32 # bronze / shit brown
        )

    card.set_thumbnail(url = icon_url)
    for key, value in summoner_data.items():
        card.add_field(name=key, value=value)
    await ctx.send(embeds=[card])