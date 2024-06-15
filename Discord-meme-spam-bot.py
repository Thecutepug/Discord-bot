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
bot = commands.Bot(command_prefix="$", intents=intents, help_command=commands.DefaultHelpCommand())
openai.api_key = os.getenv('OPENAI_API_KEY')
MODEL_NAME = 'gpt-3.5-turbo'

#Chat GPT stuff
user_chat_histories = {}
MAX_HISTORY_MESSAGES = 5  # Number of messages to retain in history
@bot.command(name='ask', help='Asks ChatGPT a question')
async def ask(ctx, *, question):
    # Send initial 'Thinking...' message
    temp_message = await ctx.send("Thinking...")
    user_id = str(ctx.author.id)

    # Initialize or update chat history
    if user_id not in user_chat_histories:
        user_chat_histories[user_id] = []
    user_chat_histories[user_id].append({"role": "user", "content": question})

    # Keep only the most recent part of the chat history
    user_chat_histories[user_id] = user_chat_histories[user_id][-MAX_HISTORY_MESSAGES:]

    try:
        # Call OpenAI API with the user's chat history
        response = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=user_chat_histories[user_id]
        )

        # Process response
        bot_response = response.choices[0].message['content']
        user_chat_histories[user_id].append({"role": "assistant", "content": bot_response})
        # Check if response is too long and handle accordingly
        if len(bot_response) > 2000:
            first_part = bot_response[:2000]
            await temp_message.edit(content=first_part)
            for i in range(2000, len(bot_response), 2000):
                await ctx.send(bot_response[i:i+2000])
        else:
            await temp_message.edit(content=bot_response)
    except Exception as e:
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
