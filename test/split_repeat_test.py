from __future__ import annotations
import unittest
import uuid
from src.austin_heller_repo.common import split_repeat, IterationTypeEnum


class SplitRepeatTest(unittest.TestCase):

	def test_exact_repeat_stutter(self):

		expected_output = str(uuid.uuid4())
		actual_output = split_repeat(
			text=expected_output,
			delimiter="",
			format="{x}",
			iteration_type=IterationTypeEnum.Stutter,
			repetition_total=1
		)
		self.assertEqual(expected_output, actual_output)

	def test_exact_repeat_cycle(self):

		expected_output = str(uuid.uuid4())
		actual_output = split_repeat(
			text=expected_output,
			delimiter="",
			format="{x}",
			iteration_type=IterationTypeEnum.Cycle,
			repetition_total=1
		)
		self.assertEqual(expected_output, actual_output)

	def test_every_other_stutter(self):

		expected_output = f"{str(uuid.uuid4())},{str(uuid.uuid4())}"
		actual_output = split_repeat(
			text=expected_output,
			delimiter=",",
			format="{x},{x}",
			iteration_type=IterationTypeEnum.Stutter,
			repetition_total=1
		)
		self.assertEqual(expected_output, actual_output)

	def test_every_other_cycle(self):

		expected_output = f"{str(uuid.uuid4())},{str(uuid.uuid4())}"
		actual_output = split_repeat(
			text=expected_output,
			delimiter=",",
			format="{x},{x}",
			iteration_type=IterationTypeEnum.Cycle,
			repetition_total=1
		)
		self.assertEqual(expected_output, actual_output)

	def test_actual_problem_001(self):

		text = "open_translator: str," \
			"login: str," \
			"create_account: str," \
			"coins: str," \
			"translate: str," \
			"use_one_coin_per_minute: str," \
			"volunteer: str," \
			"get_free_coins: str," \
			"quiz: str," \
			"english: str," \
			"spanish: str," \
			"haitian_creole: str," \
			"buy_coins: str," \
			"sign_in_with_google: str," \
			"languages_that_you_currently_know: str," \
			"save: str," \
			"cancel: str," \
			"thank_you_for_signing_up: str," \
			"when_you_get_coins_you_are_helping_make_this_app_better: str," \
			"ten_minutes: str," \
			"ten_coins_for_one_dollar: str," \
			"thirty_minutes: str," \
			"thirty_coins_for_three_dollars: str," \
			"draw_rectangles_over_words: str," \
			"copy_letters_from_word: str," \
			"translate_sentence: str," \
			"i_dont_know: str," \
			"not_a_word: str," \
			"not_a_sentence: str," \
			"does_the_rectangle_perfectly_surround_exactly_one_word: str," \
			"yes: str," \
			"no: str," \
			"do_these_two_words_match: str," \
			"which_translation_makes_the_most_sense: str," \
			"neither: str," \
			"can_read_statement"

		result = split_repeat(
			text=text,
			delimiter=": str,",
			format="\tdef get_{x}(self) -> str:\n\t\treturn self.__{x}\n\n",
			iteration_type=IterationTypeEnum.Stutter,
			repetition_total=2
		)

		print(f"result: {result}")
