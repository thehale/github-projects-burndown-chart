from datetime import datetime, timedelta
from typing import Dict
from dateutil.parser import isoparse

from config import config
from util.dates import TODAY_UTC


class Project:
    def __init__(self, project_data):
        self.name = project_data['name']
        self.columns = self.__parse_columns(project_data)

    def __parse_columns(self, project_data):
        columns_data = project_data['columns']['nodes']
        columns = [Column(column_data) for column_data in columns_data]
        return columns

    @property
    def total_points(self):
        return sum([column.get_total_points() for column in self.columns])

    def points_completed_by_date(self, start_date: datetime, end_date: datetime) -> Dict[datetime, int]:
        """Computes the number of points completed by date.
        Basically the data behind a burnup chart for the given date range.

        Args:
            start_date (datetime): The start date of the chart in UTC.
            end_date (datetime): The end date of the chart in UTC.

        Returns:
            Dict[datetime, int]: A dictionary of date and points completed.
        """
        points_completed_by_date = {}

        cards = [card for column in self.columns for card in column.cards]
        completed_cards = [card for card in cards if card.closedAt is not None]
        sprint_dates = [start_date + timedelta(days=x)
                        # The +1 includes the end_date in the list
                        for x in range(0, (end_date - start_date).days + 1)]
        for date in sprint_dates:
            # Get the issues completed before midnight on the given date.
            date_23_59 = date + timedelta(hours=23, minutes=59)
            cards_done_by_date = [card for card in completed_cards
                                  if card.closedAt <= date_23_59]
            points_completed_by_date[date] = sum([card.points for card
                                                  in cards_done_by_date])
        return points_completed_by_date

    def outstanding_points_by_date(self, start_date: datetime, end_date: datetime) -> Dict[datetime, int]:
        """Computes the number of points remaining to be completed by date.
        Basically the data behind a burndown chart for the given date range.

        Args:
            start_date (datetime): The start date of the chart in UTC.
            end_date (datetime): The end date of the chart in UTC.

        Returns:
            Dict[datetime, int]: A dictionary of date and points remaining.
        """
        points_completed_by_date = self.points_completed_by_date(
            start_date, end_date)
        today_23_59 = TODAY_UTC + timedelta(hours=23, minutes=59)
        return {
            date: self.total_points - points_completed_by_date[date]
            if date <= today_23_59 else None
            for date in points_completed_by_date
        }


class Column:
    def __init__(self, column_data):
        self.cards = self.__parse_cards(column_data)

    def __parse_cards(self, column_data):
        cards_data = column_data['cards']['nodes']
        cards = [Card(card_data) for card_data in cards_data]
        return cards

    def get_total_points(self):
        return sum([card.points for card in self.cards])


class Card:
    def __init__(self, card_data):
        card_data = card_data['content'] if card_data['content'] else card_data
        self.createdAt = self.__parse_createdAt(card_data)
        self.closedAt = self.__parse_closedAt(card_data)
        self.points = self.__parse_points(card_data)

    def __parse_createdAt(self, card_data):
        createdAt = None
        if card_data.get('createdAt'):
            createdAt = isoparse(card_data['createdAt'])
        return createdAt

    def __parse_closedAt(self, card_data):
        closedAt = None
        if card_data.get('closedAt'):
            closedAt = isoparse(card_data['closedAt'])
        return closedAt

    def __parse_points(self, card_data):
        card_points = 0
        points_label = config['settings']['points_label']
        if not points_label:
            card_points = 1
        else:
            card_labels = card_data.get('labels', {"nodes": []})['nodes']
            card_points = sum([int(label['name'][len(points_label):])
                              for label in card_labels
                              if points_label in label['name']])
        return card_points
