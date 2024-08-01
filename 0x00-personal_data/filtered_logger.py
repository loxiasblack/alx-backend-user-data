#!/usr/bin/env python3
""" first interaction with pii"""
from typing import List
import re
import logging
import os
from mysql.connector import MySQLConnection
import mysql.connector

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str],
                 redaction: str, message: str,
                 separator: str) -> str:
    """ function that filter the list """
    return re.sub(rf'({"|".join(map(re.escape, fields))})=[^{separator}]*',
                  lambda m: f"{m.group(1)}={redaction}", message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ instantiation """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ format function that return format """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def get_logger() -> logging.Logger:
    """ Create function get_logger
        goal is to display logging info about
        the app in the console with the formatted class
        created above """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    fromatter = RedactingFormatter(fields=PII_FIELDS)
    console_handler.setFormatter(fromatter)

    logger.addHandler(console_handler)
    return logger


def get_db() -> MySQLConnection:
    """ get db function that return a db"""
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    if not db_name:
        raise ValueError("Database name not provided in environment variables")

    connection = mysql.connector.connect(
        username=username,
        password=password,
        host=host,
        database=db_name
    )

    return connection
