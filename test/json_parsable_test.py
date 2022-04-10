from __future__ import annotations
import unittest
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple
import uuid
from src.austin_heller_repo.common import JsonParsable, StringEnum, JsonParsableException


class ModuleInputTypeEnum(StringEnum):
	Image = "image"
	TensorCacheElement = "tensor_cache_element"


class ModuleInputJsonParsable(JsonParsable, ABC):

	def __init__(self):
		super().__init__()

		pass

	@classmethod
	def get_json_parsable_type_dictionary_key(cls) -> str:
		return "__module_input_type"


class ImageModuleInputJsonParsable(ModuleInputJsonParsable):

	def __init__(self, *, image_bytes_base64string: str, image_extension: str):
		super().__init__()

		self.__image_bytes_base64string = image_bytes_base64string
		self.__image_extension = image_extension

	def get_image_bytes_base64string(self) -> str:
		return self.__image_bytes_base64string

	def get_image_extension(self) -> str:
		return self.__image_extension

	@classmethod
	def get_json_parsable_type(cls) -> StringEnum:
		return ModuleInputTypeEnum.Image

	def to_json(self) -> Dict:
		json_dict = super().to_json()
		json_dict["image_bytes_base64string"] = self.__image_bytes_base64string
		json_dict["image_extension"] = self.__image_extension
		return json_dict


class TensorCacheElementModuleInputJsonParsable(ModuleInputJsonParsable):

	def __init__(self, *, tensor_data: List):
		super().__init__()

		self.__tensor_data = tensor_data

	def get_tensor_data(self) -> List:
		return self.__tensor_data

	@classmethod
	def get_json_parsable_type(cls) -> StringEnum:
		return ModuleInputTypeEnum.TensorCacheElement

	def to_json(self) -> Dict:
		json_dict = super().to_json()
		json_dict["tensor_data"] = self.__tensor_data
		return json_dict


class JsonParsableTest(unittest.TestCase):

	def test_parse_json(self):

		image_bytes_base64string = str(uuid.uuid4())
		image_extension = str(uuid.uuid4())
		image_module_input_json_parsable = ImageModuleInputJsonParsable(
			image_bytes_base64string=image_bytes_base64string,
			image_extension=image_extension
		)
		actual_json_dict = image_module_input_json_parsable.to_json()
		expected_json_dict = {
			"__module_input_type": ModuleInputTypeEnum.Image.value,
			"image_bytes_base64string": image_bytes_base64string,
			"image_extension": image_extension
		}

		self.assertEqual(expected_json_dict, actual_json_dict)

		with self.assertRaises(JsonParsableException):
			actual_object = JsonParsable.parse_json(
				json_dict=actual_json_dict
			)  # type: ImageModuleInputJsonParsable

		actual_object = ModuleInputJsonParsable.parse_json(
			json_dict=actual_json_dict
		)  # type: ImageModuleInputJsonParsable

		self.assertEqual(image_bytes_base64string, actual_object.get_image_bytes_base64string())
		self.assertEqual(image_extension, actual_object.get_image_extension())
		self.assertTrue(isinstance(actual_object, ImageModuleInputJsonParsable))

	def test_invalid_json_type(self):
		image_bytes_base64string = str(uuid.uuid4())
		image_extension = str(uuid.uuid4())
		image_module_input_json_parsable = ImageModuleInputJsonParsable(
			image_bytes_base64string=image_bytes_base64string,
			image_extension=image_extension
		)
		actual_json_dict = image_module_input_json_parsable.to_json()
		actual_json_dict[ModuleInputJsonParsable.get_json_parsable_type_dictionary_key()] = str(uuid.uuid4())

		with self.assertRaises(JsonParsableException):
			test = ModuleInputJsonParsable.parse_json(
				json_dict=actual_json_dict
			)

	def test_parse_exact_json_type(self):
		image_bytes_base64string = str(uuid.uuid4())
		image_extension = str(uuid.uuid4())
		image_module_input_json_parsable = ImageModuleInputJsonParsable(
			image_bytes_base64string=image_bytes_base64string,
			image_extension=image_extension
		)
		actual_json_dict = image_module_input_json_parsable.to_json()

		actual_object = ImageModuleInputJsonParsable.parse_json(
			json_dict=actual_json_dict
		)

		self.assertEqual(image_bytes_base64string, actual_object.get_image_bytes_base64string())
		self.assertEqual(image_extension, actual_object.get_image_extension())
		self.assertTrue(isinstance(actual_object, ImageModuleInputJsonParsable))

	def test_parse_exact_json_type_wrong_type(self):
		image_bytes_base64string = str(uuid.uuid4())
		image_extension = str(uuid.uuid4())
		image_module_input_json_parsable = ImageModuleInputJsonParsable(
			image_bytes_base64string=image_bytes_base64string,
			image_extension=image_extension
		)
		actual_json_dict = image_module_input_json_parsable.to_json()
		actual_json_dict[ModuleInputJsonParsable.get_json_parsable_type_dictionary_key()] = str(uuid.uuid4())

		with self.assertRaises(JsonParsableException):
			actual_object = TensorCacheElementModuleInputJsonParsable.parse_json(
				json_dict=actual_json_dict
			)
