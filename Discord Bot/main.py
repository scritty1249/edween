import discord
from utils import file

command = "something"
token = file.getDiscordKey()
intents = discord.Intents.default()

client = discord.Client(intents=intents)
@client.event
async def on_message(message):
    if message == command:
        print("Hello, World")
client.run(token)