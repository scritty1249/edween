import discord
from discord.ext import commands
from utils import file

command = "something"
configs = file.getConfig()
# [!] Testing, remove on deploy
testingConfigs = configs["testing"] if "testing" in configs.keys() else None

token = file.getDiscordKey()

intents = discord.Intents.default()
intents.presences = True
intents.message_content = True
bot = commands.Bot(command_prefix='AYO ', intents=intents)
@bot.command(name = "TESTING")
async def test(ctx, *args):
    # [!] Testing, remove on deploy
    if testingConfigs:
        if ctx.channel.id == testingConfigs["watch-channel"]:
           await ctx.send("Echoing \"%s\"" % ", ".join(args))
           print("Response to %s sent successfully" % ctx)
bot.run(token)