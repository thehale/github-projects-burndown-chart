from datetime import datetime, timedelta

from config import config


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

    def points_completed_by_date(self, start_date, end_date):
        points_completed_by_date = {
            str(date)[:10] : 0 
            for date in [
                start_date + timedelta(days=x) 
                for x in range(0, (end_date - start_date).days + 1)
            ]
        }
        for column in self.columns:
            for card in column.cards:
                if card.closedAt:
                    date_str = str(card.closedAt)[:10]
                    points_completed_by_date[date_str] += card.points
        return points_completed_by_date

    def outstanding_points_by_day(self, start_date, end_date):
        outstanding_points_by_day = {}
        points_completed = 0
        points_completed_by_date = self.points_completed_by_date(start_date, end_date)
        current_date = datetime.now()
        for date in points_completed_by_date:
            points_completed += points_completed_by_date[date]
            if datetime.strptime(date, '%Y-%m-%d') < current_date:
                outstanding_points_by_day[date] = self.total_points - points_completed
            else:
                outstanding_points_by_day[date] = None
        return outstanding_points_by_day


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
            createdAt = datetime.strptime(
                card_data['createdAt'][:10],
                '%Y-%m-%d')
        return createdAt

    def __parse_closedAt(self, card_data):
        closedAt = None
        if card_data.get('closedAt'):
            closedAt = datetime.strptime(
                card_data['closedAt'][:10],
                '%Y-%m-%d')
        return closedAt

    def __parse_points(self, card_data):
        card_points = 0
        card_labels = card_data.get('labels', {"nodes": []})['nodes']
        for label in card_labels:
            if config['points_label'] in label['name']:
                card_points += int(label['name'][len(config['points_label']):])
        return card_points