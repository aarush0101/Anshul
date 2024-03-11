__version__ = '2.0d'

import os
import time
import types
import typing
import discord
from discord.ext import commands
from git import Optional
from utils.logger import getLogger, configure_logging
import logging
from utils.config import Config as cm
import dotenv
import asyncio
from aiohttp import ClientSession
from typing import Union

logger = getLogger(__name__)


class YourMom(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=cm("Prefix"), description="Main client for anshul's YourMom bot",intents=discord.Intents.all())
        self.started = False
        self.config = cm
        # self.guild = self.get_guild_(id=int(self.config("Guild_ID")))
        self.token = self.config("Token")
    @property
    def owners(self) -> list:
        """
        Return list of bot owner ID(s)
        """
        return self.config("Owners")
    @property
    def copyright(self) -> str:
        """
        Return the author of this project
        """
        return self.config("Copyright")
    @property
    def logging_(self) -> int:
        """
        Return log channel ID for logging
        """
        return self.config("Log_Channel_ID")
    
    @property
    def gifted_to(self) -> str:
        """
        Returns to whom is this licensed to
        """
        return self.config("Owner_Name")

    @property
    def hosting_method(self) -> str:
        """
        Returns on what is this currently running
        """
        if 'REPLIT_DB_URL' in dotenv.dotenv_values:
            return "REPLIT:("
        import platform
        system = platform.system().lower()
        if system:
            if system.lower() == 'windows':
                if platform.architecture()[0] == '32bit':
                    return "WINDOWS 32 BIT"
                elif platform.architecture()[0] == '64bit':
                    return "WINDOWS 64 BIT"
                else:
                    return "WINDOWS"
            if system.lower() == 'linux':
                return "LINUX"
            if system.lower() == 'darwin':
                return "MAC OS"
            if system.lower() == 'atheos':
                return "ATHE OS"
            if system.lower() == 'riscos':
                return "RISC OS"
            if system.lower() == 'os/2':
                return "OS/2"
            if system.lower() == 'java':
                return "JAVA VIRTUAL MACHINE"
            if system.lower() == 'java freebsd':
                return "JAVA FREEBSD"

        return "Couldn't detect system"
    
    @property
    def cogs_dir(self) -> str:
        """
        Returns the cog directory where commands are located
        """
        root = os.path.join(os.path.dirname(__file__), 'bot.py')
        cogs_dir = os.path.join(root, 'commands')
        return cogs_dir
    
    
    async def load_extension(self) -> None:
        """
        Load the commands into the bot for usage.
        """
        await self.wait_until_ready()
        dir = self.cogs_dir
        
        for cog in dir:
            logger.debug("Loading %s cog..." % (cog,))
            try:
                await self.load_extension(cog)
                logger.debug("Loaded cog: %s" % (cog,))
            except Exception:
                logger.error("Unable to load cog: %s" % (cog,))
        logger.info("Successfully loaded all the commands")

    @property
    def get_guild_icon(self, guild: typing.Optional[discord.Guild], *, size: typing.Optional[int] = None) -> str:
        """
        Returns main guild icon
        """
        if guild is None:
            guild = self.guild
        if guild.icon is None:
            return "https://cdn.discordapp.com/embed/avatars/0.png"
        if size is None:
            return guild.icon.url
        return guild.icon.with_size(size).url

    async def get_owners(self) -> str:
        """
        Returns str of owners the bot currently has listed in its config
        """
        ids_ = self.owners
        owners = ", ".join(
            getattr(self.get_user_(owner_id), "name", str(owner_id)) for owner_id in ids_
        )
        return owners
    
    async def get_user_(self, id: int) -> discord.User:
        """
        Similar to get_user of discord module but this tries getting the user from the cache and falls back to making
        an API call if they're not found in the cache.
        """
        return await self.get_user(id) or await self.fetch_user(id)
    
    async def get_channel_(self, id: int) -> Optional[Union[discord.TextChannel, discord.ForumChannel, discord.VoiceChannel, discord.StageChannel, discord.CategoryChannel, discord.DMChannel, discord.channel.VocalGuildChannel]]:
        """
        Similar to get_channel of discord module but this tries to get the channel from the cache and if not found, try to get from API calls.
        """
        return await self.get_channel(id) or await self.fetch_channel(id)
        
    async def get_guild_(self, id: int) -> discord.Guild:
        """
        Similar to get_guild of discord module but this one tries to get the guild object even if its not found in cache
        """
        return await self.get_guild(id) or await self.fetch_guild(id)
    
    async def checker(self) -> bool:
        """
        Checks if everything is perfect before starting, this is called in on_ready event.
        """
        properties = [
            self.owners,
            self.copyright,
            self.logging_,
            self.gifted_to,
            self.hosting_method,
            self.cogs_dir,
            self.get_guild_icon(self.guild),
            self.start_time,
            self.version
        ]
        if not all(properties):
            logger.debug(f"Some of the properties is None: {', '.join(str(property_) for property_ in properties if not property_) or True}")
            return False

        # Check if all other properties that require async calls are valid
        async_properties = [
            await self.servers(),
            await self.retrieve_emoji(),
            await self.get_owners()
        ]
        if not all(async_properties):
            logger.debug(f"Some of the async properties are false: {', '.join(str(property_) for property_ in async_properties if not property_) or True}")
            return False

        return True
    
    @property
    def invite(self) -> str:
        """
        Returns the bot invite link. Explicitly generated through discord.utils
        """
        permissions = discord.PermissionOverwrite(
            administrator=True
        )
        invite_link = discord.utils.oauth_url(client_id=self.user.id, permissions=permissions)
        return invite_link
    
    async def guild_invite(self) -> discord.Invite:
        """
        Get the invite for first channel in the main guild.
        """
        guild_id = self.config("Guild_ID")
        guild = await self.get_guild_(int(guild_id))
        for channel in guild.channels:
            if isinstance(channel, discord.TextChannel): 
                invite = await channel.create_invite(max_age=0, max_uses=0, temporary=False)
                break  
        else:
            return None  
    
        return invite 
    
    @property
    async def uptime_st(self) -> None:
        """
        Once called, it sets uptime. Subtract it when the appropriate value is required.
        """
        self.start_time = time.time()

    @property
    def uptime(self) -> str:
        """
        Should return the time string which was inherited from uptime_st?
        """
        now = discord.utils.utcnow()
        delta = now - self.start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        fmt = "{h}h {m}m {s}s"
        if days:
            fmt = "{d}d " + fmt

        return fmt.format(d=days, h=hours, m=minutes, s=seconds)
    
    @property
    def version(self) -> str:
        """
        Returns the current version of the software
        """
        return __version__
    

    async def servers(self) -> int:
        """
        Returns the count of servers the bot is in
        """
        await self.wait_until_ready()
        servers = len(self.guilds)
        return servers
    

    async def retrieve_emoji(self) -> bool:
        """
        Returns whether the emojis in self.config are accessible by the bot or not
        """
        self.success_emoji_id = self.config("Success_Emoji")
        self.error_emoji_id = self.config("Error_Emoji")

        try:
            self.success_emoji = self.get_emoji(self.success_emoji_id)
            self.error_emoji = self.get_emoji(self.error_emoji_id)
            return True
        except (Exception, discord.NotFound):
            return False

    @property
    def activity(self) -> dict:
        """
        Return a dict containing all the information about the activity
        """
        msg = self.config("Activity_Message")
        type_ = self.config("Activity_Type")
        state = self.config("Activity_State")
        kwargs = {
            "message": msg,
            "type": type_,
            "state": state
        }
        return kwargs
    
    async def set_activity(self) -> str:
        if self.config("Activity") != True:
           return "activity is disabled"
        try:
            k = self.activity
            act = discord.Activity(type=k.get("type"), name=k.get("msg"))
            await self.change_presence(activity=act, status=k.get("state"))
            return "success"
        except Exception as e:
            return "error: %s" % (e,)
           


    async def on_ready(self) -> None:
        """
        Bot startup, sets the bot's uptime
        """

        # wait for checker function to check all the stuff and populate cache
        checked = await self.checker()
        if checked:
            logger.line()
            logger.info("                         _           _ ")
            logger.info("         /\             | |         | |")
            logger.info("  ___   /  \   _ __  ___| |__  _   _| |")
            logger.info(" / _ \ / /\ \ | '_ \/ __| '_ \| | | | |")
            logger.info("| (_) / ____ \| | | \__ \ | | | |_| | |")
            logger.info(" \___/_/    \_\_| |_|___/_| |_|\__,_|_|")
            logger.line()
            logger.info(f"Version: {self.version}")
            if "d" in self.version:
                logger.info("Stable Version: False")
            logger.info("Stable Version: True")
            logger.warning("You are using a development version, it may contain some errors and bugs")
            logger.info(f"Authors: {self.copyright}")
            logger.info(f"Licensed to: {self.gifted_to}")
            logger.line()
            logger.info(f"Guild: {self.guild.name}")
            logger.info(f"Logging channel: {self.get_channel_(id=int(self.logging_))}")
            logger.info("Currently in %s guilds" % (await self.servers(),))

            act = self.set_activity()
            if act.lower() in ["activity is disabled"]:
                logger.warning("The activity is disabled in config, skipping...")
            elif act.lower() in ["success"]:
                logger.info("Successfully set activity")
            elif act.lower() in ["error"]:
                logger.warning("Failed to set activity. Please contact your administrator")
            else:
                logger.warning(f"Unable to load activity: {act}")
                raise RuntimeError(act)
            logger.info("Loading commands...")
            self.load_extension()

            logger.line()
            logger.info("Successfully logged in")
            self.started = True
        else:
            logger.info("Some of the properties are false as per checked by checker function, please check `temp/log.log` for the properties that were invalid.")
            raise RuntimeError("Invalid properties")
       

    def run(self):

        async def runner():
            async with self:
                self.session = ClientSession(loop=self.loop)
                try:
                    await self.start(self.token)
                except discord.PrivilegedIntentsRequired:
                    logger.critical(
                        "Privileged intents are not explicitly granted in the discord developers dashboard."
                    )
                except discord.LoginFailure:
                    logger.critical("Invalid token")
                except Exception:
                    logger.critical("Fatal exception", exc_info=True)
                finally:
                    if self.session:
                        await self.session.close()
                    if not self.is_closed():
                        await self.close()

        async def _cancel_tasks():
            async with self:
                task_retriever = asyncio.all_tasks
                loop = self.loop
                tasks = {t for t in task_retriever() if not t.done() and t.get_coro() != cancel_tasks_coro}

                if not tasks:
                    return

                logger.info("Cleaning up after %d tasks.", len(tasks))
                for task in tasks:
                    task.cancel()

                await asyncio.gather(*tasks, return_exceptions=True)
                logger.info("All tasks finished cancelling.")

                for task in tasks:
                    try:
                        if task.exception() is not None:
                            loop.call_exception_handler(
                                {
                                    "message": "Unhandled exception during Client.run shutdown.",
                                    "exception": task.exception(),
                                    "task": task,
                                }
                            )
                    except (asyncio.InvalidStateError, asyncio.CancelledError):
                        pass
        try:
            asyncio.run(runner(), debug=bool(os.getenv("DEBUG_ASYNCIO")))
        except (KeyboardInterrupt, SystemExit):
            logger.info("Received signal to terminate bot and event loop.")
        finally:
            logger.info("Cleaning up tasks.")

            try:
                cancel_tasks_coro = _cancel_tasks()
                asyncio.run(cancel_tasks_coro)
            finally:
                logger.info("Closing the event loop.")






def main():
    try:
        bot = YourMom()
        bot.remove_command('help')
        bot.run()
    except (discord.ClientException, discord.LoginFailure):
        logger.critical("Invalid token, get a valid one first.")
        raise RuntimeError("Invalid Token")
    
main()