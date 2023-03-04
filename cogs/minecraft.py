# Manages a locally hosted minecraft server
# Author: Hu Bowen
# Date: 2/3/23

# Libraries
import discord
from discord import app_commands
from discord.ext import commands

import json
import typing
import requests

from mcipc.query import Client

import constants
from balding_functions import random_color

# Minecraft Class
class Minecraft(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        """Initialise cog with given arguments"""
        self.bot = bot

    @app_commands.command(name="whitelist", description="Adds player to whitelist if they are not already on it")
    async def whitelist(self, interaction: discord.Interaction, player: str, uuid: typing.Optional[str]) -> None:
        """Adds player to whitelist if they are not already on it"""

        # Open whitelist.json file and load usernames
        with open("whitelist.json", "r") as f:
            whitelisted_data = json.load(f)
            usernames = [user["name"] for user in whitelisted_data]

        # Check if player is already whitelisted
        if player in usernames:
            return await interaction.response.send_message(":x: Player is already whitelisted")
        
        # Retrieve UUID of player from Mojang API
        if uuid is None:
            url = "https://api.mojang.com/users/profiles/minecraft/" + player
            res = requests.get(url)
            if res.status_code == 204:
                return await interaction.response.send_message(":x: Player does not exist")
            uuid = res.json()["id"]
        
        # Add player to whitelist.json file
        whitelisted_data.append({"name": player, "uuid": uuid})

        # Create response embed
        embed = discord.Embed(title="Whitelisted Player", color=0x1FFF35 )
        embed.add_field(name="Player", value=player, inline=False)
        embed.add_field(name="UUID", value=uuid, inline=False)

        await interaction.response.send_message(f"Whitelisted `{player}`\nUUID: `{uuid}`")

    @app_commands.command(name="server_stats", description="Gets stats of the minecraft server")
    async def server_stats(self, interaction: discord.Interaction) -> None:
        """Gets the stats of the server"""

        # Get stats from server
        try:
            with Client("127.0.0.1", 25565, timeout=5) as client:
                full_stats = dict(client.stats(full=True))
        except:
            await interaction.response.send_message(":x: Server is not running")
            return
        
        # Create embed
        embed = discord.Embed(title="Server Stats", color=random_color())
        embed.add_field(name="MOTD", value=full_stats["host_name"], inline=False)
        embed.add_field(name="Game Version", value=full_stats["version"], inline=False)
        embed.add_field(name="Players", value=str(full_stats["num_players"]) + "/" + str(full_stats["max_players"]), inline=False)
        embed.add_field(name="Player Names", value="\n".join(full_stats["players"]), inline=False)

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    """Setup cog on BaldBot"""
    await bot.add_cog(Minecraft(bot), guilds=[discord.Object(id=constants.GUILD_ID)])