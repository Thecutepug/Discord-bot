import os
import discord
from discord.ext import commands
import random

print("Connecting to Discord...")

intents = discord.Intents.all()
#intents.messages = True
#intents.guilds = True
#intents.dm_messages = True
bot = commands.Bot(command_prefix="/", intents=intents, help_command=commands.DefaultHelpCommand())

#Launch event in console
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

#DM bot command
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

#Do you love me command
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

#Hello Command
@bot.command(name='hello', help='Say hello to the bot')
async def hello(ctx):
    await ctx.send(f'Hello {ctx.author.mention}!')

#Repeat Command
@bot.command(name='repeat', help='Repeat a message')
async def repeat(ctx, *, message):
    await ctx.send(message)

#Help Command
class CustomHelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.help_command = self.CustomHelpCommand()


class CustomHelpCommand(commands.DefaultHelpCommand):
        async def send_bot_help(self, mapping):
            embed = discord.Embed(title="Bot Commands", color=discord.Color.blue())

            for cog, commands in mapping.items():
                if cog:
                    embed.add_field(name=cog.qualified_name, value="\n".join(f"/{command.name} - {command.short_doc}" for command in commands), inline=False)
                else:
                    embed.add_field(name="Other Commands", value="\n".join(f"/{command.name} - {command.short_doc}" for command in commands), inline=False)

            channel = self.get_destination()
            await channel.send(embed=embed)

# Load the custom help command cog
bot.add_cog(CustomHelpCommand(bot))

# Override the default /help command
@bot.command(name='help', help='Display a list of available commands and their descriptions')
async def custom_help_command(ctx):
    bot.help_command.CustomHelpCommand(ctx.bot).send_bot_help(ctx.bot.cogs)
bot.run(os.environ["DISCORD_TOKEN"])
