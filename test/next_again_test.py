from __future__ import annotations
import unittest
from src.austin_heller_repo.common import next_again


class NextAgainTest(unittest.TestCase):

    def test_list(self):

        some_list = [0, 1, 2, 3]
        for some_list_index in range(len(some_list) + 1):
            item = next_again(some_list, some_list_index)
            if some_list_index == 0:
                self.assertIsNone(item)
            else:
                self.assertEqual(some_list[some_list_index - 1], item)

    def test_range(self):

        some_range = range(4)
        for some_list_index in range(len(some_range) + 1):
            item = next_again(some_range, some_list_index)
            if some_list_index == 0:
                self.assertIsNone(item)
            else:
                self.assertEqual(some_range[some_list_index - 1], item)

    def test_list_already_iterator(self):

        some_list = iter([0, 1, 2, 3])
        for some_list_index in range(5):
            item = next_again(some_list, some_list_index if some_list_index == 0 else 1)
            if some_list_index == 0:
                self.assertIsNone(item)
            else:
                self.assertEqual(some_list_index - 1, item)
