# BaldBot Rewrite for the BaldSMP
# Author: Hu Bowen
# Date: 9/11/22

# Libraries
import asyncio
import os
import random
import time
import json

import discord
from discord.ext import commands
from discord import app_commands

import logger
import constants


# Bad word class
class BadWord:
    def __init__(self, name, wordList, responses):
        self.name = name
        self.wordList = wordList
        self.responses = responses


# Bad word lists
bad_words = [
    BadWord("N word", [
        "neger", "negro", "neeger", "nigger", "nigga", "黑鬼", "hei gui"
    ], [
        "Orh hor say N word I tell mummy",
        "Orh hor say N word u naughty naughty u teasing me",
        "Nigger, a contemptuous term for a black or dark-skinned person. Nigger is an infamous word in current English, so much so that when people are called upon to discuss it, they more often than not refer to it euphemistically as \"the N-word.\" In senses 1 and 2, the word ranks as almost certainly the most offensive and inflammatory racial slur in English, a term expressive of hatred and bigotry. Sense 3 is also now rarely used and is often considered offensive. The word's self-referential uses by and among Black people are not always intended or taken as offensive (although many object to those uses as well), but its use by a person who is not Black to refer to a Black person can only be regarded as a deliberate expression of contemptuous racism. First known use of the word \"Nigger\" you may ask. The answer? 1755",
        "Black people might sometimes address other of their black friends, \"My Nigger!\"",
        "This word is often derogatory and Whites are banned from using that word. The reason for this is that the history of the word \"Nigger\" dates back to when Blacks were still used as slaves and people would not treat them like normal human beings and call them \"Negro\".",
        "In the 1800s, there were human zoos showcasing black people (Niggers!)",
        "NIGGGAAAAAAAAAAAAAAAAAAAAAA"
    ]),
    BadWord("F word", ["fuck", "fucking", "fucker"], [
        "Orh hor say F word I tell mummy",
        "Orh hor say F word u naughty naughty u teasing me",
    ]),
    BadWord("Chink word", ["chink", "cheenk", "ching"], [
        "Chink, a English-language ethnic slur usually referring to a person of Chinese descent.",
        "A chink is usually defined from the person's facial appearance, such as having small eyes. (Aidan)",
        'The word that u have just used (Chink), is thought to have originated from ancient China as the Qing dynasty is sometimes pronounced as "Chink" in America',
        'When I came to the U.S. as an adopted child from Vietnam (Bill). I was playing on a swing set  when a kid my age walked out of his house and came up to me and said, "Hey chink, get off the swing I want to use it."  I didn\'t know what the word meant and went home and looked it up in the dictionary. [Definition of CHINK] : a narrow beam of light shining through a hole of a wall or building. I laughed so hard until my good friend Tyron Jamal Jones James Johnson explained to me that it means the same as the N word people applied to him. We both went back the next day and kicked the living racist "chink" out of his loathsome armor. "Words have many meanings, but hate has only one intention, to cut at a person\'s self worth so the user of that word can feel a false sense of worth."',
    ]),
    BadWord("Pinoy word", ["pinoy"], [
        "Pinoy more like penis (kidding)",
        "Pinoy, a person of Filipino origin or descent used with sometimes no negative connotations unlike Nigger or Chink. Pinoy is usually used referring to a Toxic Valorant Player who speaks in noodle language that baits the entire team and screams at them for not entrying, what's worse is that he uses a fork to eat mac n cheese on a plate!",
        "OI PINOYS STOP YELLING AND PLAYING VALORANT LAH U NO LIFER EAT ASS NOODLE LANGUAGE SPEAKING ASS, jk please dont sue me"
    ]),
    BadWord("Fat word",
            ["royce", "fat", "obese", "chunky", "thorston", "kamal"], [
                "little fat fuck", "royce kinda gay", "i love physics",
                "asian leaksss", "omg kamal yacob hehehehehehehor",
                "i hate tryhards LAZY EYE"
            ]),
    BadWord("Tryhard", ["tryhard", "aidan", "bill", "min qi", "minqi", "4a1"],
            [
                "eww tryhard go and study medicine lah",
                "tryhard.exe",
            ]),
    BadWord("Liverpool", ["lfc", "liverpool", "scouse", "scouser"], [
        "allez allez allez", "premier league champions 2021/22",
        "corner taken quickly ORIGIII", "mo salad"
    ])
]


# Define bot with required params
class BaldBot(commands.Bot):
    def __init__(self) -> None:
        """ Initialises BaldBot with required arguments """
        super().__init__(
            command_prefix="b",
            intents=discord.Intents.all(),
            application_id=constants.APPLICATION_ID
        ) 

    async def setup_hook(self) -> None:
        """ Load the cogs """
        for file in os.listdir("./cogs"):
            if not file.endswith(".py"): continue  # Ignore non-pythonic files
            await self.load_extension(f"cogs.{file[:-3]}")
        await bot.tree.sync(guild=discord.Object(id=constants.GUILD_ID))

    async def on_ready(self):
        """ The bot has been successfully setup """
        logger.plus("Bot is ready.")

    async def on_member_join(self, member: discord.Member) -> None:
        """ Send welcome message to newcomer and give the Bald role """
        channel = bot.get_channel(constants.WELCOME_CHANNEL_ID)
        await channel.send("Welcome to the BaldSMP, %s" % member.mention)

        role = discord.utils.get(member.guild.roles, name="Bald")
        await member.add_roles(role)
        
    async def on_message(self, message: discord.Message) -> None:
        """ Checks for bad words before processing the command """
        # TODO: Clean this code?
        if message.author.bot:
            return

        with open("word_count.json", "r") as f:
            data = json.load(f)
            f.close()

        msg = message.content.lower()
        for swear in bad_words:
            for bad_word in swear.wordList:
                if bad_word in msg:
                    try:
                        data[swear.name] += 1
                    except KeyError:
                        data[swear.name] = 1

                    await message.channel.send(random.choice(swear.responses))
                    await message.channel.send(swear.name + " count: " + str(data[swear.name]))

        with open("word_count.json", "w") as f:
            json.dump(data, f, indent=4)
            f.close()

        await bot.process_commands(message)


# Init and run bot
bot = BaldBot()
token = os.getenv("BALD_BOT_TOKEN")
bot.run(token)