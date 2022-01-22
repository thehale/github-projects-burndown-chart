from datetime import datetime, timedelta
from typing import Dict, Iterable
from gh.project import *
from util.dates import TODAY_UTC, date_range
from util.calculators import *


class ProjectStats():

    def __init__(self, project: Project, start_date: datetime, end_date: datetime):
        self.start_date: datetime = start_date
        self.end_date: datetime = end_date
        self.project: Project = project

    @property
    def total_points(self) -> int:
        return self.project.total_points

    def points_by_date(self, calculator: PointsCalculator) -> Dict[datetime, int]:
        points = {}
        sprint_dates: Iterable[datetime] = date_range(
            self.start_date, self.end_date)
        for date in sprint_dates:
            # Get the issues completed before midnight on the given date.
            date_23_59 = date + timedelta(hours=23, minutes=59)
            points[date] = calculator.points_as_of(date_23_59)
        return points

    def remaining_points_by_date(self, calculator: PointsCalculator) -> Dict[datetime, int]:
        points_by_date = self.points_by_date(calculator)
        today_23_59 = TODAY_UTC + timedelta(hours=23, minutes=59)
        return {
            date: self.total_points - points_by_date[date]
            if date <= today_23_59 else None
            for date in points_by_date
        }
