# Help Commands for Bald Bot
# Author: Hu Bowen
# Date: 9/11/22

# Libraries
import discord
from discord import app_commands
from discord.ext import commands

import constants
import balding_functions


# Help Class
class Help(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        """ Initalise cog with given arguments """
        self.bot = bot

    @app_commands.command(name="help", description="Sends all available commands")
    async def help(self, interaction: discord.Interaction) -> None:
        """ Help Command, sends all available functions """
        embed = discord.Embed(
            title="Help", color=balding_functions.random_color())

        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/791588775456800802/792709248349503488/20201224_171052.jpg"
        )
        embed.set_footer(text=f"Requested by: {interaction.user.name}",
                         icon_url=f"{interaction.user.avatar}")

        embed.add_field(name="ping:",
                        value="Returns the latency of the bot.",
                        inline=False)
        embed.add_field(name="time:",
                        value="Gets the time you have spent in this server.",
                        inline=False)
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    """ Setup cog on BaldBot """
    await bot.add_cog(Help(bot), guilds=[discord.Object(id=constants.GUILD_ID)])
