#!/usr/bin/env python3
""" first interaction with pii"""
from typing import List
import re


def filter_datum(fields: List[str],
                 redaction: str, message: str,
                 separator: str) -> str:
    """ function that filter the list """
    return re.sub(rf'({"|".join(map(re.escape, fields))})=[^{separator}]*',
                  lambda m: f"{m.group(1)}={redaction}", message)
