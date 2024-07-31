#!/usr/bin/env python3
""" filtered logger """
from typing import List
import re


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str, separator: str) -> str:
    """ function that change pii by redaction"""
    for field in fields:
        pattern = re.compile(rf"{re.escape(field)}=[^\\{separator}]*")
        message = pattern.sub(f"{field}={redaction}", message)
    return message
