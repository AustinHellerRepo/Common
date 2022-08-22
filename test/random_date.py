import unittest
from datetime import date, datetime, timedelta
import random
import uuid
from typing import List, Tuple, Dict, Set
from src.austin_heller_repo.common import get_random_date
import itertools


days_between_min_and_max = (date.max - date.min)
print(f"days between: {days_between_min_and_max}")

# need to get days between 1000-01-01 and max in order to avoid less-than-4 digit years
earliest_date = date(1000, 1, 1)
print(f"days between 4 year earliest: {(date.max - earliest_date)}")

days_total = 3652058
add_days_timedelta = timedelta(days=days_total)
print(f"min date {date.min} plus {days_total} equals {date.min + add_days_timedelta}.")


four_year_days_total = 3287181
offset_days_total = 364877
four_year_add_days_timedelta = timedelta(days=four_year_days_total)
print(f"min date {earliest_date} plus {four_year_days_total} equals {earliest_date + four_year_add_days_timedelta}.")


class RandomDate(unittest.TestCase):

    def test_generate_with_seed(self):

        seeds = []
        random_dates_per_seed = {}  # type: Dict[str, List[date]]
        for _ in range(100):
            seed = str(uuid.uuid4())
            seeds.append(seed)
            random_instance = random.Random(seed)
            random_dates_per_seed[seed] = []
            for _ in range(10):
                random_date = get_random_date(
                    random_instance=random_instance
                )
                random_dates_per_seed[seed].append(random_date)

        for seed in seeds:
            random_instance = random.Random(seed)
            for random_date in random_dates_per_seed[seed]:
                generated_random_date = get_random_date(
                    random_instance=random_instance
                )
                self.assertEqual(random_date, generated_random_date)

        for first_index, first_random_date in enumerate([
            individual_random_date for individual_random_dates in [
                random_dates for random_dates in random_dates_per_seed.values()
            ] for individual_random_date in individual_random_dates
        ]):
            for second_index, second_random_date in enumerate([
                individual_random_date for individual_random_dates in [
                    random_dates for random_dates in random_dates_per_seed.values()
                ] for individual_random_date in individual_random_dates
            ]):
                if first_index == second_index:
                    self.assertEqual(first_random_date, second_random_date)
                else:
                    self.assertNotEqual(first_random_date, second_random_date)
