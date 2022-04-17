from __future__ import annotations
import unittest
from src.austin_heller_repo.common import get_random_rainbow_color
import random


class RandomColorTest(unittest.TestCase):

	def test_random_rainbow_color(self):

		random_instance = random.Random(0)
		for _ in range(1000):
			color = get_random_rainbow_color(
				random_instance=random_instance
			)
			found_index = None
			for color_index in range(3):
				if color[color_index] == 1.0:
					found_index = color_index
					break
			self.assertIsNotNone(found_index)
			self.assertTrue(0 <= color[(found_index + 1) % 3] <= 1)
			self.assertTrue(0 <= color[(found_index + 2) % 3] <= 1)
			self.assertEqual(1, color[(found_index + 1) % 3] + color[(found_index + 2) % 3])
