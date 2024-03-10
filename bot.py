__version__ = '2.0'

import os
import discord
from discord.ext import commands
from utils.logger import getLogger, configure_logging
import logging
from utils.config import Config as cm
from web import web
import asyncio
from aiohttp import ClientSession


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
        logger.warning("Invalid logging level set: %s.", level_text)
        logger.warning("Using default logging level: INFO.")
    else:
        logger.info("Logging level: %s", level_text)

    logger.info("Log file: %s", name)
    configure_logging(name, log_level)
    logger.debug("Successfully configured logging.")


        

class YourMom(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=cm("Prefix"), tree_cls=MainTree, description="Main client for anshul's YourMom bot",intents=discord.Intents.all())
    
    async def on_ready(self):
        logger.info("Starting")
        await check()

    def run(self):
        async def runner():
            async with self:
                self._connected = asyncio.Event()
                self.session = ClientSession(loop=self.loop)

                try:
                    await self.start(self.token)
                except discord.PrivilegedIntentsRequired:
                    logger.critical(
                        "Privileged intents are not explicitly granted in the discord developers dashboard."
                    )
                except discord.LoginFailure:
                    logger.critical("Invalid token")
                    raise RuntimeError("Invalid Token")
                except Exception:
                    logger.critical("Fatal exception")
                finally:
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
        bot.run(token=cm("Token"))
    except (discord.ClientException, discord.LoginFailure):
        logger.critical("Invalid token, get a valid one first.")
        raise RuntimeError("Invalid Token")
    
