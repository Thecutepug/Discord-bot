import os
import discord
import openai
from discord.ext import commands, tasks
import random
from datetime import datetime, timedelta

import openai

print("Connecting to Discord...")

intents = discord.Intents.all()
#intents.messages = True
#intents.guilds = True
#intents.dm_messages = True
bot = commands.Bot(command_prefix=";", intents=intents, help_command=commands.DefaultHelpCommand())


@tasks.loop(hours=4)
async def bump_task(channel):
    await channel.send("/bump")

#Chat GPT stuff
MODEL_NAME = 'gpt-3.5-turbo'
@bot.command()
async def ask(ctx, *, question):
    # Send initial 'Thinking...' message
    temp_message = await ctx.send("Thinking...")

    try:
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model=MODEL_NAME,
             messages=[{"role": "user", "content": question}]
        )

        # Edit the 'Thinking...' message with the response
        await temp_message.edit(content=response.choices[0].message['content'])
    except Exception as e:
        # In case of an error, edit the message to indicate failure
        await temp_message.edit(content=f"Sorry, I couldn't process that request. Error: {e}")

#Launch event in console
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    '''
    bump_channel_id = 1184324679473840208
    bump_channel = bot.get_channel(bump_channel_id)

    # Start the background task to send "/bump" every 4 hours
    bump_task.start(bump_channel)
    '''

#Loop Tasks
'''
@tasks.loop(hours=4)
async def bump_task(channel):
    await channel.send("/bump")
'''

#DM bot command
'''
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
'''
    
#Do you love me command
@bot.command(name='do_you_love_me', help='Ask the bot if it loves you')
async def do_you_love_me(ctx):
    responses = [
        "No",
        "Yes",
        "HAHAHAHAHAHA ... what?!",
        "K."
    ]

    # Assigning probabilities to the responses
    weights = [0.49, 0.25, 0.25,0.01]

    response = random.choices(responses, weights)[0]
    await ctx.send(response)

#Hello Command
@bot.command(name='hello', help='Say hello to the bot')
async def hello(ctx):
    await ctx.send(f'Hello {ctx.author.mention}!')


#Runs Bot
bot.run(os.environ["DISCORD_TOKEN"])
