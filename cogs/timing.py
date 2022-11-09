# Timing Related Commands for Bald Bot
# Author: Hu Bowen
# Date: 9/11/22

# Libraries
import discord
from discord import app_commands
from discord.ext import commands

import datetime
import constants


# Timing Class
class Timing(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        """  Initialise cog with given arguments """
        self.bot = bot

    @app_commands.command(name="time", description="Gets how long you spent in this server in days.")
    async def time(self, interaction: discord.Interaction, member: discord.Member = None) -> None:
        """ Time command, gets time of self or mentioned user spent in server in days """

        # If no member argument was supplied, set member as the user who called the command
        if member is None:
            member = interaction.user
        
        join_date = member.joined_at

        days = await self.getDays(join_date)
        await interaction.response.send_message(f"{member.mention}'s days in BaldSMP: **{days}**")

    async def getDays(self, join_date: discord.Member.joined_at) -> int:
        """ Gets the number of days between the current date and the argument """
        tz_info = join_date.tzinfo  # Get timezone info so that datetime does not throw an error when subtracting
        duration = datetime.datetime.now(tz_info) - join_date

        hours, remainder = divmod(int(duration.total_seconds()), 3600)
        days, hours = divmod(hours, 24)

        return days


async def setup(bot: commands.Bot) -> None:
    """ Setup cog on BaldBot """
    await bot.add_cog(Timing(bot), guilds=[discord.Object(id=constants.GUILD_ID)])