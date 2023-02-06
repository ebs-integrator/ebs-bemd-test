from typing import Dict
from datetime import timedelta

from apps.products.models import PriceInterval


class Prices:
    def __init__(self, data: dict):
        self.data: dict = data
        self.price = 0
        self.days = 0

    def query_records(self):
        return PriceInterval.objects.filter(
            product=self.data.get('product'),
            end_date__gte=self.data.get('start_date'),
            start_date__lte=self.data.get('end_date')
        )

    def get_average(self) -> Dict:
        for record in self.query_records():
            if record.start_date > self.data.get('start_date'):
                start_date = record.start_date
            else:
                start_date = self.data.get('start_date')

            if record.end_date < self.data.get('end_date'):
                end_date = record.end_date
            else:
                end_date = self.data.get('end_date')

            days = end_date - start_date + timedelta(days=1)

            self.price += record.price * days.days
            self.days += days.days
        return {
            "price": self.price / self.days,
            "days": (self.data.get('end_date') - self.data.get('start_date') + timedelta(days=1)).days
        }
