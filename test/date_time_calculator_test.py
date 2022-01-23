from __future__ import annotations
import unittest
from datetime import datetime
from src.austin_heller_repo.common import DateTimeDeltaCalculator


class DateTimeCalculatorTest(unittest.TestCase):

	def test_time_delta_section_previous_to_start_section(self):

		#	|			|			|			|			|			|
		#   |			|			|			start		>			eff end
		#	|			|			|			|			|			|
		#	td start	<			now			|			|			|
		#	|			|			|			|			|			|

		start_datetime = datetime(2022, 1, 10, 1, 0, 30)
		effective_seconds = 30
		now_datetime = datetime(2022, 1, 10, 1, 0, 29)
		time_delta = 20

		calculation = DateTimeDeltaCalculator.get_calculated_time_delta(
			start_datetime=start_datetime,
			effective_seconds=effective_seconds,
			now_datetime=now_datetime,
			time_delta=time_delta
		)

		self.assertEqual(0, calculation)

	def test_time_delta_section_previous_to_start_section_with_start_equals_now(self):

		#	|			|			|			|			|
		#   |			|			start		>			eff end
		#	|			|			|			|			|
		#	td start	<			now			|			|
		#	|			|			|			|			|

		start_datetime = datetime(2022, 1, 10, 1, 0, 30)
		effective_seconds = 30
		now_datetime = datetime(2022, 1, 10, 1, 0, 30)
		time_delta = 20

		calculation = DateTimeDeltaCalculator.get_calculated_time_delta(
			start_datetime=start_datetime,
			effective_seconds=effective_seconds,
			now_datetime=now_datetime,
			time_delta=time_delta
		)

		self.assertEqual(0, calculation)

	def test_time_delta_overlaps_start(self):
		#	|			|			|			|
		#   |			start		>			eff end
		#	|			|			|			|
		#	td start	<			now			|
		#	|			|			|			|

		start_datetime = datetime(2022, 1, 10, 1, 1, 0)
		effective_seconds = 60
		now_datetime = datetime(2022, 1, 10, 1, 1, 20)
		time_delta = 60

		calculation = DateTimeDeltaCalculator.get_calculated_time_delta(
			start_datetime=start_datetime,
			effective_seconds=effective_seconds,
			now_datetime=now_datetime,
			time_delta=time_delta
		)

		self.assertEqual(20, calculation)

	def test_time_delta_overlaps_start_with_now_equals_effective_end(self):
		#	|			|			|			|
		#   |			start		>			eff end
		#	|			|			|			|
		#	td start	<			<			now
		#	|			|			|			|

		start_datetime = datetime(2022, 1, 10, 1, 1, 0)
		effective_seconds = 60
		now_datetime = datetime(2022, 1, 10, 1, 2, 0)
		time_delta = 80

		calculation = DateTimeDeltaCalculator.get_calculated_time_delta(
			start_datetime=start_datetime,
			effective_seconds=effective_seconds,
			now_datetime=now_datetime,
			time_delta=time_delta
		)

		self.assertEqual(60, calculation)

	def test_time_delta_section_encapsulates_start_section(self):
		#	|			|			|			|			|
		#   |			start		>			eff end		|
		#	|			|			|			|			|
		#	td start	<			<			<			now
		#	|			|			|			|			|

		start_datetime = datetime(2022, 1, 10, 1, 1, 0)
		effective_seconds = 60
		now_datetime = datetime(2022, 1, 10, 1, 2, 30)
		time_delta = 120

		calculation = DateTimeDeltaCalculator.get_calculated_time_delta(
			start_datetime=start_datetime,
			effective_seconds=effective_seconds,
			now_datetime=now_datetime,
			time_delta=time_delta
		)

		self.assertEqual(60, calculation)

	def test_time_delta_section_within_start_section_with_previous_equal_to_start(self):
		#	|			|			|			|
		#   start		>			>			eff end
		#	|			|			|			|
		#	td start	<			now			|
		#	|			|			|			|

		start_datetime = datetime(2022, 1, 10, 1, 0, 0)
		effective_seconds = 60
		now_datetime = datetime(2022, 1, 10, 1, 0, 45)
		time_delta = 45

		calculation = DateTimeDeltaCalculator.get_calculated_time_delta(
			start_datetime=start_datetime,
			effective_seconds=effective_seconds,
			now_datetime=now_datetime,
			time_delta=time_delta
		)

		self.assertEqual(45, calculation)

	def test_time_delta_section_within_start_section_with_equal_distance(self):
		#	|			|			|			|			|
		#   start		>			>			>			eff end
		#	|			|			|			|			|
		#	td start	<			<			<			now
		#	|			|			|			|			|

		start_datetime = datetime(2022, 1, 10, 1, 0, 0)
		effective_seconds = 60
		now_datetime = datetime(2022, 1, 10, 1, 1, 0)
		time_delta = 60

		calculation = DateTimeDeltaCalculator.get_calculated_time_delta(
			start_datetime=start_datetime,
			effective_seconds=effective_seconds,
			now_datetime=now_datetime,
			time_delta=time_delta
		)

		self.assertEqual(60, calculation)

	def test_time_delta_section_encapsulates_start_section_with_now_after_effective_end(self):
		#	|			|			|			|			|
		#   start		>			>			eff end		|
		#	|			|			|			|			|
		#	td start	<			<			<			now
		#	|			|			|			|			|

		start_datetime = datetime(2022, 1, 10, 1, 0, 0)
		effective_seconds = 60
		now_datetime = datetime(2022, 1, 10, 1, 1, 30)
		time_delta = 90

		calculation = DateTimeDeltaCalculator.get_calculated_time_delta(
			start_datetime=start_datetime,
			effective_seconds=effective_seconds,
			now_datetime=now_datetime,
			time_delta=time_delta
		)

		self.assertEqual(60, calculation)

	def test_time_delta_section_within_start_section(self):
		#	|			|			|			|			|
		#   start		>			>			>			eff end
		#	|			|			|			|			|
		#	|			td start	<			now			|
		#	|			|			|			|			|

		start_datetime = datetime(2022, 1, 10, 1, 0, 0)
		effective_seconds = 60
		now_datetime = datetime(2022, 1, 10, 1, 0, 45)
		time_delta = 30

		calculation = DateTimeDeltaCalculator.get_calculated_time_delta(
			start_datetime=start_datetime,
			effective_seconds=effective_seconds,
			now_datetime=now_datetime,
			time_delta=time_delta
		)

		self.assertEqual(30, calculation)

	def test_time_delta_section_within_start_section_with_now_equal_to_effective_end(self):
		#	|			|			|			|			|
		#   start		>			>			>			eff end
		#	|			|			|			|			|
		#	|			td start	<			<			now
		#	|			|			|			|			|

		start_datetime = datetime(2022, 1, 10, 1, 0, 0)
		effective_seconds = 60
		now_datetime = datetime(2022, 1, 10, 1, 1, 0)
		time_delta = 45

		calculation = DateTimeDeltaCalculator.get_calculated_time_delta(
			start_datetime=start_datetime,
			effective_seconds=effective_seconds,
			now_datetime=now_datetime,
			time_delta=time_delta
		)

		self.assertEqual(45, calculation)

	def test_time_delta_overlaps_effective_end(self):
		#	|			|			|			|
		#   start		>			eff end		|
		#	|			|			|			|
		#	|			td start	<			now
		#	|			|			|			|

		start_datetime = datetime(2022, 1, 10, 1, 0, 0)
		effective_seconds = 60
		now_datetime = datetime(2022, 1, 10, 1, 1, 20)
		time_delta = 60

		calculation = DateTimeDeltaCalculator.get_calculated_time_delta(
			start_datetime=start_datetime,
			effective_seconds=effective_seconds,
			now_datetime=now_datetime,
			time_delta=time_delta
		)

		self.assertEqual(40, calculation)

	def test_time_delta_section_after_start_section_with_previous_equals_effective_end(self):
		#	|			|			|			|			|
		#   start		>			eff end		|			|
		#	|			|			|			|			|
		#	|			|			td start	<			now
		#	|			|			|			|			|

		start_datetime = datetime(2022, 1, 10, 1, 0, 0)
		effective_seconds = 30
		now_datetime = datetime(2022, 1, 10, 1, 1, 0)
		time_delta = 30

		calculation = DateTimeDeltaCalculator.get_calculated_time_delta(
			start_datetime=start_datetime,
			effective_seconds=effective_seconds,
			now_datetime=now_datetime,
			time_delta=time_delta
		)

		self.assertEqual(0, calculation)

	def test_time_delta_section_after_start_section(self):
		#	|			|			|			|			|			|
		#   start		>			eff end		|			|			|
		#	|			|			|			|			|			|
		#	|			|			|			td start	<			now
		#	|			|			|			|			|			|

		start_datetime = datetime(2022, 1, 10, 1, 0, 0)
		effective_seconds = 30
		now_datetime = datetime(2022, 1, 10, 1, 1, 0)
		time_delta = 29

		calculation = DateTimeDeltaCalculator.get_calculated_time_delta(
			start_datetime=start_datetime,
			effective_seconds=effective_seconds,
			now_datetime=now_datetime,
			time_delta=time_delta
		)

		self.assertEqual(0, calculation)
