from chart.burndown import BurndownChart
from gh.api_wrapper import get_repository_project
from gh.project import Project

if __name__ == '__main__':
    project: Project = get_repository_project()
    burndown_chart = BurndownChart(project)
    burndown_chart.render()
    print('Done')