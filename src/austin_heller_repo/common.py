from __future__ import annotations
from enum import Enum
from typing import List, Tuple, Dict


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
