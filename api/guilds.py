import discord
from discord.ext import commands


class GuildService:
    _discord_client: commands.Bot

    def __init__(self, discord_client: commands.Bot) -> None:
        self._discord_client = discord_client

    def get_members(self, guild_id: int) -> list[discord.Member]:
        guild = self._discord_client.get_guild(guild_id)
        return [x for x in guild.members if x.bot is not True]

    def get_online_members(self, guild_id: int) -> list[discord.Member]:
        members = self.get_members(guild_id)
        return [x for x in members if x.status is discord.Status.online]
