import discord
from discord.ext import commands


class GuildService:
    discord_client: commands.Bot

    def __init__(self, discord_client: commands.Bot) -> None:
        self.discord_client = discord_client

    def get_members(self, guild_id: int) -> list[discord.Member]:
        guild = self.discord_client.get_guild(guild_id)

        members = []
        for member in guild.members:
            if member.bot == True:
                continue

            members.append(member)

        return members

    def get_online_members(self, guild_id: int) -> list[discord.Member]:
        members = self.get_members(guild_id)

        online_members = []
        for member in members:
            if member.status == discord.Status.online:
                online_members.append(member)

        return online_members
