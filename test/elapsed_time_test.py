from __future__ import annotations
import unittest
import time
from datetime import datetime
from src.austin_heller_repo.common import ElapsedTimer, ElapsedTimerMessageManager


class ElapsedTimeTest(unittest.TestCase):

	def test_one_second(self):
		for index in range(10):
			elapsed_timer = ElapsedTimer()
			time.sleep(1.0)
			print(f"{datetime.utcnow()}: test: {elapsed_timer.get_time_seconds()}")

	def test_tenth_second(self):
		for index in range(10):
			elapsed_timer = ElapsedTimer()
			time.sleep(0.1)
			print(f"{datetime.utcnow()}: test: {elapsed_timer.get_time_seconds()}")

	def test_hundredth_second(self):
		for index in range(10):
			elapsed_timer = ElapsedTimer()
			time.sleep(0.01)
			print(f"{datetime.utcnow()}: test: {elapsed_timer.get_time_seconds()}")

	def test_thousandth_second(self):
		for index in range(10):
			elapsed_timer = ElapsedTimer()
			time.sleep(0.001)
			print(f"{datetime.utcnow()}: test: {elapsed_timer.get_time_seconds()}")

	def test_zero_second(self):
		for index in range(10):
			elapsed_timer = ElapsedTimer()
			time.sleep(0)
			print(f"{datetime.utcnow()}: test: {elapsed_timer.get_time_seconds()}")

	def test_message_manager(self):
		elapsed_timer_message_manager = ElapsedTimerMessageManager(
			include_datetime_prefix=True,
			include_stack=True
		)
		time.sleep(0.1)
		elapsed_timer_message_manager.print("test")
		time.sleep(0.1)
		elapsed_timer_message_manager.print("test")

	def test_message_manager_with_depth(self):

		def test_method():
			elapsed_timer_message_manager = ElapsedTimerMessageManager(
				include_datetime_prefix=True,
				include_stack=True,
				stack_offset=1
			)
			time.sleep(0.1)
			elapsed_timer_message_manager.print("test")
			time.sleep(0.1)
			elapsed_timer_message_manager.print("test")

		test_method()

	def test_message_manager_with_depth_override(self):

		def test_method():
			elapsed_timer_message_manager = ElapsedTimerMessageManager(
				include_datetime_prefix=True,
				include_stack=True,
				stack_offset=1
			)
			time.sleep(0.1)
			elapsed_timer_message_manager.print("test", 0)
			time.sleep(0.1)
			elapsed_timer_message_manager.print("test", 2)

		test_method()
