import argparse

from chart.burndown import BurndownChart
from config import config
from gh.api_wrapper import get_organization_project, get_repository_project
from gh.project import Project

if __name__ == '__main__':
    # Parse the command line arguments
    parser = argparse.ArgumentParser(
        description='Generate a burndown chart for a GitHub project.')
    parser.add_argument("project_type",
                        choices=['repository', 'organization'],
                        help="The type of project to generate a burndown chart for. Can be either 'organization' or 'repository'.")
    parser.add_argument("project_name", help="The name of the project as it appears in the config.json")
    args = parser.parse_args()

    # Point the config to the correct project
    config.set_project(args.project_type, args.project_name)
    
    # Pull the corresponding project from GitHub
    if args.project_type == 'repository':
        project: Project = get_repository_project()
    elif args.project_type == 'organization':
        project: Project = get_organization_project()
    
    # Generate the burndown chart
    burndown_chart = BurndownChart(project)
    burndown_chart.render()
    print('Done')
