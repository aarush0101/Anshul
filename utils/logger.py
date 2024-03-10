import json
import asyncio
import logging
from logging.handlers import RotatingFileHandler
import os
from colorama import Fore, Style
import re
import sys
from typing import Optional, Dict
from logging import Handler, StreamHandler, FileHandler

# Custom Logger class with color-coded log levels
class Logger(logging.Logger):
    @staticmethod
    def _debug_(*msgs):
        return f'{Fore.CYAN}{" ".join(msgs)}{Style.RESET_ALL}'

    @staticmethod
    def _info_(*msgs):
        return f'{Fore.GREEN}{" ".join(msgs)}{Style.RESET_ALL}'

    @staticmethod
    def _error_(*msgs):
        return f'{Fore.RED}{" ".join(msgs)}{Style.RESET_ALL}'

    # Override log methods to use color-coded messages
    def debug(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.DEBUG):
            self._log(logging.DEBUG, self._debug_(msg), args, **kwargs)

    def info(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.INFO):
            self._log(logging.INFO, self._info_(msg), args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.WARNING):
            self._log(logging.WARNING, self._error_(msg), args, **kwargs)

    def error(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.ERROR):
            self._log(logging.ERROR, self._error_(msg), args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.CRITICAL):
            self._log(logging.CRITICAL, self._error_(msg), args, **kwargs)

    # Add a line separator to the log
    def line(self, level="info"):
        if level == "info":
            level = logging.INFO
        elif level == "debug":
            level = logging.DEBUG
        else:
            level = logging.INFO
        if self.isEnabledFor(level):
            self._log(
                level,
                Fore.BLACK + Style.BRIGHT + "-------------------------" + Style.RESET_ALL,
                [],
            )

# Custom JSON Formatter for log records
class JsonFormatter(logging.Formatter):
    """
    Formatter that outputs JSON strings after parsing the LogRecord.
    """
    def __init__(
        self,
        fmt_dict: Optional[Dict[str, str]] = None,
        time_format: str = "%Y-%m-%dT%H:%M:%S",
        msec_format: str = "%s.%03dZ",
    ):
        self.fmt_dict: Dict[str, str] = fmt_dict if fmt_dict is not None else {"message": "message"}
        self.default_time_format: str = time_format
        self.default_msec_format: str = msec_format
        self.datefmt: Optional[str] = None

    def usesTime(self) -> bool:
        return "asctime" in self.fmt_dict.values()

    def formatMessage(self, record) -> Dict[str, str]:
        return {fmt_key: record.__dict__[fmt_val] for fmt_key, fmt_val in self.fmt_dict.items()}

    def format(self, record) -> str:
        record.message = record.getMessage()

        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)

        message_dict = self.formatMessage(record)

        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)

        if record.exc_text:
            message_dict["exc_info"] = record.exc_text

        if record.stack_info:
            message_dict["stack_info"] = self.formatStack(record.stack_info)

        return json.dumps(message_dict, default=str)

# Custom Formatter to remove ANSI escape codes from log messages
class FileFormatter(logging.Formatter):
    ansi_escape = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")

    def format(self, record):
        record.msg = self.ansi_escape.sub("", record.msg)
        return super().format(record)

# Set up log formatters
log_stream_formatter = logging.Formatter("%(asctime)s %(name)s[%(lineno)d] - %(levelname)s: %(message)s", datefmt="%m/%d/%y %H:%M:%S")
log_file_formatter = FileFormatter("%(asctime)s %(name)s[%(lineno)d] - %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
json_formatter = JsonFormatter(
    {
        "level": "levelname",
        "message": "message",
        "loggerName": "name",
        "processName": "processName",
        "processID": "process",
        "threadName": "threadName",
        "threadID": "thread",
        "timestamp": "asctime",
    }
)

# Set up custom logger class
logging.setLoggerClass(Logger)
log_level = logging.INFO
loggers = set()

# Set up file formatter for debugging
formatter_debug = FileFormatter("%(asctime)s %(name)s[%(lineno)d] - %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

# Function to remove ANSI escape codes from text


# Set up stream handler for console logging
ch = logging.StreamHandler(stream=sys.stdout)
ch.setLevel(log_level)
formatter = logging.Formatter("%(asctime)s %(name)s[%(lineno)d] - %(levelname)s: %(message)s", datefmt="%m/%d/%y %H:%M:%S")
log_stream_formatter = logging.Formatter("%(asctime)s %(name)s[%(lineno)d] - %(levelname)s: %(message)s", datefmt="%m/%d/%y %H:%M:%S")
log_file_formatter = FileFormatter("%(asctime)s %(name)s[%(lineno)d] - %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%:M:%S")
f = "%(asctime)s %(name)s[%(lineno)d] - %(levelname)s: %(message)s"
ch.setFormatter(formatter)
ch_debug = None

# Function to create a custom log handler based on parameters
def create_log_handler(
    filename: Optional[str] = None,
    rotating: bool = False,
    level: int = logging.INFO,
    mode: str = "a+",
    encoding: str = "utf-8",
    format: str = "plain",
    maxBytes: int = 28000000,
    **kwargs
) -> Handler:

    if filename is None and rotating:
        raise ValueError("`filename` must be set to instantiate a `RotatingFileHandler`.")

    if filename is None:
        handler = StreamHandler(stream=sys.stdout, **kwargs)
        formatter = log_stream_formatter
    elif not rotating:
        handler = FileHandler(filename, mode=mode, encoding=encoding, **kwargs)
        formatter = log_file_formatter
    else:
        handler = RotatingFileHandler(
            filename, mode=mode, encoding=encoding, maxBytes=maxBytes, **kwargs
        )
        formatter = log_file_formatter

    if format == "json":
        formatter = json_formatter
    handler.setLevel(level)
    handler.setFormatter(formatter)
    return handler

# Set up initial stream handler for logging
ch = create_log_handler(level=log_level)
ch_debug: Optional[RotatingFileHandler] = None

# Set up directory paths and log file
current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
temp_dir = os.path.join(parent_directory, "temp")
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)
log_file = os.path.join(temp_dir, "log.log")

if not os.path.exists(log_file):
    open(log_file, 'w').close()

# Function to get a custom logger with file and console logging
def getLogger(name=None) -> Logger:
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    logger.addHandler(ch)
    logging.basicConfig(
        filename=log_file, filemode='w', encoding='utf-8', format=f, datefmt="%Y-%m-%d %H:%M:%S"
    )
    if ch_debug is not None:
        logger.addHandler(ch_debug)
    loggers.add(logger)
    return logger

# Function to configure logging for the project
def configure_logging(bot) -> None:
    global ch_debug, log_level, ch

    stream_log_format, file_log_format = "plain", "plain"
    if stream_log_format == "json":
        ch.setFormatter(json_formatter)
    level_text = "INFO"
    logging_levels = {
        "CRITICAL": logging.CRITICAL,
        "ERROR": logging.ERROR,
        "WARNING": logging.WARNING,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
    }

    level = logging_levels.get(level_text)
    log_level = level
    logger = getLogger(__name__)
    logger.info("Log file: %s", log_file)

    ch_debug = create_log_handler(log_file, rotating=True)

    if file_log_format == "json":
        ch_debug.setFormatter(json_formatter)

    ch.setLevel(log_level)

    logger.info("Stream log format: %s", stream_log_format)
    logger.info("File log format: %s", file_log_format)

    for log in loggers:
        log.setLevel(log_level)
        log.addHandler(ch_debug)

    d_level_text = "INFO"
    d_level = logging_levels.get(d_level_text)
    if d_level is None:
        logger.warning("Invalid discord logging level set: %s.", d_level_text)
        logger.warning("Using default discord logging level: %s.", d_level)
        d_level = logging_levels[d_level]
    d_logger = logging.getLogger("discord")
    d_logger.setLevel(d_level)

    non_verbose_log_level = max(d_level, logging.INFO)
    stream_handler = create_log_handler(level=non_verbose_log_level)
    if non_verbose_log_level != d_level:
        logger.info("Discord logging level (stdout): %s.", logging.getLevelName(non_verbose_log_level))
        logger.info("Discord logging level (logfile): %s.", logging.getLevelName(d_level))
    else:
        logger.info("Discord logging level: %s.", logging.getLevelName(d_level))
    d_logger.addHandler(stream_handler)
    d_logger.addHandler(ch_debug)

    logger.debug("Successfully configured logging.")