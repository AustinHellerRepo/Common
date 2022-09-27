from __future__ import annotations
import os
from enum import Enum
from typing import List, Tuple, Dict, Callable, Any, Deque, Type, Iterator, Iterable
from abc import ABC, abstractmethod
import hashlib
import json
from datetime import datetime, timedelta, date
import time
from threading import Semaphore, Lock
from collections import deque
from itertools import cycle, chain, repeat, groupby
from timeit import default_timer
import subprocess
import re
import uuid
import inspect
import shutil
import random
import base64
import io
import pathlib


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


class JsonInterchangeable(ABC):

    @abstractmethod
    def to_json(self) -> Dict:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def parse_json(cls, *, json_dict: Dict) -> JsonInterchangeable:
        raise NotImplementedError()


class HostPointer(JsonInterchangeable):

    def __init__(self, *, host_address: str, host_port: int):

        self.__host_address = host_address
        self.__host_port = host_port

    def get_host_address(self) -> str:
        return self.__host_address

    def get_host_port(self) -> int:
        return self.__host_port

    def to_json(self) -> Dict:
        return {
            "host_address": self.__host_address,
            "host_port": self.__host_port
        }

    @staticmethod
    def parse_json(*, json_dict: Dict) -> HostPointer:
        return HostPointer(
            host_address=json_dict["host_address"],
            host_port=json_dict["host_port"]
        )


def static_init(cls):
    if getattr(cls, "static_init", None):
        cls.static_init()
    return cls


def hash_json_dict(*, json_dict: Dict) -> str:
    hash_instance = hashlib.sha256()
    encoded_json_dict = json.dumps(json_dict, sort_keys=True).encode()
    hash_instance.update(encoded_json_dict)
    return hash_instance.hexdigest()


class FloatReference():

    def __init__(self, *, value: float):
        self.__value = value

    def get(self) -> float:
        return self.__value

    def set(self, *, value: float):
        self.__value = value


class BooleanReference():

    def __init__(self, *, value: bool):
        self.__value = value

    def get(self) -> bool:
        return self.__value

    def set(self, *, value: bool):
        self.__value = value


class DateTimeDeltaCalculator():

    @staticmethod
    def get_calculated_time_delta(*, start_datetime: datetime, effective_seconds: float, now_datetime: datetime, time_delta: float) -> float:

        #	A
        #	|			|			|			|			|
        #   |			start		>			eff end		|
        #	|			|			|			|			|
        #	td start	<			<			<			now
        #	|			|			|			|			|
        #	|			|===================================|

        #	B
        #	|			|			|			|			|
        #   start		>			>			>			eff end
        #	|			|			|			|			|
        #	|			td start	<			now			|
        #	|			|			|			|			|
        #	|===================================|			|

        #	C
        #	|			|			|			|			|
        #   |			start       >			>			eff end
        #	|			|			|			|			|
        #	td start	<			now			|			|
        #	|			|			|			|			|
        #	|			|===========|			|			|

        #	D
        #	|			|			|			|			|
        #   start       >			>			eff end		|
        #	|			|			|			|			|
        #	|			|			td start	<			now
        #	|			|			|			|			|
        #	|===============================================|

        between_now_and_start_seconds = (now_datetime - start_datetime).total_seconds()
        if between_now_and_start_seconds < 0:
            return 0
        end_datetime = start_datetime + timedelta(seconds=effective_seconds)
        previous_datetime = now_datetime - timedelta(seconds=time_delta)
        if previous_datetime > end_datetime:
            return 0
        if now_datetime > end_datetime:
            if previous_datetime > start_datetime:
                # D
                return (end_datetime - previous_datetime).total_seconds()
            else:
                # A
                return effective_seconds
        else:
            if previous_datetime > start_datetime:
                # B
                return time_delta
            else:
                # C
                return between_now_and_start_seconds

        # TODO convert this to use three time spans (seconds) instead of four dates
        if now_datetime < start_datetime:
            return 0
        between_now_and_start_seconds = (now_datetime - start_datetime).total_seconds()
        if effective_seconds + time_delta < between_now_and_start_seconds:
            return 0
        if between_now_and_start_seconds < time_delta:
            return between_now_and_start_seconds
        #if
        after_effective_in_time_delta_seconds = (between_now_and_start_seconds - effective_seconds)
        if after_effective_in_time_delta_seconds > 0:
            # now comes after effective seconds ends
            raise NotImplementedError()
        else:
            # now exists within
            raise NotImplementedError()


class SingleDependentDependencyManager():

    def __init__(self, *, on_dependent_dependency_satisfied_callback: Callable[[Any, Any, Any], None], is_dependency_reusable: bool):

        self.__on_dependent_dependency_satisfied_callback = on_dependent_dependency_satisfied_callback
        self.__is_dependency_reusable = is_dependency_reusable

        # this contains a list of dependents are are waiting for the same key as the dependency_cache
        self.__dependents_per_key = {}  # type: Dict[Any, Deque[Any]]
        # this contains each dependencies that a dependent may need
        self.__dependencies_per_key = {}  # type: Dict[Any, Deque[Any]]
        self.__semaphore = Semaphore()

    def __get_dependent_dependency_pairs(self, *, key: Any) -> List[Tuple[Any, Any]]:
        pairs = []  # type: List[Tuple[Any, Any]]
        if key in self.__dependents_per_key and key in self.__dependencies_per_key:
            while self.__dependents_per_key[key] and self.__dependencies_per_key[key]:
                dependent = self.__dependents_per_key[key].popleft()
                dependency = self.__dependencies_per_key[key].popleft()
                pairs.append((dependent, dependency))
                if self.__is_dependency_reusable:
                    self.__dependencies_per_key[key].append(dependency)
            if not self.__dependents_per_key[key]:
                del self.__dependents_per_key[key]
            if not self.__dependencies_per_key[key]:
                del self.__dependencies_per_key[key]
        return pairs

    def add_dependency(self, *, key: Any, dependency: Any):

        self.__semaphore.acquire()
        try:
            if key not in self.__dependencies_per_key:
                self.__dependencies_per_key[key] = deque()
            self.__dependencies_per_key[key].append(dependency)

            pairs = self.__get_dependent_dependency_pairs(
                key=key
            )
        finally:
            self.__semaphore.release()

        if pairs:
            for pair in pairs:
                self.__on_dependent_dependency_satisfied_callback(*pair, key)

    def add_dependent(self, *, dependent: Any, key: Any):

        self.__semaphore.acquire()
        try:
            if key not in self.__dependents_per_key:
                self.__dependents_per_key[key] = deque()
            self.__dependents_per_key[key].append(dependent)

            pairs = self.__get_dependent_dependency_pairs(
                key=key
            )
        finally:
            self.__semaphore.release()

        if pairs:
            for pair in pairs:
                self.__on_dependent_dependency_satisfied_callback(*pair, key)


class AggregateDependentDependencyManager():

    def __init__(self, *, on_dependent_dependency_satisfied_callback: Callable[[Any, List[Tuple[Any, Any]]], None]):

        self.__on_dependent_dependency_satisfied_callback = on_dependent_dependency_satisfied_callback

        self.__expected_dependencies_total_per_dependent = {}  # type: Dict[Any, int]
        self.__dependency_and_key_pair_per_dependent = {}  # type: Dict[Any, List[Tuple[Any, Any]]]
        self.__dependencies_per_dependent_semaphore = Semaphore()
        self.__single_dependent_dependency_manager_per_is_reusable = {}  # type: Dict[bool, SingleDependentDependencyManager]

        self.__initialize()

    def __initialize(self):
        for is_reusable in [True, False]:
            self.__single_dependent_dependency_manager_per_is_reusable[is_reusable] = SingleDependentDependencyManager(
                on_dependent_dependency_satisfied_callback=self.__single_dependent_dependency_manager_on_dependent_dependency_satisfied_callback,
                is_dependency_reusable=is_reusable
            )

    def __single_dependent_dependency_manager_on_dependent_dependency_satisfied_callback(self, dependent: Any, dependency: Any, key: Any):
        self.__dependency_and_key_pair_per_dependent[dependent].append((dependency, key))
        if len(self.__dependency_and_key_pair_per_dependent[dependent]) == self.__expected_dependencies_total_per_dependent[dependent]:
            self.__on_dependent_dependency_satisfied_callback(dependent, self.__dependency_and_key_pair_per_dependent[dependent])
            del self.__dependency_and_key_pair_per_dependent[dependent]
            del self.__expected_dependencies_total_per_dependent[dependent]

    def add_dependent(self, *, dependent: Any, reusable_keys: List[Any], nonreusable_keys: List[Any]):
        self.__dependencies_per_dependent_semaphore.acquire()
        try:
            self.__expected_dependencies_total_per_dependent[dependent] = len(reusable_keys) + len(nonreusable_keys)
            self.__dependency_and_key_pair_per_dependent[dependent] = []
            for dependency_key, is_reusable in chain(zip(reusable_keys, cycle([True])), zip(nonreusable_keys, cycle([False]))):
                self.__single_dependent_dependency_manager_per_is_reusable[is_reusable].add_dependent(
                    key=dependency_key,
                    dependent=dependent
                )
        finally:
            self.__dependencies_per_dependent_semaphore.release()

    def add_dependency(self, *, key: Any, dependency: Any, is_reusable: bool):
        self.__dependencies_per_dependent_semaphore.acquire()
        try:
            self.__single_dependent_dependency_manager_per_is_reusable[is_reusable].add_dependency(
                key=key,
                dependency=dependency
            )
        finally:
            self.__dependencies_per_dependent_semaphore.release()


class ElapsedTimer():

    def __init__(self):

        # TODO add ability to specify formats, etc.

        self.__start_timer_value = default_timer()

    def get_time_seconds(self) -> float:
        next_timer_value = default_timer()
        time_seconds, self.__start_timer_value = next_timer_value - self.__start_timer_value, next_timer_value
        return time_seconds

    def peek_time_seconds(self) -> float:
        return (default_timer() - self.__start_timer_value)


class ElapsedTimerMessageManager():

    def __init__(self, *, include_datetime_prefix: bool, include_stack: bool, stack_offset: int = 0):

        self.__include_datetime_prefix = include_datetime_prefix
        self.__include_stack = include_stack
        self.__stack_offset = stack_offset

        self.__elapsed_timer = ElapsedTimer()
        self.__elapsed_seconds_total_per_message = {}  # type: Dict[str, int]

    def print(self, message: str, override_stack_offset: int = None):

        elapsed_seconds = self.__elapsed_timer.get_time_seconds()
        if message not in self.__elapsed_seconds_total_per_message:
            self.__elapsed_seconds_total_per_message[message] = 0
        self.__elapsed_seconds_total_per_message[message] += elapsed_seconds
        formatted_message = f"{str(datetime.utcnow()) + ': ' if self.__include_datetime_prefix else ''}{inspect.stack()[1 + (override_stack_offset if override_stack_offset is not None else self.__stack_offset)][3] + ': ' if self.__include_stack else ''}{elapsed_seconds}: {message}"
        print(formatted_message)

    def get_elapsed_seconds_total_per_message(self) -> Dict[str, int]:
        return self.__elapsed_seconds_total_per_message.copy()


DateFormat_Year_Month_Day_Hour_Minute_Second_Millisecond = "%Y-%m-%d %H:%M:%S.%f"


class SubprocessWrapper():

    def __init__(self, *, command: str, arguments: List[str]):

        self.__command = command
        self.__arguments = arguments

        self.__subprocess = None  # type: subprocess.Popen

    def run(self) -> Tuple[int, str]:

        formatted_command = [self.__command] + self.__arguments

        with subprocess.Popen(formatted_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as process_handle:
            self.__subprocess = process_handle
            process_handle.wait()
            standard_output = process_handle.stdout.read().decode()
            return_code = process_handle.returncode
        self.__subprocess = None

        return return_code, standard_output

    def kill(self):
        if self.__subprocess is not None:
            self.__subprocess.kill()


def is_directory_empty(*, directory_path: str) -> bool:
    with os.scandir(directory_path) as scan_dir:
        return not next(scan_dir, None)


def delete_directory_contents(directory_path: str):
    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)


class IterationTypeEnum(StringEnum):
    Stutter = "stutter"
    Cycle = "cycle"


def split_repeat(text: str, delimiter: str, is_delimiter_regex: bool, format: str, iteration_type: IterationTypeEnum, repetition_total: int) -> str:

    output_elements = []  # type: List[str]

    if delimiter == "" or delimiter is None:
        text_parts = [text]
    else:
        if is_delimiter_regex:
            delimiters = re.search(delimiter, text)
            if not delimiters:
                text_parts = [text]
            else:
                text_parts = []  # type: List[str]
                while delimiters:
                    found_delimiter = delimiters.group(0)
                    text_part = text[:text.index(found_delimiter)]
                    text_parts.append(text_part)
                    text = text[text.index(found_delimiter) + len(found_delimiter):]
                    delimiters = re.search(delimiter, text)
                if text != "":
                    text_parts.append(text)
        else:
            text_parts = text.split(delimiter)

    if iteration_type == IterationTypeEnum.Cycle:
        iterator = chain(*[x for x in repeat(text_parts, repetition_total)])
    elif iteration_type == IterationTypeEnum.Stutter:
        iterator = chain.from_iterable(repeat(x, repetition_total) for x in text_parts)
    else:
        raise Exception(f"Unexpected {IterationTypeEnum.__name__} value {iteration_type}.")

    iterator_elements = [x for x in iterator]
    iterator_elements_index = 0
    iterator_elements_total = len(iterator_elements)

    while iterator_elements_index < iterator_elements_total:
        is_escaped = False
        characters_total = len(format)
        character_index = 0
        while character_index < characters_total:
            character = format[character_index]
            if is_escaped:
                output_element = character
                is_escaped = False
            else:
                if character == "\\":
                    is_escaped = True
                else:
                    if character == "{":
                        # replacement object
                        if format[character_index:character_index+3] == "{x}":
                            is_at_least_one_replace_object = True
                            output_element = iterator_elements[iterator_elements_index]
                            iterator_elements_index += 1
                            character_index += 2
                        else:
                            raise Exception(f"Unexpected curly brace at index {character_index}.")
                    else:
                        output_element = character
            if not is_escaped:
                output_elements.append(output_element)

            character_index += 1

        if not is_at_least_one_replace_object:
            raise Exception(f"Failed to find any replacement objects in format: {format}")

    return "".join(output_elements)


def get_non_maximum_suppression_rectangles(*, rectangles: List[Tuple[float, float, float, float]], overlap_threshold: float) -> List[Tuple[float, float, float, float]]:

    if len(rectangles) == 0:
        return []
    else:

        areas = []  # type: List[float]
        for rectangle in rectangles:
            area = rectangle[2] * rectangle[3]
            areas.append(area)

        indexes = list(range(len(areas)))
        for index, rectangle in enumerate(rectangles):

            temp_indexes = [i for i in indexes if i != index]

            for temp_index in temp_indexes:
                temp_x1 = max(rectangle[0], rectangles[temp_index][0])
                temp_y1 = max(rectangle[1], rectangles[temp_index][1])
                temp_x2 = min(rectangle[0] + rectangle[2], rectangles[temp_index][0] + rectangles[temp_index][2])
                temp_y2 = min(rectangle[1] + rectangle[3], rectangles[temp_index][1] + rectangles[temp_index][3])
                w = max(0, temp_x2 - temp_x1)
                h = max(0, temp_y2 - temp_y1)

                # a ratio of how much the rectangle and the rectangles[temp_index] overlap
                overlap = (w * h) / (areas[temp_index] + areas[index] - (w * h))

                # the higher the threshold, the rectangle will be removed since it overlaps more
                if overlap > overlap_threshold:
                    indexes.remove(index)
                    break

        return [rectangle for rectangle_index, rectangle in enumerate(rectangles) if rectangle_index in indexes]


def get_average_rectangles(*, rectangles: List[Tuple[float, float, float, float]], overlap_threshold: float) -> List[Tuple[float, float, float, float]]:

    if len(rectangles) == 0:
        return []
    else:

        areas = []  # type: List[float]
        for rectangle in rectangles:
            area = rectangle[2] * rectangle[3]
            areas.append(area)

        nearby_rectangle_indexes_per_rectangle_index = {}  # type: Dict[int, List[int]]
        nearby_rectangle_indexes_magnitude_per_rectangle_index = {}  # type: Dict[int, float]

        indexes = list(range(len(areas)))
        for index, rectangle in enumerate(rectangles):

            nearby_rectangle_indexes_per_rectangle_index[index] = []  # type: List[int]
            nearby_rectangle_indexes_magnitude_per_rectangle_index[index] = 0.0  # type: float
            temp_indexes = [i for i in indexes if i != index]

            for temp_index in temp_indexes:
                temp_x1 = max(rectangle[0], rectangles[temp_index][0])
                temp_y1 = max(rectangle[1], rectangles[temp_index][1])
                temp_x2 = min(rectangle[0] + rectangle[2], rectangles[temp_index][0] + rectangles[temp_index][2])
                temp_y2 = min(rectangle[1] + rectangle[3], rectangles[temp_index][1] + rectangles[temp_index][3])
                w = max(0, temp_x2 - temp_x1)
                h = max(0, temp_y2 - temp_y1)

                # a ratio of how much the rectangle and the rectangles[temp_index] overlap
                overlap = (w * h) / (areas[temp_index] + areas[index] - (w * h))
                print(f"{index}: overlap from {rectangle} to {rectangles[temp_index]} with {overlap}.")

                # the higher the threshold, the rectangle will be removed since it overlaps more
                if overlap > overlap_threshold:
                    nearby_rectangle_indexes_per_rectangle_index[index].append(temp_index)
                    nearby_rectangle_indexes_magnitude_per_rectangle_index[index] += overlap

        # start with the rectangles that have the most nearby rectangles
        used_rectangle_index = set()
        averaged_rectangles = []  # type: List[Tuple[float, float, float, float]]
        for rectangle_index in sorted(nearby_rectangle_indexes_magnitude_per_rectangle_index, key=nearby_rectangle_indexes_magnitude_per_rectangle_index.get, reverse=True):

            if rectangle_index not in used_rectangle_index:

                used_rectangle_index.add(rectangle_index)

                acceptable_rectangle_indexes = []  # type: List[int]
                for nearby_rectangle_index in nearby_rectangle_indexes_per_rectangle_index[rectangle_index]:
                    if nearby_rectangle_index not in used_rectangle_index:
                        acceptable_rectangle_indexes.append(nearby_rectangle_index)
                acceptable_rectangle_indexes.append(rectangle_index)

                if acceptable_rectangle_indexes:

                    x1 = 0
                    y1 = 0
                    x2 = 0
                    y2 = 0

                    for acceptable_rectangle_index in acceptable_rectangle_indexes:
                        x1 += rectangles[acceptable_rectangle_index][0]
                        y1 += rectangles[acceptable_rectangle_index][1]
                        x2 += rectangles[acceptable_rectangle_index][0] + rectangles[acceptable_rectangle_index][2]
                        y2 += rectangles[acceptable_rectangle_index][1] + rectangles[acceptable_rectangle_index][3]

                        used_rectangle_index.add(acceptable_rectangle_index)

                    x1 /= len(acceptable_rectangle_indexes)
                    y1 /= len(acceptable_rectangle_indexes)
                    x2 /= len(acceptable_rectangle_indexes)
                    y2 /= len(acceptable_rectangle_indexes)

                    averaged_rectangles.append((x1, y1, x2 - x1, y2 - y1))

        return averaged_rectangles


def get_unique_directory_path(*, parent_directory_path: str) -> str:
    _child_directory_path = None
    while _child_directory_path is None:
        _child_directory_name = str(uuid.uuid4())
        _child_directory_path = os.path.join(parent_directory_path, _child_directory_name)
        if os.path.exists(_child_directory_path):
            _child_directory_path = None
    return _child_directory_path


def get_unique_file_path(*, parent_directory_path: str, extension: str) -> str:
    _formatted_extension = extension if extension.startswith(".") else f".{extension}"
    _child_file_path = None
    while _child_file_path is None:
        _child_file_name = f"{uuid.uuid4()}{_formatted_extension}"
        _child_file_path = os.path.join(parent_directory_path, _child_file_name)
        if os.path.exists(_child_file_path):
            _child_file_path = None
    return _child_file_path


def get_subclasses(*, cls: Type, include_children: bool) -> List[Type]:
    subclasses = cls.__subclasses__()
    if include_children:
        children = []  # type: List[Type]
        for subclass in subclasses:
            children.extend(get_subclasses(
                cls=subclass,
                include_children=True
            ))
        subclasses.extend(children)
    return subclasses


class JsonParsableException(Exception):

    def __init__(self, *args):
        super().__init__(*args)

        pass


class JsonParsable(ABC):

    @classmethod
    @abstractmethod
    def get_json_parsable_type_dictionary_key(cls) -> str:
        raise NotImplementedError()

    @classmethod
    def parse_json(cls, *, json_dict) -> JsonParsable:
        if cls.__name__ == JsonParsable.__name__:
            raise JsonParsableException(f"Cannot parse json with JsonParsable class. You must create a parent class for all of your subclasses to inherit from.")
        elif cls in get_subclasses(
            cls=JsonParsable,
            include_children=False
        ):
            subclasses = get_subclasses(
                cls=cls,
                include_children=True
            )  # type: List[Type[JsonParsable]]

            parse_class = None
            for subclass in subclasses:
                if subclass.get_json_parsable_type().value == json_dict[cls.get_json_parsable_type_dictionary_key()]:
                    parse_class = subclass
                    break

            if parse_class is None:
                raise JsonParsableException(f"Failed to find subclass for type \"{json_dict[cls.get_json_parsable_type_dictionary_key()]}\".")

        else:
            if cls.get_json_parsable_type().value != json_dict[cls.get_json_parsable_type_dictionary_key()]:
                raise JsonParsableException(f"Cannot parse json to type {cls.__name__} when json specifies type {json_dict[cls.get_json_parsable_type_dictionary_key()]}.")

            parse_class = cls

        del json_dict[cls.get_json_parsable_type_dictionary_key()]
        return parse_class(**json_dict)

    @abstractmethod
    def to_json(self) -> Dict:
        return {
            self.__class__.get_json_parsable_type_dictionary_key(): self.__class__.get_json_parsable_type().value
        }

    @classmethod
    @abstractmethod
    def get_json_parsable_type(cls) -> StringEnum:
        raise NotImplementedError()


def get_all_files_in_directory(*, directory_path: str, include_subdirectories: bool) -> List[str]:
    files = []  # type: List[str]

    if include_subdirectories:
        for walk_directory_path, walk_directory_names, walk_file_names in os.walk(directory_path):
            files.extend([os.path.join(walk_directory_path, walk_file_name) for walk_file_name in walk_file_names])
    else:
        files.extend([os.path.join(directory_path, file_name) for file_name in os.listdir(directory_path)])

    return files


def get_random_rainbow_color(*, random_instance: random.Random = None) -> Tuple[float, float, float]:
    if random_instance is None:
        random_instance = random.Random()
    main_color_index = random_instance.randrange(3)
    secondary_color_amount = random_instance.random()
    color_r = 1 if main_color_index == 0 else secondary_color_amount if main_color_index == 1 else 1 - secondary_color_amount
    color_g = 1 if main_color_index == 1 else secondary_color_amount if main_color_index == 2 else 1 - secondary_color_amount
    color_b = 1 if main_color_index == 2 else secondary_color_amount if main_color_index == 0 else 1 - secondary_color_amount
    return (color_r, color_g, color_b)


def load_file_as_base64string(*, file_path: str) -> str:
    with open(file_path, "rb") as file_handle:
        file_bytes = file_handle.read()
    return base64.b64encode(file_bytes).decode()


def save_file_from_base64string(*, file_bytes_base64string: str, file_path: str):
    file_bytes = base64.b64decode(file_bytes_base64string.encode())
    with open(file_path, "wb") as file_handle:
        file_handle.write(file_bytes)


def get_delimited_string_regex_pattern_frequencies(*, text: str):
    regex_patterns = []  # type: List[str]
    lines = text.replace("\r\n", "\n").split("\n")
    regex_replacement_per_original = {
        r"|": r"\|",
        "\\": "\\\\",
        r"(": r"\(",
        r")": r"\)",
        r".": r"\.",
        r"+": r"\+",
        r"*": r"\*",
        r"?": r"\?",
        r"^": r"\^",
        r"$": r"\$",
        r"[": r"\[",
        r"]": r"\]",
        r"{": r"\{",
        r"}": r"\}",
        r"-": r"\-"
    }

    def get_replacement(text: str) -> str:
        output = text
        for original, replacement in regex_replacement_per_original.items():
            output = output.replace(original, replacement)
        return output

    for line in lines:
        # pair up string sequences
        for delimiter, replacement in zip([" ", "|", ",", "\t"], [" +", r"\|+", ",+", r"\t+"]):
            delimited_words = [x for x in line.split(delimiter) if x != ""]
            if len(delimited_words) > 1:
                escaped_delimited_words = [
                    get_replacement(x) for x in delimited_words
                ]
                for start_word_index in range(len(delimited_words)):
                    for end_word_index in range(start_word_index + 1, len(delimited_words) + 1):
                        regex_pattern = replacement.join(escaped_delimited_words[start_word_index:end_word_index])
                        regex_patterns.append(regex_pattern)

    total_per_regex_pattern = dict((x, regex_patterns.count(x)) for x in set(regex_patterns))

    return total_per_regex_pattern


class StoredCollection():

    def __init__(self, *, directory_path: str):
        self.__directory_path = directory_path

        self.__subdirectory_path = None  # type: str
        self.__index_file_path = None  # type: str
        self.__index_file_handle = None  # type: io.BytesIO
        self.__count_file_path = None  # type: str
        self.__count = None  # type: int
        self.__index_bytes_length = None  # type: int
        self.__is_index_file_handle_at_end = None  # type: bool

        self.__initialize()

    def __initialize(self):
        self.__subdirectory_path = os.path.join(self.__directory_path, "collection")
        pathlib.Path(self.__subdirectory_path).mkdir(parents=True, exist_ok=True)

        self.__index_file_path = os.path.join(self.__directory_path, ".index")
        self.__index_file_handle = open(self.__index_file_path, "w+b")
        self.__index_file_handle.seek(0, io.SEEK_END)
        self.__index_bytes_length = self.__index_file_handle.tell()
        self.__is_index_file_handle_at_end = True

        self.__count_file_path = os.path.join(self.__directory_path, ".count")
        if os.path.exists(self.__count_file_path):
            with open(self.__count_file_path, "r") as file_handle:
                self.__count = int(file_handle.readline())
        else:
            self.__count = 0

    def append(self, *, json_dict: dict):
        file_uuid = uuid.uuid4()
        file_uuid_bytes = file_uuid.bytes
        file_uuid_string = str(file_uuid)
        file_path = os.path.join(self.__subdirectory_path, f"{file_uuid_string}.ser")
        with open(file_path, "w") as file_handle:
            json.dump(json_dict, file_handle)
        if not self.__is_index_file_handle_at_end:
            self.__index_file_handle.seek(0, io.SEEK_END)
            self.__is_index_file_handle_at_end = True
        self.__index_file_handle.write(file_uuid_bytes)
        self.__index_bytes_length += 17
        self.__count += 1

    def get(self) -> dict:
        if not self.__is_index_file_handle_at_end:
            file_uuid_bytes = self.__index_file_handle.read(16)
            if self.__index_file_handle.tell() == self.__index_bytes_length:
                self.__is_index_file_handle_at_end = True
            file_uuid = uuid.UUID(bytes=file_uuid_bytes)
            file_uuid_string = str(file_uuid)
            file_path = os.path.join(self.__subdirectory_path, f"{file_uuid_string}.ser")
            with open(file_path, "r") as file_handle:
                return json.load(file_handle)
        return None

    def try_process(self, process_method: Callable[[dict], dict]) -> bool:
        if not self.__is_index_file_handle_at_end:
            file_uuid_bytes = self.__index_file_handle.read(16)
            if self.__index_file_handle.tell() == self.__index_bytes_length:
                self.__is_index_file_handle_at_end = True
            file_uuid = uuid.UUID(bytes=file_uuid_bytes)
            file_uuid_string = str(file_uuid)
            file_path = os.path.join(self.__subdirectory_path, f"{file_uuid_string}.ser")
            with open(file_path, "r") as file_handle:
                json_dict = json.load(file_handle)
            processed_json_dict = process_method(json_dict)
            if processed_json_dict is not None:
                with open(file_path, "w") as file_handle:
                    json.dump(processed_json_dict, file_handle)
            return True
        return False

    def reset(self):
        if self.__index_bytes_length != 0:
            self.__index_file_handle.seek(0)
            self.__is_index_file_handle_at_end = False

    def count(self) -> int:
        return self.__count

    def dispose(self):
        self.__index_file_handle.close()


datetime_string_format = "%Y-%m-%d %H:%M:%S.%f"


def convert_datetime_to_string(*, datetime: datetime) -> str:
    return datetime.strftime(datetime_string_format)


def convert_string_to_datetime(*, string: str) -> datetime:
    return datetime.strptime(string, datetime_string_format)


date_string_format = "%Y-%m-%d"


def convert_date_to_string(*, date: date) -> str:
    return date.strftime(date_string_format)


def convert_string_to_date(*, string: str) -> date:
    return datetime.strptime(string, date_string_format).date()


def get_random_date(random_instance: random.Random = None) -> date:
    if random_instance is None:
        random_instance = random.Random()
    days_total = random_instance.randrange(3287182)
    days_timedelta = timedelta(days=days_total + 364877)
    return date.min + days_timedelta


def get_random_string_enum_value(*, enum_type: Type[StringEnum], random_instance: random.Random = None) -> str:
    if random_instance is None:
        random_instance = random.Random()
    list_of_enum_types = list(enum_type)
    return list_of_enum_types[random_instance.randrange(len(list_of_enum_types))].value


def next_again(iterator: Iterator, count: int, default: Any = None) -> Any:
    if iterator is not Iterator:
        iterator = iter(iterator)
    output = default
    for _ in range(count):
        output = next(iterator, default)
    return output


def get_comma_delimited_english_phrases(*, phrases: List[str], final_combinator: str, default: str = None):
    if not phrases:
        return default
    phrases_total = len(phrases)
    if phrases_total == 1:
        return phrases[0]
    if phrases_total == 2:
        return f"{phrases[0]} {final_combinator} {phrases[1]}"
    return "".join([(", " if phrase_index != 0 else "") + (f"{final_combinator} " if phrase_index + 1 == phrases_total else "") + phrase for phrase_index, phrase in enumerate(phrases)])
