import json
import os
import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option
import coloredlogs
from commands.participants import ParticipantsService
from commands.proclaimer import ProclamationService
from commands.scripter import ScripterService

coloredlogs.install(
    fmt='{"created_at": "%(asctime)s.%(msecs)06dZ", "process": "%(name)s[%(process)d]", "log_level": "%(levelname)s", "message": "%(message)s"}', datefmt='%Y-%m-%dT%H:%M:%S')


def format_exception(e) -> str:
    return f"🔮 Astrolog'rs hast discovered their wit: '{e}'"


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


@slash.slash(name='missing', description="Check who's missing", guild_ids=[GUILD_ID], options=[
    create_option(
        name="voice_channel",
        description="The name of a voice channel to find missing participants",
        option_type=7,
        required=True
    )
])
async def get_missing_participants(ctx, voice_channel: discord.VoiceChannel):
    try:
        restricted_member_ids = config['app']['restrictedMemberIds']
        service = ParticipantsService(bot)

        members = service.get(voice_channel, GUILD_ID, restricted_member_ids)
        if len(members) == 0:
            await ctx.send("Ev'ryone is h're")
            return

        message = f'{members[0].mention}'
        for member in members[1:]:
            message += f', {member.mention}'

        await ctx.send(message)
    except Exception as e:
        await ctx.send(format_exception(e))


@slash.slash(name='proclaim', description='Hear the prediction for the next week', guild_ids=[GUILD_ID])
async def get_scripter(ctx):
    try:
        service = ProclamationService(bot)

        proclamation_correction_coefficient = config['app']['proclamationCorrectionCoefficient']
        proclamation_engineer_ids = config['app']['proclamationEngineerIds']

        proclaimed = service.get(
            proclamation_engineer_ids, proclamation_correction_coefficient)
        next_proclaimed = service.get(
            proclamation_engineer_ids, proclamation_correction_coefficient + 1)

        message = (
            f"🔮 Astrolog'rs has't did declare this week to beest {proclaimed.mention}'s week. {proclaimed.mention} doubles the numb'r of did close bugs 🔮 {next_proclaimed.mention} appears on the h'rizon")

        await ctx.send(message)
    except Exception as e:
        await ctx.send(format_exception(e))


@slash.slash(name='scripter', description='Slay a sacrifice!', guild_ids=[GUILD_ID])
async def get_scripter(ctx):
    try:
        restricted_member_ids = config['app']['restrictedMemberIds']
        service = ScripterService(bot)

        member = service.get(GUILD_ID, restricted_member_ids)
        message = ("🔮 Astrolog'rs did announce yond th're is none to chooseth from 🔮"
                   if member is None
                   else f"📜 Astrolog'rs has't chosen {member.mention}")

        await ctx.send(message)
    except Exception as e:
        await ctx.send(format_exception(e))


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


bot.run(os.environ.get('HTDC_ON_CALL_2_DISCORD_TOKEN'))
