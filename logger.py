"""Logger.

This module handles all the logging mechanism.
"""
import logging


class AppLogger:
    """Logger class."""

    def __init__(self) -> None:
        """Intializes the required variables."""
        self.__log_format = (
            "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s)"
            ".%(funcName)s(%(lineno)d) - %(message)s"
        )

    def get_file_handler(self, log_file_name):
        """Write log to a file.

        Args:
            log_file_name (str): The name of the logfile
        Returns:
            FileHandler: FileHandler for logging to file
        """
        file_handler = logging.FileHandler(f"{log_file_name}.log", mode="w")
        file_handler.setFormatter(logging.Formatter(self.__log_format))
        return file_handler

    def get_stream_handler(self):
        """Write log to console.

        Returns:
            StreamHandler: StreamHandler for logging to console
        """
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter(self.__log_format))
        return stream_handler

    def get_logger(self, name, level=logging.INFO):
        """Get the logger with both file log and console log on different levels.

        Args:
            name (str): The name of the logger
            levle (int): log level
        Returns:
            logging: A logging object to use when logging in the code
        """
        logger = logging.getLogger(name)
        logger.addHandler(self.get_file_handler(name))
        logger.addHandler(self.get_stream_handler())
        logger.setLevel(level)
        return logger
