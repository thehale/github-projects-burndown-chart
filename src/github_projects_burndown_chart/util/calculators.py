from datetime import datetime
from typing import List

from gh.project import Card


class PointsCalculator:

    def __init__(self, cards: List[Card]):
        self.cards: List[Card] = cards

    def points_as_of(self, date: datetime):
        raise NotImplementedError()


class ClosedPointsCalculator(PointsCalculator):

    def points_as_of(self, date: datetime):
        return sum(card.points for card in self.cards
                   if isinstance(card.closed, datetime)
                   and card.closed <= date)


class AssignedPointsCalculator(PointsCalculator):

    def points_as_of(self, date: datetime):
        return sum(card.points for card in self.cards
                   if isinstance(card.assigned, datetime)
                   and card.assigned <= date)


class CreatedPointsCalculator(PointsCalculator):

    def points_as_of(self, date: datetime):
        return sum(card.points for card in self.cards
                   if isinstance(card.created, datetime)
                   and card.created <= date)


class TaigaPointsCalculator(PointsCalculator):

    def points_as_of(self, date: datetime):
        closed_by_date = [card for card in self.cards
                          if isinstance(getattr(card, 'closed'), datetime)
                          and getattr(card, 'closed') <= date]
        points = sum(card.points for card in closed_by_date)
        assigned_by_date = [card for card in self.cards
                            if isinstance(getattr(card, 'assigned'), datetime)
                            and getattr(card, 'assigned') <= date
                            and card not in closed_by_date]
        points += sum(card.points / 2 for card in assigned_by_date)
        return points
