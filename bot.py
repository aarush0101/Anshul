__version__ = '2.0'

import discord
from discord.ext import commands
from utils.logger import getLogger, configure_logging
import logging
from utils.config import Config as cm

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








