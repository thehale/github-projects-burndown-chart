from gh.project import Project
from util.calculators import *


def calculators(project: Project):
    return {
        'created': CreatedPointsCalculator(project.cards),
        'assigned': AssignedPointsCalculator(project.cards),
        'closed': ClosedPointsCalculator(project.cards),
        'taiga': TaigaPointsCalculator(project.cards)
    }

def colors():
    count = -1
    colors = ['blue', 'green', 'gold',  'red', 'orange',
              'purple', 'pink', 'brown', 'black', 'grey']
    while True:
        count += 1
        yield colors[count % len(colors)]