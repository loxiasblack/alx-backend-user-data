#!/usr/bin/env python3
""" first interaction with pii"""
from typing import List
import re
import logging


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
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)
