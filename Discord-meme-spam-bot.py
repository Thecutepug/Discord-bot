import os
import discord
from discord.ext import commands
import random

print("Connecting to Discord...")

intents = discord.Intents.all()
#intents.messages = True
#intents.guilds = True
#intents.dm_messages = True
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Ignore messages from the bot itself
    if isinstance(message.channel, discord.DMChannel):
        target_channel_id = 1182090592411471972  
        target_channel = bot.get_channel(target_channel_id)
        if message.content:
            await target_channel.send(f"**I received a message:**\n{message.content}")

        for attachment in message.attachments:
            await target_channel.send(f"**I received an image:** \n{attachment.url}")

    await bot.process_commands(message)

@bot.command(name='do_you_love_me', help='Ask the bot if it loves you')
async def do_you_love_me(ctx):
    responses = [
        "No",
        "Yes",
        "HAHAHAHAHAHA ... what?!",
    ]

    # Assigning probabilities to the responses
    weights = [0.5, 0.25, 0.25]

    response = random.choices(responses, weights)[0]
    await ctx.send(response)

@bot.command(name='hello', help='Say hello to the bot')
async def hello(ctx):
    await ctx.send(f'Hello {ctx.author.mention}!')

@bot.command(name='repeat', help='Repeat a message')
async def repeat(ctx, *, message):
    await ctx.send(f"I said: "(message))

bot.run(os.environ["DISCORD_TOKEN"])
