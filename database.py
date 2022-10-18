"""DataBase.

This module handles all the databases related activities.
"""
import logging
from typing import Union
import mysql.connector as connection
from logger import AppLogger


class DataBase:
    """Handle database activities."""

    def __init__(self) -> None:
        """Intialize required variables."""
        self.__is_client_connected = False
        self.__db = None
        self.__logger_class = AppLogger()
        self.__logger = self.__logger_class.get_logger(name="database")
        self.__tablename = "reviews"

    def db_connect(self, host="127.0.0.1", user="root", passwd="root") -> bool:
        """Connect to database.

        Args:
            host (str, optional): ip address. Defaults to "127.0.0.1".
            user (str, optional): username. Defaults to "root".
            passwd (str, optional): password. Defaults to "root".
            tablename (str, optional):tablename. Defaults to reviews
        Returns:
            bool: True on success, False on failure
        """
        try:
            self.__db = connection.connect(
                host=host, user=user, passwd=passwd, use_pure=True
            )
            if self.__db.is_connected() is False:
                self.__db = None
            else:
                self.__is_client_connected = True
                self.__logger.info("Connected to DB successfully")
                query = "CREATE DATABASE IF NOT EXISTS Flipkart"
                cur = self.__db.cursor()
                cur.execute(query)
                self.__db.commit()
        except Exception as db_exception:
            self.__db = None
            self.__logger.exception(str(db_exception))
        return self.__is_client_connected

    def create_table(self, tablename):
        """Create a table if not exists.

        Args:
            tablename (str): tablename
        """
        if self.__is_client_connected is True:
            self.__tablename = tablename
            try:
                cur = self.__db.cursor()
                query = f"CREATE TABLE IF NOT EXISTS Flipkart.{self.__tablename}(Name VARCHAR(50),Rating VARCHAR(5), CommentHead VARCHAR(100), Comment VARCHAR(1000))"
                cur.execute(query)
                self.__db.commit()
            except Exception as db_exception:
                self.__logger.exception(str(db_exception))
        else:
            self.__logger.warning("Database is not connected")

    def add_to_db(self, data) -> None:
        """Add given data to db.

        Args:
            data (list): data
        """
        if self.__is_client_connected is True:
            try:
                cur = self.__db.cursor()
                query = f'INSERT INTO Flipkart.{self.__tablename} VALUES("{data[0]}","{data[1]}","{data[2]}","{data[3]}")'
                cur.execute(query)
                self.__db.commit()
            except Exception as db_add_exception:
                self.__logger.exception(str(db_add_exception))
        else:
            self.__logger.info("Database is not connected")

    def check_if_table_exists(self, tablename) -> bool:
        """Check if a table already exists.

        Args:
            tablename (str): product name

        Returns:
            bool: True if exists else False
        """
        if self.__is_client_connected is True:
            cur = self.__db.cursor()
            query = f"SELECT COUNT(*) FROM information_schema.tables where table_name='{tablename}'"
            cur.execute(query)
            if cur.fetchone()[0] == 1:
                return True
            else:
                return False
        else:
            return True

    def get_data(self, tablename) -> Union[list, None]:
        """Get data if it exists.

        Args:
            tablename (str): tablename

        Returns:
            list | None: list if success else None
        """
        if self.__is_client_connected is True:
            try:
                cur = self.__db.cursor()
                query = f"SELECT * FROM Flipkart.{tablename}"
                cur.execute(query)
                data = list(cur.fetchall())
                self.__logger.info("Reusing the data from db")
                return data
            except Exception as db_exception:
                self.__logger.exception(db_exception)
                return None
        else:
            return None

    def close_db(self) -> None:
        """Close database."""
        if self.__is_client_connected is True:
            self.__db.close()
            self.__logger.info("Closed DB successfully")
