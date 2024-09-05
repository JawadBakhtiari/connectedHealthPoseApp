#!/usr/bin/env python3

import json
import sys
from validator import Validator

try:
    config_filepath = sys.argv[1]
except:
    print(f'usage: {sys.argv[0]} <path/to/validation/config/file>')
    exit(1)

with open(config_filepath) as f:
    config = json.load(f)

validator = Validator(config.get('mobile_data_filepath'), config.get('lab_data_filepath'))
validator.validate(config.get('angles'))

