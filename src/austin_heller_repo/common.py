from __future__ import annotations
from enum import Enum
from typing import List, Tuple, Dict
from abc import ABC, abstractmethod
import hashlib
import json
from datetime import datetime, timedelta


class StringEnum(Enum):
	def __repr__(self):
		return f"<{self.__class__.__name__}.{self.name}>"

	@classmethod
	def get_list(cls) -> List[str]:
		enum_list = list(cls)
		string_list = []  # type: List[str]
		for enum_list_element in enum_list:
			string_list.append(enum_list_element.value)
		return string_list


class HostPointer():

	def __init__(self, *, host_address: str, host_port: int):

		self.__host_address = host_address
		self.__host_port = host_port

	def get_host_address(self) -> str:
		return self.__host_address

	def get_host_port(self) -> int:
		return self.__host_port


def static_init(cls):
	if getattr(cls, "static_init", None):
		cls.static_init()
	return cls


def hash_json_dict(*, json_dict: Dict) -> str:
	hash_instance = hashlib.sha256()
	encoded_json_dict = json.dumps(json_dict, sort_keys=True).encode()
	hash_instance.update(encoded_json_dict)
	return hash_instance.hexdigest()


class FloatReference():

	def __init__(self, *, value: float):

		self.__value = value

	def get(self) -> float:
		return self.__value

	def set(self, *, value: float):
		self.__value = value


class DateTimeDeltaCalculator():

	@staticmethod
	def get_calculated_time_delta(*, start_datetime: datetime, effective_seconds: float, now_datetime: datetime, time_delta: float) -> float:

		#	A
		#	|			|			|			|			|
		#   |			start		>			eff end		|
		#	|			|			|			|			|
		#	td start	<			<			<			now
		#	|			|			|			|			|
		#	|			|===================================|

		#	B
		#	|			|			|			|			|
		#   start		>			>			>			eff end
		#	|			|			|			|			|
		#	|			td start	<			now			|
		#	|			|			|			|			|
		#	|===================================|			|

		#	C
		#	|			|			|			|			|
		#   |			start       >			>			eff end
		#	|			|			|			|			|
		#	td start	<			now			|			|
		#	|			|			|			|			|
		#	|			|===========|			|			|

		#	D
		#	|			|			|			|			|
		#   start       >			>			eff end		|
		#	|			|			|			|			|
		#	|			|			td start	<			now
		#	|			|			|			|			|
		#	|===============================================|

		between_now_and_start_seconds = (now_datetime - start_datetime).total_seconds()
		if between_now_and_start_seconds < 0:
			return 0
		end_datetime = start_datetime + timedelta(seconds=effective_seconds)
		previous_datetime = now_datetime - timedelta(seconds=time_delta)
		if previous_datetime > end_datetime:
			return 0
		if now_datetime > end_datetime:
			if previous_datetime > start_datetime:
				# D
				return (end_datetime - previous_datetime).total_seconds()
			else:
				# A
				return effective_seconds
		else:
			if previous_datetime > start_datetime:
				# B
				return time_delta
			else:
				# C
				return between_now_and_start_seconds

		# TODO convert this to use three time spans (seconds) instead of four dates
		if now_datetime < start_datetime:
			return 0
		between_now_and_start_seconds = (now_datetime - start_datetime).total_seconds()
		if effective_seconds + time_delta < between_now_and_start_seconds:
			return 0
		if between_now_and_start_seconds < time_delta:
			return between_now_and_start_seconds
		#if
		after_effective_in_time_delta_seconds = (between_now_and_start_seconds - effective_seconds)
		if after_effective_in_time_delta_seconds > 0:
			# now comes after effective seconds ends
			raise NotImplementedError()
		else:
			# now exists within
			raise NotImplementedError()
