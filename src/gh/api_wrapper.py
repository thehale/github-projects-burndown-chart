import logging
import requests
from requests.api import head

from config import secrets
from .project import Project

# Set up logging
__logger = logging.getLogger(__name__)
__ch = logging.StreamHandler()
__ch.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
__logger.addHandler(__ch)

repo_project_query = """
query {
  repository(owner: "%(username)s", name: "%(repo_name)s") {
    project(number: %(project_number)d) {
      name
      columns(first: 5) {
        nodes {
          name
          cards(first: 50) {
            nodes {
              id
              note
              state
              content {
                ... on Issue {
                  title
                  createdAt
                  closedAt
                  labels(first: 5) {
                    nodes {
                      name
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
"""  # Heavily inspired by https://github.com/radekstepan/burnchart/issues/129#issuecomment-394469442

org_project_query = """
query {
  organization(login: "%(username)s") {
    project(number: %(project_number)d) {
      name
      columns(first: 5) {
        nodes {
          name
          cards(first: 50) {
            nodes {
              id
              note
              state
              content {
                ... on Issue {
                  title
                  createdAt
                  closedAt
                  labels(first: 5) {
                    nodes {
                      name
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
"""  # Heavily inspired by https://github.com/radekstepan/burnchart/issues/129#issuecomment-394469442

def get_repo_project(username: str, repo_name: str, project_number: int) -> dict:
    query = repo_project_query % {
        'username': username,
        'repo_name': repo_name,
        'project_number': project_number}
    query_response = gh_api_query(query)
    project_data = query_response['data']['repository']['project']
    return Project(project_data)

def get_org_project(username: str, project_number: int) -> dict:
    query = org_project_query % {
        'username': username,
        'project_number': project_number}
    query_response = gh_api_query(query)
    project_data = query_response['data']['organization']['project']
    return Project(project_data)

def gh_api_query(query: str) -> dict:
    headers = {'Authorization': 'bearer %s' % secrets['github_token']} \
        if 'github_token' in secrets else {}
    response = requests.post(
        'https://api.github.com/graphql',
        headers=headers,
        json={'query': query}).json()
    # Gracefully report failures due to bad credentials
    if response.get('message') and response['message'] == 'Bad credentials':
        __logger.critical(response['message'])
        __logger.critical('Failed to extract project data from GitHub due '
            'to an invalid access token.')
        __logger.critical('Please set the `github_token` key in the '
            '`src/secrets.json` file to a valid access token with access '
            'to the repo specified in the `src/config.json` file.')
        exit(1)
    return response
        