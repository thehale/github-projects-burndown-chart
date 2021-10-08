import matplotlib.pyplot as plt
from datetime import datetime

from config import config
from gh.project import Project

class BurndownChart:

    def __init__(self, project: Project):
        # Initialize important dates
        self.start_date = datetime.strptime(
            config['sprint_start_date'],
            '%Y-%m-%d')
        self.end_date = datetime.strptime(
            config['sprint_end_date'],
            '%Y-%m-%d')
        self.project = project
    
    def render(self):
        outstanding_points_by_day = self.project.outstanding_points_by_day(
            self.start_date,
            self.end_date)
        # Load date dict for priority values with x being range of how many days are in sprint
        x = list(range(len(outstanding_points_by_day.keys())))
        y = list(outstanding_points_by_day.values())

        # Plot point values for sprint along xaxis=range yaxis=points over time
        plt.plot(x, y)
        plt.axline((x[0], self.project.total_points),
            slope=-(self.project.total_points/(len(y)-1)),
            color="green",
            linestyle=(0, (5, 5)))

        # Set sprint beginning
        plt.ylim(ymin=0)
        plt.xlim(xmin=x[0], xmax=x[-1])

        # Replace xaxis range for date matching to range value
        plt.xticks(x, outstanding_points_by_day.keys())
        plt.xticks(rotation=90)

        # Set titles and labels
        plt.title(f"{self.project.name}: Burndown Chart")
        plt.ylabel("Outstanding Points")
        plt.xlabel("Date")

        # Generate Plot
        plt.show()
