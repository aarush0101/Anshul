__version__ = '2.0'

import os
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

def _configure_logging(name):
    level_text = "INFO"
    logging_levels = {
        "CRITICAL": logging.CRITICAL,
        "ERROR": logging.ERROR,
        "WARNING": logging.WARNING,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
    }

    logger.line()
    log_level = logging_levels.get(level_text)
    
    if log_level is None:
        log_level = logging.INFO
        logger.warning("Invalid logging level set: %s." % (level_text,))
        logger.warning("Using default logging level: INFO.")
    else:
        logger.info("Logging level: %s" % (level_text,))

    logger.info("Log file: %s" % (name,))
    configure_logging(name, log_level)
    logger.debug("Successfully configured logging.")


        

class YourMom(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=cm("Prefix"), description="Main client for anshul's YourMom bot",intents=discord.Intents.all())
        self.started = False
        self.config = cm

    @property
    def owners(self):
        """
        Return list of bot owner ID(s)
        """
        return self.config("Owners")
    @property
    def copyright(self):
        """
        Return the author of this project
        """
        return self.config("Copyright")
    @property
    def logging_(self) -> in:
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
            if cog in self.loaded_cog:
                continue
            logger.debug("Loading %s cog..." % (dir,))
            try:
                await self.load_extension(dir)
                logger.debug("Loaded cog: %s" % (dir,))
            except Exception:
                logger.error("Unable to load cog: %s" % (dir,))
        logger.debug("dbg")

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
        
    async def checker(self) -> bool:
        """
        Checks if everything is perfect before starting, this is called in on_ready event.
        """
        pass
        # TODO: MAKE IT RN
    
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
    
    @property
    def guild_invite(self):





    async def on_ready(self):
        logger.info("Starting")
        # await check()

    def run(self):
        async def runner():
            async with self:
                self.session = ClientSession(loop=self.loop)

                try:
                    await self.start(self.token)
                    
                except discord.PrivilegedIntentsRequired:
                    logger.critical("Privileged intents are not explicitly granted in the discord developers dashboard.")

                except discord.LoginFailure:
                    logger.critical("Invalid token")

                except Exception as e:
                    logger.critical("Fatal exception\n%s" % (e,))
                finally:
                    if not self.is_closed():
                        await self.close()
        async def _cancel_tasks():
            async with self:
                task_retriever = asyncio.all_tasks
                loop = self.loop
                tasks = {t for t in task_retriever() if not t.done() and t.get_coro() != cancel_tasks}

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
                                    "message": "Unhandled exception during shutdown.",
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
                cancel_tasks = _cancel_tasks()
                asyncio.run(cancel_tasks)
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
    
