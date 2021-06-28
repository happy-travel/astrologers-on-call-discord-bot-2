import datetime
import math
import discord
from discord.ext import commands
from api.guilds import GuildService


class ProclamationService:
    _discord_client: commands.Bot

    def __init__(self, discord_client: commands.Bot) -> None:
        self._discord_client = discord_client

    def _get_elapsed_week_number(self) -> int:
        timestamp = datetime.datetime.utcnow().timestamp()
        return math.floor((timestamp / (1000 * 60 * 60 * 24)) / 7)

    def _get_position(self, elapsed_week_number: int, engineer_count: int, correction_coefficient: int) -> int:
        position = (elapsed_week_number %
                    engineer_count) + correction_coefficient

        if (engineer_count <= position):
            position = position - engineer_count

        return position

    def get(self, engineer_ids: list[int], proclamation_correction_coefficient: int) -> discord.User:
        elapsed_week_number = self._get_elapsed_week_number()
        position = self._get_position(elapsed_week_number, len(
            engineer_ids), proclamation_correction_coefficient)

        user_id = engineer_ids[position]
        guild_service = GuildService(self._discord_client)

        return guild_service.get_user(user_id)
