import os
import discord
from discord.ext import commands

print("Connecting to Discord...")   #To see if code is running

intents = discord.Intents.all() #Specifying discord intents as it is a requirement
intents.messages = True
intents.guilds = True
intents.dm_messages = True
bot = commands.Bot(command_prefix="/", intents=intents)     #Spesifying Bot command prefix

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Ignore messages from the bot itself

    if isinstance(message.channel, discord.DMChannel):            # If the message is sent in a DM, forward it to a specific channel
        
        target_channel_id = 1182090592411471972  
        target_channel = bot.get_channel(target_channel_id)

        if message.content:
            await target_channel.send(f"**I recieved a message:**\n{message.content}")

        # Check if there are any attachments (images) and send them as well
        for attachment in message.attachments:
            await target_channel.send(f"**I recieved an image:**\n{attachment.url}")

    await bot.process_commands(message) 

bot.run(os.environToken)

print("Bot running :)")
