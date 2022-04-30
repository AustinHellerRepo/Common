from __future__ import annotations
import unittest
from src.austin_heller_repo.common import load_file_as_base64string, save_file_from_base64string
import tempfile
import os


class Base64EncodeDecodeTest(unittest.TestCase):

	def test_save_file_and_load_file(self):

		expected_file_contents = ["test\n", "here"]

		original_file = tempfile.NamedTemporaryFile(delete=False)

		try:
			with open(original_file.name, "w") as file_handle:
				file_handle.writelines(expected_file_contents)

			file_bytes_base64string = load_file_as_base64string(
				file_path=original_file.name
			)

		finally:
			original_file.close()
			os.unlink(original_file.name)

		self.assertFalse(os.path.exists(original_file.name))

		saved_file = tempfile.NamedTemporaryFile(delete=False)

		try:
			save_file_from_base64string(
				file_bytes_base64string=file_bytes_base64string,
				file_path=saved_file.name
			)

			with open(saved_file.name, "r") as file_handle:
				actual_file_contents = file_handle.readlines()

			self.assertEqual(expected_file_contents, actual_file_contents)
		finally:
			saved_file.close()
			os.unlink(saved_file.name)
