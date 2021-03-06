from __future__ import annotations
import unittest
from src.austin_heller_repo.common import get_non_maximum_suppression_rectangles


class NonMaximumSuppressionTest(unittest.TestCase):

	def test_no_rectangles(self):

		actual_rectangles = get_non_maximum_suppression_rectangles(
			rectangles=[],
			overlap_threshold=1.0
		)

		self.assertIsNotNone(actual_rectangles)
		self.assertEqual(0, len(actual_rectangles))

	def test_one_rectangle(self):

		actual_rectangles = get_non_maximum_suppression_rectangles(
			rectangles=[
				(1, 2, 3, 4)
			],
			overlap_threshold=1.0
		)

		self.assertIsNotNone(actual_rectangles)
		self.assertEqual(1, len(actual_rectangles))

	def test_two_nonoverlapping_rectangles(self):

		actual_rectangles = get_non_maximum_suppression_rectangles(
			rectangles=[
				(1, 2, 3, 4),
				(5, 2, 3, 4)
			],
			overlap_threshold=0.01
		)

		print(f"actual_rectangles: {actual_rectangles}")

	def test_two_overlapping_rectangles(self):

		actual_rectangles = get_non_maximum_suppression_rectangles(
			rectangles=[
				(1, 2, 3, 4),
				(1.1, 2.1, 3, 4)
			],
			overlap_threshold=0.01
		)

		print(f"actual_rectangles: {actual_rectangles}")
