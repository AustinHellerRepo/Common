from __future__ import annotations
import unittest
from datetime import datetime
from src.austin_heller_repo.common import SubprocessWrapper, ElapsedTime


class SubprocessWrapperTest(unittest.TestCase):

	def test_initialize(self):

		subprocess_wrapper = SubprocessWrapper(
			command=None,
			arguments=None
		)

		self.assertIsNotNone(subprocess_wrapper)

	def test_basic_script(self):

		subprocess_wrapper = SubprocessWrapper(
			command="sh",
			arguments=["./subprocess_wrapper/basic_script.sh"]
		)

		exit_code, output = subprocess_wrapper.run()

		self.assertEqual(0, exit_code)
		self.assertEqual("Hello World\n", output)

	def test_delayed_by_script(self):

		subprocess_wrapper = SubprocessWrapper(
			command="sh",
			arguments=["./subprocess_wrapper/delay_three_seconds.sh"]
		)

		with ElapsedTime() as elapsed_time:
			exit_code, output = subprocess_wrapper.run()

		self.assertGreater(elapsed_time.get_time_seconds(), 3)
		self.assertEqual(0, exit_code)
		self.assertEqual("", output)
