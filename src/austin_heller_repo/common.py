from __future__ import annotations
from enum import Enum
from typing import List, Tuple, Dict
from abc import ABC, abstractmethod
import hashlib
import json


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
