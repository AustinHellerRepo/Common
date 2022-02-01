from __future__ import annotations
import unittest
import time
from datetime import datetime
from src.austin_heller_repo.common import ElapsedTime


class ElapsedTimeTest(unittest.TestCase):

	def test_one_second(self):
		for index in range(10):
			with ElapsedTime() as elapsed_time:
				time.sleep(1.0)
				print(f"{datetime.utcnow()}: test: {elapsed_time.get_time_seconds()}")

	def test_tenth_second(self):
		for index in range(10):
			with ElapsedTime() as elapsed_time:
				time.sleep(0.1)
				print(f"{datetime.utcnow()}: test: {elapsed_time.get_time_seconds()}")

	def test_hundredth_second(self):
		for index in range(10):
			with ElapsedTime() as elapsed_time:
				time.sleep(0.01)
				print(f"{datetime.utcnow()}: test: {elapsed_time.get_time_seconds()}")

	def test_thousandth_second(self):
		for index in range(10):
			with ElapsedTime() as elapsed_time:
				time.sleep(0.001)
				print(f"{datetime.utcnow()}: test: {elapsed_time.get_time_seconds()}")

	def test_zero_second(self):
		for index in range(10):
			with ElapsedTime() as elapsed_time:
				time.sleep(0)
				print(f"{datetime.utcnow()}: test: {elapsed_time.get_time_seconds()}")
