from chart.burndown import BurndownChart
from config import config
from gh.api_wrapper import get_repo_project, get_org_project

if __name__ == '__main__':
    repo_name = config['repo_name']
    if repo_name:
        project = get_project(
            config['username'],
            config['repo_name'],
            config['project_number'])
    else:
        project = get_org_project(
            config['username'],
            config['project_number'])
    burndown_chart = BurndownChart(project)
    burndown_chart.render()
    print('Done')