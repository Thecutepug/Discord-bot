import os
import discord
from discord.ext import commands

print("Connecting to Discord...")

intents = discord.Intents.all()
intents.messages = True
intents.guilds = True
intents.dm_messages = True
token = os.environ.get('DISCORD_TOKEN')
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Ignore messages from the bot itself

    if isinstance(message.channel, discord.DMChannel):
        # If the message is sent in a DM, forward it to a specific channel
        target_channel_id = 1182090592411471972  
        target_channel = bot.get_channel(target_channel_id)

        if message.content:
            await target_channel.send(f"**I recieved a message:**\n{message.content}")

        # Check if there are any attachments (images) and send them as well
        for attachment in message.attachments:
            await target_channel.send(f"**I recieved an image:** {attachment.url}")

    await bot.process_commands(message)

if token is None:
    print("Error: Discord bot token not found")
else:
    bot.run(os.environ["DISCORD_TOKEN"])
