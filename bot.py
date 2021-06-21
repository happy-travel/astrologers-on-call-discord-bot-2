import discord
from discord.ext import commands
from discord_slash import SlashCommand
import json
import os


def read_config():
    with open("config.json", "r") as file:
        return json.load(file)


intents = discord.Intents.default()
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix='/', intents=intents)
slash = SlashCommand(bot, sync_commands=True)

config = read_config()
GUILD_ID = int(config['APP']['GUILD_ID'])


@slash.slash(name='ping', description='Test', guild_ids=[GUILD_ID])
async def ping(ctx):
    await ctx.send('pong')


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


bot.run(os.environ.get('HTDC_ON_CALL_2_DISCORD_TOKEN'))