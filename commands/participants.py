import discord
from discord.ext import commands
from api.guilds import GuildService

class ParticipantsService:
    _discord_client: commands.Bot

    def __init__(self, discord_client: commands.Bot) -> None:
        self._discord_client = discord_client

    def get(self, voice_channel: discord.VoiceChannel, guild_id: int, restricted_member_ids: list [int] = []) -> list[discord.Member]:
        guild_service = GuildService(self._discord_client)
        members = guild_service.get_members(guild_id)

        missing_participants = [x for x in members if x not in voice_channel.members]
        return [x for x in missing_participants if x.id not in restricted_member_ids]