from datetime import datetime

from data.dataclasses.delivery_date import DeliveryDate
from data.generators.generator import BaseFakerGenerator


class DateGenerator(BaseFakerGenerator):
    def date_generator(self):

        date = self.faker.future_date()
        dt = datetime.strptime(str(date), '%Y-%m-%d')
        formatted_date = dt.strftime('%m/%d/%y')

        month_contraction = self.faker.month_name()[:3].upper()
        month = self.faker.month_name()

        day = self.faker.day_of_month()

        if day.startswith('0'):
            day = day[1:]

        return DeliveryDate(
            year=str(self.faker.future_date().year),
            month=month_contraction,
            day=day,
            date=formatted_date
        )