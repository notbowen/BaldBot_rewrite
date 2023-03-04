# Miscellaneous Commands for Bald Bot
# Author: Hu Bowen
# Date: 9/11/22

# Libraries
import discord
from discord import app_commands
from discord.ext import commands

import constants
import random


# Miscellaneous Class
class Misc(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        """ Initialise cog with given arguments """
        self.bot = bot

    @app_commands.command(name="ping", description="Shows the bot latency")
    async def ping(self, interaction: discord.Interaction) -> None:
        """ Ping command, Returns the latency of the bot """
        await interaction.response.send_message(f"Pong! Latency: **{round(self.bot.latency * 1000)}**ms")

    @app_commands.command(name="acceptance_rate", description="Shows the chance of one getting women & getting married")
    async def acceptance_rate(self, interaction: discord.Interaction, member: discord.Member = None) -> None:
        """ Command to get the rate of women """
        dating_rate = random.randint(1, 100)
        marriage_rate = random.randint(1, 100)

        if member == None:
            member = interaction.user
        
        await interaction.response.send_message(f"{member.mention}'s:\nDating Rate: `{dating_rate}%`\nMarriage Rate: `{marriage_rate}%`")


async def setup(bot: commands.Bot) -> None:
    """ Setup cog on BaldBot """
    await bot.add_cog(Misc(bot), guilds=[discord.Object(id=constants.GUILD_ID)])
