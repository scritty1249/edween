import discord
from discord.ext import commands
from utils import file

command = "something"
configs = file.get_config()
# [!] Testing, remove on deploy
testing_configs = configs["testing"] if "testing" in configs.keys() else None

token = file.get_discord_key()
intents = discord.Intents.default()
intents.presences = True
intents.message_content = True
bot = commands.Bot(command_prefix='AYO ', intents=intents)
@bot.command(name = "TESTING")
async def test(ctx, *args):
    # [!] Testing, remove on deploy
    if testing_configs:
        if ctx.channel.id == testing_configs["watch-channel"]:
           await ctx.send("Echoing \"%s\"" % ", ".join(args))
           print("Response to %s sent successfully" % ctx)
bot.run(token)

