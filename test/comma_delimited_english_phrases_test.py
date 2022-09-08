import unittest
import uuid
from src.austin_heller_repo.common import get_comma_delimited_english_phrases
import timeit
import statistics


class CommaDelimitedEnglishPhrasesTest(unittest.TestCase):

    def test_none(self):
        default = str(uuid.uuid4())
        actual_output = get_comma_delimited_english_phrases(
            phrases=[],
            final_combinator=str(uuid.uuid4()),
            default=default
        )
        self.assertEqual(default, actual_output)

    def test_single(self):
        single_phrase = str(uuid.uuid4())
        actual_output = get_comma_delimited_english_phrases(
            phrases=[
                single_phrase
            ],
            final_combinator=str(uuid.uuid4()),
            default=str(uuid.uuid4())
        )
        self.assertEqual(single_phrase, actual_output)

    def test_double(self):
        first_phrase = str(uuid.uuid4())
        final_combinator = str(uuid.uuid4())
        second_phrase = str(uuid.uuid4())
        actual_output = get_comma_delimited_english_phrases(
            phrases=[
                first_phrase,
                second_phrase
            ],
            final_combinator=final_combinator,
            default=str(uuid.uuid4())
        )
        self.assertEqual(f"{first_phrase} {final_combinator} {second_phrase}", actual_output)

    def test_three_or_more(self):
        for index in range(100):
            phrases_total = index + 3
            phrases = []
            for phrases_index in range(phrases_total):
                phrases.append(str(uuid.uuid4()))
            final_combinator = str(uuid.uuid4())
            actual_output = get_comma_delimited_english_phrases(
                phrases=phrases,
                final_combinator=final_combinator,
                default=str(uuid.uuid4())
            )
            expected_output = "".join([(", " if phrase_index != 0 else "") + (final_combinator if phrase_index + 1 == phrases_total else "") + phrase for phrase_index, phrase in enumerate(phrases)])
            self.assertEqual(expected_output, actual_output)

    def test_timing_inline(self):
        import_module = "import uuid"
        code = """
def test():
    for index in range(10):
        phrases_total = index + 3
        phrases = []
        for phrases_index in range(phrases_total):
            phrases.append(str(uuid.uuid4()))
        final_combinator = str(uuid.uuid4())
        expected_output = "".join([(", " if phrase_index != 0 else "") + (final_combinator if phrase_index + 1 == phrases_total else "") + phrase for phrase_index, phrase in enumerate(phrases)])
        """
        print(f"test_timing_inline: {statistics.mean(timeit.repeat(stmt=code, setup=import_module, repeat=100))}")

    def test_timing_function(self):
        import_module = "import io; import uuid"
        code = """
def test():
    for index in range(10):
        phrases_total = index + 3
        phrases = []
        for phrases_index in range(phrases_total):
            phrases.append(str(uuid.uuid4()))
        final_combinator = str(uuid.uuid4())
        writer = io.StringIO()
        for phrase_index, phrase in enumerate(phrases):
            if phrase_index != 0:
                writer.write(", ")
            if phrase_index + 1 == phrases_total:
                writer.write(final_combinator)
            writer.write(phrase)
        actual_output = writer.getvalue()
        """
        print(f"test_timing_function: {statistics.mean(timeit.repeat(stmt=code, setup=import_module, repeat=100))}")
