import discord

command = "something"
token = getDiscordToken()

client = discord.Client()
@client.event
async def on_message(message):
    if message == command:
        ...
client.run(token)