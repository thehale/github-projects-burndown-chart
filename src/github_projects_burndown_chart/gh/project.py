from datetime import datetime
from dateutil.parser import isoparse

from config import config


class Project:
    def __init__(self, project_data):
        self.name = project_data["name"]
        self.columns = self.__parse_columns(project_data)

    def __parse_columns(self, project_data):
        columns_data = project_data["columns"]["nodes"]
        columns = [Column(column_data) for column_data in columns_data]
        return columns

    @property
    def total_points(self):
        return sum([column.get_total_points() for column in self.columns])

    @property
    def cards(self):
        return [card for column in self.columns for card in column.cards]


class Column:
    def __init__(self, column_data):
        self.cards = self.__parse_cards(column_data)

    def __parse_cards(self, column_data):
        cards_data = column_data["cards"]["nodes"]
        cards = [Card(card_data) for card_data in cards_data]
        return cards

    def get_total_points(self):
        return sum([card.points for card in self.cards])


class Card:
    def __init__(self, card_data):
        self.column_name = card_data["column"]["name"]

        card_data = card_data["content"] if card_data["content"] else card_data
        self.created: datetime = self.__parse_createdAt(card_data)
        self.assigned: datetime = self.__parse_assignedAt(card_data)
        self.closed: datetime = self.__parse_closedAt(card_data)
        self.moved: datetime = self.__parse_movedAt(card_data)
        self.points = self.__parse_points(card_data)

    def __parse_assignedAt(self, card_data) -> datetime:
        assignedAt = None
        assignedDates = card_data.get("timelineItems", {}).get("nodes", [])
        if assignedDates:
            assignedAt = isoparse(assignedDates[0]["createdAt"])
        return assignedAt

    def __parse_createdAt(self, card_data) -> datetime:
        createdAt = None
        if card_data.get("createdAt"):
            createdAt = isoparse(card_data["createdAt"])
        return createdAt

    def __parse_closedAt(self, card_data) -> datetime:
        closedAt = None
        if card_data.get("closedAt"):
            closedAt = isoparse(card_data["closedAt"])
        return closedAt

    def __parse_movedAt(self, card_data) -> datetime:
        movedAt = None
        last_event = card_data["timelineItems"]["nodes"][-1]
        if last_event.get("__typename") == "MovedColumnsInProjectEvent":
            card_data["movedAt"] = last_event["createdAt"]
        if card_data.get("movedAt"):
            movedAt = isoparse(card_data["movedAt"])
        return movedAt

    def __convert_hours(self, points_label: str, card_lables: list) -> list:
        for label in card_lables:
            if points_label in label["name"]:
                if "h" in label["name"]:
                    label["name"] = points_label + str(
                        float(label["name"][len(points_label) :].replace("h", "")) / 8
                    )
                elif "d" in label["name"]:
                    label["name"] = points_label + str(
                        float(label["name"][len(points_label) :].replace("d", ""))
                    )
        return card_lables

    def __parse_points(self, card_data) -> float:
        card_points = 0
        points_label = config["settings"]["points_label"]
        if not points_label:
            card_points = 1
        else:
            card_labels = card_data.get("labels", {"nodes": []})["nodes"]
            card_labels = self.__convert_hours(points_label, card_labels)
            card_points = sum(
                [
                    float(label["name"][len(points_label) :])
                    for label in card_labels
                    if points_label in label["name"]
                ]
            )
            print(card_points)
        return card_points
