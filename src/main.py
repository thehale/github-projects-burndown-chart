from chart.burndown import BurndownChart
from config import config
from gh.api_wrapper import get_project

if __name__ == '__main__':
    project = get_project(
        config['repo_owner'],
        config['repo_name'],
        config['project_number'])
    burndown_chart = BurndownChart(project)
    burndown_chart.render()
    print('Done')