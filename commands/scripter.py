from typing import Optional
import discord
import random
from api.guilds import GuildService
from discord.ext import commands


class ScripterService:
    discord_client: commands.Bot

    def __init__(self, discord_client: commands.Bot) -> None:
        self.discord_client = discord_client

    def get(self, guild_id: int, forbidden_member_ids: Optional[list[int]] = None) -> Optional[discord.Member]:
        guild_service = GuildService(self.discord_client)
        members = guild_service.get_online_members(guild_id)

        if forbidden_member_ids is not None:
            members = [x for x in members if x not in forbidden_member_ids]

        member_count = len(members)
        if member_count == 0:
            return None

        position = random.randint(0, member_count - 1)
        return members[position]
