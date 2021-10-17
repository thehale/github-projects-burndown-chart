import logging
import requests
from requests.api import head

from config import config, secrets
from .project import Project
from .queries import OrganizationProject, RepositoryProject

# Set up logging
__logger = logging.getLogger(__name__)
__ch = logging.StreamHandler()
__ch.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
__logger.addHandler(__ch)


def get_repository_project() -> dict:
    query_variables = config['query_variables']
    query_response = gh_api_query(RepositoryProject, query_variables)
    project_data = query_response['data']['repository']['project']
    return Project(project_data)


def get_organization_project() -> dict:
    query_variables = config['query_variables']
    query_response = gh_api_query(OrganizationProject, query_variables)
    project_data = query_response['data']['organization']['project']
    return Project(project_data)


def gh_api_query(query: str, variables: dict) -> dict:
    headers = {'Authorization': 'bearer %s' % secrets['github_token']} \
        if 'github_token' in secrets else {}

    response = requests.post(
        'https://api.github.com/graphql',
        headers=headers,
        json={'query': query, 'variables': variables}).json()

    # Gracefully report failures due to bad credentials
    if response.get('message') and response['message'] == 'Bad credentials':
        __logger.critical(response['message'])
        __logger.critical('Failed to extract project data from GitHub due '
                          'to an invalid access token.')
        __logger.critical('Please set the `github_token` key in the '
                          '`src/secrets.json` file to a valid access token with access '
                          'to the repo specified in the `src/config.json` file.')
        exit(1)
    # Gracefully report failures due to errors
    elif response.get('errors'):
        __logger.critical('Failed to extract project data from GitHub due to '
                          'an error.')
        __logger.critical(response['errors'])
        exit(1)
    return response
