from __future__ import annotations
import re
from src.austin_heller_repo.common import get_delimited_string_regex_pattern_frequencies
import unittest


class CommonRegexTest(unittest.TestCase):

    def test_basic_regex(self):

        source = "test here a b c d\n" \
                 "something here a b f g\n" \
                 "another here a b\n" \
                 "something here x y"

        total_per_regex = {k: v for k, v in sorted(get_delimited_string_regex_pattern_frequencies(
            text=source
        ).items(), key=lambda item: item[1])}

        print(f"total_per_regex: {total_per_regex}")
        print(f"len(total_per_regex): {len(total_per_regex)}")

        self.assertEqual(47, len(total_per_regex))

    def test_escaped_regex_a_hyphen_z(self):

        source = "test (here) a-z c d\n" \
                 "something (here) a-z f g\n" \
                 "another (here) x y a-z\n" \
                 "something (here) x y"

        total_per_regex = {k: v for k, v in reversed(sorted(get_delimited_string_regex_pattern_frequencies(
            text=source
        ).items(), key=lambda item: item[1]))}

        print(f"total_per_regex: {total_per_regex}")

        self.assertEqual(4, total_per_regex["\\(here\\)"])

        regex_pattern = list(total_per_regex.keys())[1]

        print(f"regex_pattern: {regex_pattern}")

        compiled_regex_pattern = re.compile(regex_pattern)

        match = compiled_regex_pattern.search(source)

        print(f"match: {match}")

        self.assertEqual((12, 15), match.span())

    def test_escaped_regex_meta_regex_word_anchor(self):

        source = "x cat x \\<cat\\> \\<cat\\> \\<cat\\> \\<cat\\>\n"

        total_per_regex = {k: v for k, v in reversed(sorted(get_delimited_string_regex_pattern_frequencies(
            text=source
        ).items(), key=lambda item: item[1]))}

        print(f"total_per_regex: {total_per_regex}")

        regex_pattern = list(total_per_regex.keys())[0]

        print(f"regex_pattern: {regex_pattern}")

        compiled_regex_pattern = re.compile(regex_pattern)

        match = compiled_regex_pattern.search(source)

        print(f"match: {match}")

        self.assertEqual((8, 15), match.span())

    def test_escaped_regex_period(self):

        source = "x cat x . . . . .\n"

        total_per_regex = {k: v for k, v in reversed(sorted(get_delimited_string_regex_pattern_frequencies(
            text=source
        ).items(), key=lambda item: item[1]))}

        print(f"total_per_regex: {total_per_regex}")

        regex_pattern = list(total_per_regex.keys())[0]

        print(f"regex_pattern: {regex_pattern}")

        compiled_regex_pattern = re.compile(regex_pattern)

        match = compiled_regex_pattern.search(source)

        print(f"match: {match}")

        self.assertEqual((8, 9), match.span())
