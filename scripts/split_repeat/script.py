try:
	from src.austin_heller_repo.common import split_repeat, copy_to_clipboard, paste_from_clipboard, IterationTypeEnum
except ImportError:
	from austin_heller_repo.common import split_repeat, copy_to_clipboard, paste_from_clipboard, IterationTypeEnum

import sys
from typing import List

delimiter = None  # type: str
format = None  # type: str
iteration_type = None  # type: IterationTypeEnum
repetition_total = None  # type: int

is_run_expected = True

for argument_index in range(len(sys.argv)):
	if argument_index != 0:
		if sys.argv[argument_index] == "-d":
			argument_index += 1
			delimiter = sys.argv[argument_index]
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
		elif sys.argv[argument_index] == "--help":
			print(f"Standard:")
			print(f"split_repeat -d [delimiter] -f [format] -stutter [repetition total]")
			print(f"split_repeat -d [delimiter] -f [format] -cycle [repetition total]")
			print(f"Examples:")
			print(f"split_repeat -d \",\" -f \"info for {{x}}: {{x}}\\n\" -stutter 2")
			print(f"split_repeat -d \",\" -f \"the first item is {{x}} and the second item is {{x}}. That was {{x}} and {{x}}.\" -loop 2")
			is_run_expected = False
		elif sys.argv[argument_index] == "--version":
			print(f"split_repeat: Version 0.0.1")
			is_run_expected = False

if is_run_expected:
	original_text = paste_from_clipboard()
	print(f"original_text: {original_text}")

	escaped_format_list = []  # type: List[str]
	is_escaped = False
	for character in format:
		if is_escaped:
			if character == "n":
				escaped_format_list.append("\n")
			elif character == "t":
				escaped_format_list.append("\t")
			else:
				escaped_format_list.append(character)
			is_escaped = False
		else:
			if character == "\\":
				is_escaped = True
			else:
				escaped_format_list.append(character)
	escaped_format = "".join(escaped_format_list)
	print(f"escaped_format: {escaped_format}")

	formatted_text = split_repeat(
		text=original_text,
		delimiter=delimiter,
		format=escaped_format,
		iteration_type=iteration_type,
		repetition_total=repetition_total
	)
	print(f"formatted_text: {formatted_text}")
	copy_to_clipboard(
		text=formatted_text
	)
