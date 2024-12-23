import discord
from utils import file

command = "something"
token = file.getDiscordKey()

client = discord.Client()
@client.event
async def on_message(message):
    if message == command:
        ...
client.run(token)