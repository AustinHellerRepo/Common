import sys, os
#sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

try:
	from austin_heller_repo.common import split_repeat, copy_to_clipboard, paste_from_clipboard, IterationTypeEnum
except ImportError:
	try:
		from .src.austin_heller_repo.common import split_repeat, copy_to_clipboard, paste_from_clipboard, IterationTypeEnum
	except ImportError:
		try:
			from ..src.austin_heller_repo.common import split_repeat, copy_to_clipboard, paste_from_clipboard, IterationTypeEnum
		except ImportError:
			try:
				from ...src.austin_heller_repo.common import split_repeat, copy_to_clipboard, paste_from_clipboard, IterationTypeEnum
			except ImportError:
				from ....src.austin_heller_repo.common import split_repeat, copy_to_clipboard, paste_from_clipboard, IterationTypeEnum

import sys

delimiter = None  # type: str
format = None  # type: str
iteration_type = None  # type: IterationTypeEnum
repetition_total = None  # type: int

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

original_text = paste_from_clipboard()
formatted_text = split_repeat(
	text=original_text,
	delimiter=delimiter,
	format=format,
	iteration_type=iteration_type,
	repetition_total=repetition_total
)
copy_to_clipboard(
	text=formatted_text
)
