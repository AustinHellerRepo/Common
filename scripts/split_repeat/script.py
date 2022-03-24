try:
	from src.austin_heller_repo.common import split_repeat, IterationTypeEnum
except ImportError:
	from austin_heller_repo.common import split_repeat, IterationTypeEnum

import sys
from typing import List
import pyperclip

delimiter = None  # type: str
is_regex = None  # type: bool
format = None  # type: str
iteration_type = None  # type: IterationTypeEnum
repetition_total = None  # type: int
is_debug = False

is_run_expected = True

for argument_index in range(len(sys.argv)):
	if argument_index != 0:
		if sys.argv[argument_index] == "-d":
			argument_index += 1
			delimiter = sys.argv[argument_index]
			is_regex = False
		elif sys.argv[argument_index] == "-dr":
			argument_index += 1
			delimiter = sys.argv[argument_index]
			is_regex = True
		elif sys.argv[argument_index] == "-f":
			argument_index += 1
			format = sys.argv[argument_index]
		elif sys.argv[argument_index] == "-stutter":
			iteration_type = IterationTypeEnum.Stutter
			argument_index += 1
			repetition_total = int(sys.argv[argument_index])
		elif sys.argv[argument_index] == "-cycle":
			iteration_type = IterationTypeEnum.Cycle
			argument_index += 1
			repetition_total = int(sys.argv[argument_index])
		elif sys.argv[argument_index] == "--help" or sys.argv[argument_index] == "-h":
			print(f"Copy the text you want to format into your clipboard and then run the command.")
			print(f"Standard:")
			print(f"sr -d [delimiter] -f [format] -stutter [repetition total]")
			print(f"sr -d [delimiter] -f [format] -cycle [repetition total]")
			print(f"sr -dr [delimiter as regex] -f [format] -stutter [repetition total]")
			print(f"sr -dr [delimiter as regex] -f [format] -cycle [repetition total]")
			print(f"Examples:")
			print(f"sr -d \",\" -f \"info for {{x}}: {{x}}\\n\" -stutter 2")
			print(f"sr -d \",\" -f \"the first item is {{x}} and the second item is {{x}}. That was {{x}} and {{x}}.\" -loop 2")
			print(f"sr -dr \": (str|int), \" -f \"\\t\\tself.__{{x}} = {{x}}\\n\" -stutter 2")
			is_run_expected = False
		elif sys.argv[argument_index] == "--version" or sys.argv[argument_index] == "-v":
			print(f"split_repeat: Version 0.0.1")
			is_run_expected = False
		elif sys.argv[argument_index] == "--debug":
			is_debug = True

if is_run_expected:
	original_text = pyperclip.paste()
	if is_debug:
		print(f"original_text: {original_text}")

	def escape_text(*, text) -> str:
		escaped_text_list = []  # type: List[str]
		is_escaped = False
		for character in text:
			if is_escaped:
				if character == "n":
					escaped_text_list.append("\n")
				elif character == "t":
					escaped_text_list.append("\t")
				else:
					escaped_text_list.append(character)
				is_escaped = False
			else:
				if character == "\\":
					is_escaped = True
				else:
					escaped_text_list.append(character)
		return "".join(escaped_text_list)

	# escape the format
	escaped_format = escape_text(
		text=format
	)
	if is_debug:
		print(f"escaped_format: {escaped_format}")

	# escape the delimiter
	escaped_delimiter = escape_text(
		text=delimiter
	)
	if is_debug:
		print(f"escaped_delimiter: {escaped_delimiter}")

	formatted_text = split_repeat(
		text=original_text,
		delimiter=escaped_delimiter,
		is_delimiter_regex=is_regex,
		format=escaped_format,
		iteration_type=iteration_type,
		repetition_total=repetition_total
	)
	if is_debug:
		print(f"formatted_text: {formatted_text}")
	pyperclip.copy(formatted_text)
	if is_debug:
		print(f"Copied to clipboard.")
