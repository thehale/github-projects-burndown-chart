from datetime import datetime
import json
import os
import logging

from util.dates import parse_to_utc

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

###############################################################################
# Load config.json
###############################################################################
try:
    with open(os.path.join(__location__, 'config.json')) as config_json:
        __config = json.load(config_json)
except FileNotFoundError as err:
    __logger.critical(err)
    __logger.critical('Please create a config.json file in the config '
                      'directory; this tool cannot generate a burndown chart without it.')
    __logger.critical('See the project README.md and config/config.json.dist '
                      'for details.')
    exit(1)


class Config:

    def __init__(self, raw_config: dict):
        self.raw_config = raw_config

    def set_project(self, project_type: str, project_name: str):
        self.project_type = project_type
        self.project_name = project_name

    def utc_sprint_start(self) -> datetime:
        return self.__get_date('sprint_start_date')

    def utc_sprint_end(self) -> datetime:
        return self.__get_date('sprint_end_date')

    def utc_chart_end(self) -> datetime:
        return self.__get_date('chart_end_date')

    def __getitem__(self, key: str):
        if not hasattr(self, 'project_type'):
            raise AttributeError('No project has been set.')
        if not hasattr(self, 'project_name'):
            raise AttributeError('No project has been set.')
        return self.raw_config[self.project_type][self.project_name][key]

    def __get_date(self, name: str) -> datetime:
        date = self['settings'].get(name)
        return parse_to_utc(date) if date else None


config = Config(__config)


###############################################################################
# Load secrets.json
###############################################################################
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
