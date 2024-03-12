"""
PLEASE CHECK GUIDE BEFORE ADDING ANYTHING HERE. ITS NAMED `embeds_guide.json` AND IS IN CORE FOLDER. DON'T BREAK THIS BY TRYING TO BECOME PRO
"""

__version__ = '2.1d'

import discord
from utils.config import Config
from bot import YourMom


prefix = Config("Prefix").value
color = Config("Success_Color").value
icon_url = Config("Icon_URL").value

EMBED1 = discord.Embed(
    title='Tag',
    description=f'```diff\n- [] = optional argument\n- <> = required argument\n- Do NOT type these when using commands!```\n>>> Get help through a tag. It may contain some useful information.\nAliases\nt | info\nUsage\n{prefix}tag <name>',
    color=color
)
EMBED1.set_author(name='Utility', icon_url=icon_url, url=YourMom.guild_invite_)
EMBED2 = discord.Embed(
    title='Tags',
    description=f'```diff\n- [] = optional argument\n- <> = required argument\n- Do NOT type these when using commands!```\n>>> Add a tag to the bot config.\nAliases\nta | tadd\nUsage\n{prefix}tags <tag_name> *, <content>',
    color=color
)
EMBED2.set_author(name='Admin', icon_url=icon_url, url=YourMom.guild_invite_)
EMBED3 = discord.Embed(
    title='Ban',
    description=f'```diff\n- [] = optional argument\n- <> = required argument\n- Do NOT type these when using commands!```\n>>> Ban a user from the guild as a punishment!\nAliases\nb | get-out\nUsage\n{prefix}ban <user> *, [reason]',
    color=color
)
EMBED3.set_author(name='Admin', icon_url=icon_url, url=YourMom.guild_invite_)
EMBED4 = discord.Embed(
    title='Help -> Current',
    description=f'```diff\n- [] = optional argument\n- <> = required argument\n- Do NOT type these when using commands!```\n>>> Get some help. Do not feel lost in the cosmos!\nAliases\nh | hp\nUsage\n{prefix}help',
    color=color 
)
EMBED4.set_author(name='Normal Usage', icon_url=icon_url, url=YourMom.guild_invite_)
EMBED5 = discord.Embed(
    title='debug',
    description=f'```diff\n- [] = optional argument\n- <> = required argument\n- Do NOT type these when using commands!```\n>>> Get the latest console logs of the bot uploaded to haste-bin.\nAliases\ndbg | d | dg\nUsage\n{prefix}debug',
    color=color
)
EMBED5.set_author(name='Utility', icon_url=icon_url, url=YourMom.guild_invite_)
EMBED6 = discord.Embed(
    title='support',
    description=f'```diff\n- [] = optional argument\n- <> = required argument\n- Do NOT type these when using commands!```\n>>> {prefix}help could not solve your problems? Welp, join our support server then to get help.\nAliases\ns | sp\nUsage\n{prefix}support',
    color=color
)
EMBED6.set_author(name='Utility', icon_url=icon_url, url=YourMom.guild_invite_)
EMBED7 = discord.Embed(
    title='mute',
    description=f'```diff\n- [] = optional argument\n- <> = required argument\n- Do NOT type these when using commands!```\n>>> Timeout a person\nAliases\nti | to\nUsage\n{prefix}'
)
