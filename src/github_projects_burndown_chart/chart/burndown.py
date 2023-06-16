from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Iterable
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import numpy as np
import os

from util.dates import parse_to_local, date_range


@dataclass
class BurndownChartDataSeries:
    name: str
    data: Iterable[Dict[datetime, int]]
    format: Dict[str, Any]


def default_ideal_trendline_format() -> Dict[str, Any]:
    return dict(color="grey", linestyle=(0, (3, 3)))


@dataclass
class BurndownChartData:
    sprint_name: str
    utc_chart_start: datetime
    utc_chart_end: datetime
    utc_sprint_start: datetime
    utc_sprint_end: datetime
    total_points: int
    series: Iterable[BurndownChartDataSeries]
    points_label: str = "Outstanding Points"
    ideal_trendline_format: Dict[str, Any] = field(
        default_factory=default_ideal_trendline_format
    )


class BurndownChart:
    def __init__(self, data: BurndownChartData):
        self.data: BurndownChartData = data

    def __prepare_chart(self):
        # Plot the data
        chart_dates = date_range(self.data.utc_chart_start, self.data.utc_chart_end)
        for series in self.data.series:
            series_dates = [chart_dates.index(date) for date in series.data.keys()]
            series_points = list(series.data.values())
            cubic_series_dates = np.linspace(
                series_dates[0], series_dates[-1], num=100, endpoint=True
            )
            # series_points = [0 if point is None else point for point in series_points]
            f_cubic = interp1d(np.array(series_dates), np.array(series_points))
            plt.plot(
                # cubic_series_dates,
                # f_cubic(cubic_series_dates),
                series_dates,
                series_points,
                label=series.name,
                **series.format,
            )

        plt.legend()

        # Configure title and labels
        plt.title(f"Awan {self.data.sprint_name}: Burndown Chart")
        plt.ylabel(self.data.points_label)
        plt.xlabel("Date")

        # Configure axes limits
        plt.ylim(ymin=0, ymax=self.data.total_points * 1.1)
        plt.xlim(
            xmin=chart_dates.index(self.data.utc_chart_start),
            xmax=chart_dates.index(self.data.utc_chart_end),
        )

        # Configure x-axis tick marks
        date_labels = [str(parse_to_local(date))[:10] for date in chart_dates]
        plt.xticks(range(len(chart_dates)), date_labels)
        plt.xticks(rotation=90)

        # Plot the ideal trendline
        sprint_days = (self.data.utc_sprint_end - self.data.utc_sprint_start).days
        plt.axline(
            (chart_dates.index(self.data.utc_sprint_start), self.data.total_points),
            slope=-(self.data.total_points / (sprint_days)),
            **self.data.ideal_trendline_format,
        )

    def generate_chart(self, path):
        self.__prepare_chart()
        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path))
        plt.savefig(path)

    def render(self):
        self.__prepare_chart()
        plt.show()
