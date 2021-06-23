import json
import os
import discord
from discord.ext import commands
from discord_slash import SlashCommand
from commands.scripter import ScripterService


def format_exception(e) -> str:
    return f'🔮 astrologers hast discovered their wit: "{e}"'


def read_config():
    with open("config.json", "r") as file:
        return json.load(file)


intents = discord.Intents.default()
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix='/', intents=intents)
slash = SlashCommand(bot, sync_commands=True)

config = read_config()
GUILD_ID = int(config['app']['guildId'])


@slash.slash(name='ping', description='Test', guild_ids=[GUILD_ID])
async def ping(ctx):
    await ctx.send('pong')


@slash.slash(name='scripter', description='Slay a sacrifice!', guild_ids=[GUILD_ID])
async def get_scripter(ctx):
    try:
        restricted_member_ids = config['app']['restrictedMemberIds']
        service = ScripterService(bot)

        member = service.get(GUILD_ID, restricted_member_ids)
        message = ('🔮 Astrologers announced that there is none to choose from 🔮'
                   if member is None
                   else f'📜 Astrologers hast chosen {member.mention}')

        await ctx.send(message)
    except Exception as e:
        await ctx.send(format_exception(e))


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


bot.run(os.environ.get('HTDC_ON_CALL_2_DISCORD_TOKEN'))
