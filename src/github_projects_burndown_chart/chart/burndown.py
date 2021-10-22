import matplotlib.pyplot as plt
from datetime import datetime

from config import config
from gh.project import Project
from util.dates import parse_to_local, parse_to_utc


class BurndownChart:

    def __init__(self, project: Project):
        self.start_date_utc: datetime = parse_to_utc(
            config['settings']['sprint_start_date'])
        self.end_date_utc: datetime = parse_to_utc(
            config['settings']['sprint_end_date'])

        self.project: Project = project

    def render(self):
        outstanding_points_by_day = self.project.outstanding_points_by_date(
            self.start_date_utc,
            self.end_date_utc)
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
        date_labels = [str(parse_to_local(date))[:10]
                       for date in outstanding_points_by_day.keys()]
        plt.xticks(x, date_labels)
        plt.xticks(rotation=90)

        # Set titles and labels
        plt.title(f"{self.project.name}: Burndown Chart")
        points_label = config['settings']['points_label']
        plt.ylabel(f"Outstanding {'Points' if points_label else 'Issues'}")
        plt.xlabel("Date")

        # Generate Plot
        plt.show()
