#!/usr/bin/env python

import json
import jsonschema
from collections import namedtuple

MSG_SCHEMA = json.load(open('resources/json/message.json'))


def validate_message(message):
    jsonschema.validate(message, MSG_SCHEMA)
    return True


def parse_message(message):
    return (json.loads(message, object_hook=lambda d: namedtuple(
        'X', d.keys())(*d.values())))._asdict()
