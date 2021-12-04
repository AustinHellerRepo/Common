import unittest
from src.austin_heller_repo.common import StringEnum


class ExampleStringEnum(StringEnum):
	FirstValue = "first_value"
	SecondValue = "second_value"


class StringEnumTest(unittest.TestCase):

	def test_initialize(self):

		string_enum = ExampleStringEnum.FirstValue

		self.assertIsNotNone(string_enum)

	def test_get_list(self):

		string_enum_list = ExampleStringEnum.get_list()

		self.assertEqual(2, len(string_enum_list))
		self.assertEqual(ExampleStringEnum.FirstValue.value, string_enum_list[0])
		self.assertEqual(ExampleStringEnum.SecondValue.value, string_enum_list[1])
