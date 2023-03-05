# Manages a locally hosted minecraft server
# Author: Hu Bowen
# Date: 2/3/23

# Libraries
import hashlib
import os
import discord
from discord import app_commands
from discord.ext import commands

import json
import typing
import requests
import shlex
import subprocess

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
        
        # Retrieve UUID of player if not provided
        if uuid is None:
            if not self.is_online_mode():
                # Get UUID from Mojang API
                url = "https://api.mojang.com/users/profiles/minecraft/" + player
                res = requests.get(url)
                if res.status_code == 204:
                    return await interaction.response.send_message(":x: Player does not exist")
                uuid = res.json()["id"]
            else:
                # Generate UUID from player name
                # Source: https://gist.github.com/Nikdoge/474f74688b52865bf8d682a97fd4f2fe#file-minecraft_offline_uuid-py-L19
                string = "OfflinePlayer:" + player
                hash = hashlib.md5(string.encode('utf-8')).digest()
                byte_array = [byte for byte in hash]
                #set the version to 3 -> Name based md5 hash
                byte_array[6] = hash[6] & 0x0f | 0x30
                #IETF variant
                byte_array[8] = hash[8] & 0x3f | 0x80

                hash_modified = bytes(byte_array)
                uuid = hash_modified.hex()

            # Convert UUID to correct format
            uuid = uuid[:8] + "-" + uuid[8:12] + "-" + uuid[12:16] + "-" + uuid[16:20] + "-" + uuid[20:]
        
        # Add player to whitelist.json file
        whitelisted_data.append({"name": player, "uuid": uuid})
        with open("whitelist.json", "w") as f:
            json.dump(whitelisted_data, f, indent=4)

        # Send whitelist reload command to server
        os.system("screen -S minecraft -p 0 -X stuff \"whitelist reload^M\"")

        # Create response embed
        embed = discord.Embed(title="Whitelisted Player", color=0x1FFF35 )
        embed.add_field(name="Player", value=player, inline=False)
        embed.add_field(name="UUID", value=uuid, inline=False)

        await interaction.response.send_message(f"Whitelisted `{player}`\nUUID: `{uuid}`")

    # Remove player from whitelist
    @app_commands.command(name="unwhitelist", description="Removes player from whitelist")
    async def unwhitelist(self, interaction: discord.Interaction, player: str) -> None:
        """Removes player from whitelist"""

        # Open whitelist.json file and load usernames
        with open("whitelist.json", "r") as f:
            whitelisted_data = json.load(f)
            usernames = [user["name"] for user in whitelisted_data]

        # Check if player is already whitelisted
        if player not in usernames:
            await interaction.response.send_message(":x: Player is not whitelisted")
            return 
        
        # Remove player from whitelist.json file
        whitelisted_data = [user for user in whitelisted_data if user["name"] != player]
        with open("whitelist.json", "w") as f:
            json.dump(whitelisted_data, f, indent=4)

        # Send whitelist reload command to server
        os.system("screen -S minecraft -p 0 -X stuff \"whitelist reload^M\"")

        await interaction.response.send_message(f"Removed `{player}` from whitelist")

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

        if full_stats["num_players"] > 0:
            embed.add_field(name="Players", value="\n".join(full_stats["players"]), inline=False)

        await interaction.response.send_message(embed=embed)

    # Get IP of server
    @app_commands.command(name="server_ip", description="Gets the IP of the server")
    async def server_ip(self, interaction: discord.Interaction) -> None:
        """Gets the IP of the server"""

        # Check if server is running
        if os.system("screen -ls | grep -q minecraft") != 0:
            return await interaction.response.send_message(":x: Server is not running!")

        # Read server.log
        with open("server.log", "r") as f:
            lines = f.readlines()

            # Extract IP from 7th line
            try:
                backup_ip = lines[6].split(" ")[-1].split("//")[-1]
            except:
                await interaction.response.send_message(":x: Server is starting / not running!")
                return

        await interaction.response.send_message("IP: `mc.hubowen.dev`\nBackup IP: `" + backup_ip + "`")

    # Start server
    @app_commands.command(name="start_server", description="Starts the server")
    async def start_server(self, interaction: discord.Interaction) -> None:
        # Check if server screen is already running
        if os.system("screen -ls | grep -q minecraft") == 0:
            return await interaction.response.send_message(":x: Server is already running!")
        
        # Start server
        command = "screen -dmS minecraft bash -c \"cd ~; ./start.sh > ~/mc_server/server.log\""
        subprocess.Popen(shlex.split(command), start_new_session=True)

        await interaction.response.send_message("IMPORTANT NOTE: Please run `/server_ip` after the server starts, as the original IP will be unavailable till I change it.\n:white_check_mark: Server is being started!")

    # Helper function to check if server is in online mode
    def is_online_mode(self) -> bool:
        """Checks if server is in online mode"""
        with open("server.properties", "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("online-mode="):
                    return line.split("=")[-1].strip() == "true"
        return None


async def setup(bot: commands.Bot) -> None:
    """Setup cog on BaldBot"""
    await bot.add_cog(Minecraft(bot), guilds=[discord.Object(id=constants.GUILD_ID)])