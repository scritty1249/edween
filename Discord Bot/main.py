import discord
from riotlib import exceptions as riot_exceptions
from riotlib import requests as riot_requests
from discord.ext import commands
from utils import file, messages, third_party_db
from json import dumps, loads
import random

command = "something"
configs = file.get_config()

# [!] Testing, remove on deploy
testing_configs = configs["testing"] if "testing" in configs.keys() else None

discord_token = file.get_discord_key()
riot_key = file.get_riot_key()
riot_requests.init_endpoints(riot_key)

intents = discord.Intents.default()
intents.presences = True
intents.message_content = True
bot = commands.Bot(command_prefix='AYO ', intents=intents)
@bot.command(name = "echo")
async def test(ctx, *args):
    # [!] Testing, remove on deploy
    if testing_configs:
        if ctx.channel.id == testing_configs["watch-channel"]:
           await ctx.send("Echoing \"%s\"" % ", ".join(args))
           print("Echoed \"%s\"" % ", ".join(args))

@bot.command(name="find")
async def get_summoner(ctx, *args):
    summoner_name, tagline = args[0].split("#", 2)
    puuid = riot_requests.get_summoner_puuid_by_name(summoner_name, tagline)
    summoner_data = riot_requests.get_raw_summoner_data(puuid)
    icon_img_url = riot_requests.get_image_asset("profileicon", "%s.png" % summoner_data["profileIconId"])
    await messages.send_profile_card(puuid, ctx, icon_img_url, summoner_name, tagline, summoner_data)
    print("Response to \"%s\" sent successfully" % ctx.message.content)

@bot.command(name="roast")
async def run(ctx, *args):
    if len(args) == 1:
        ...
        
    elif args[0].lower() == "aram":
        name = "noob"
        summoner_name, tagline = args[1].split("#", 2)
        puuid = riot_requests.get_summoner_puuid_by_name(summoner_name, tagline)
        try:
            current_game_info = riot_requests.get_raw_active_game(puuid)
        except riot_exceptions.NotFoundException as e:
            await ctx.send("Player is not currently in a game")
            return
        name = third_party_db.pick_random_name()
        if current_game_info["gameMode"] == "ARAM":
            await ctx.send("No hands ahh lookin %s" % name)
        elif current_game_info["gameMode"] == "CLASSIC":
            await ctx.send("No hands ahh lookin %s" % name)
        else:
            await ctx.send("dog")

bot.run(discord_token)