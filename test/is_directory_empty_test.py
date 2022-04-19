from __future__ import annotations
import unittest
import os
from src.austin_heller_repo.common import is_directory_empty
import tempfile


class IsDirectoryEmptyTest(unittest.TestCase):

	def test_empty_directory(self):

		directory = tempfile.TemporaryDirectory()

		try:
			is_empty = is_directory_empty(
				directory_path=directory.name
			)

			self.assertTrue(is_empty)

		finally:
			directory.cleanup()

	def test_nonempty_directory(self):

		directory = tempfile.TemporaryDirectory()

		try:
			with open(os.path.join(directory.name, "test.txt "), "w") as file_handle:
				file_handle.write("test line")

			is_empty = is_directory_empty(
				directory_path=directory.name
			)

			self.assertFalse(is_empty)

		finally:
			directory.cleanup()
