import json
import os
import logging

# Set up logging
__logger = logging.getLogger(__name__)
__ch = logging.StreamHandler()
__ch.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
__logger.addHandler(__ch)

# File I/O inspired by https://stackoverflow.com/a/4060259/14765128
__location__ = os.path.realpath(
    os.path.join(
        os.getcwd(),
        os.path.dirname(__file__)))

try:
    with open(os.path.join(__location__, 'config.json')) as config_json:
        config = json.load(config_json)
except FileNotFoundError as err:
    __logger.critical(err)
    __logger.critical('Please create a config.json file in the config '
        'directory; this tool cannot generate a burndown chart without it.')
    __logger.critical('See the project README.md and config/config.json.dist '
        'for details.')
    exit(1)

try:
    with open(os.path.join(__location__, 'secrets.json')) as secrets_json:
        secrets = json.load(secrets_json)
except FileNotFoundError as err:
    __logger.critical(err)
    __logger.critical('Please create a secrets.json file in the config '
        'directory; this tool cannot generate a burndown chart without it.')
    __logger.critical('See the project README.md and config/secrets.json.dist '
        'for details.')
    exit(1)