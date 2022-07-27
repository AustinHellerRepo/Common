import unittest
from src.austin_heller_repo.common import convert_date_to_string, convert_string_to_date, convert_datetime_to_string, convert_string_to_datetime
from datetime import datetime, date, timedelta
import random


class DateTimeAndDateFormatTest(unittest.TestCase):

    def test_datetime_format(self):
        start_date = datetime(1, 1, 1)
        max_days_total = 365 * 3000

        for _ in range(10000):
            random_days = timedelta(max_days_total * random.random())
            random_datetime = start_date + random_days
            random_datetime_string = convert_datetime_to_string(
                datetime=random_datetime
            )
            self.assertIsNotNone(random_datetime_string)
            converted_datetime = convert_string_to_datetime(
                string=random_datetime_string
            )
            self.assertEqual(random_datetime, converted_datetime)

    def test_date_format(self):
        start_date = date(1, 1, 1)
        max_days_total = 365 * 3000

        for _ in range(10000):
            random_days = timedelta(int(max_days_total * random.random()))
            random_date = start_date + random_days
            random_date_string = convert_date_to_string(
                date=random_date
            )
            self.assertIsNotNone(random_date_string)
            converted_date = convert_string_to_date(
                string=random_date_string
            )
            self.assertEqual(random_date, converted_date)
