from __future__ import annotations
import unittest
from typing import List, Tuple, Dict, Type, Callable
import gc
import random
from src.austin_heller_repo.common import AggregateDependentDependencyManager


class AggregateDependentDependencyManagerTest(unittest.TestCase):

	def test_initialize(self):

		def on_dependent_dependency_satisfied_callback(dependent, dependency_and_key_pairs):
			raise NotImplementedError()

		manager = AggregateDependentDependencyManager(
			on_dependent_dependency_satisfied_callback=on_dependent_dependency_satisfied_callback
		)

		self.assertIsNotNone(manager)

	def test_one_dependent_and_one_dependency(self):

		found_pairs = []  # type: List[Tuple[str, List[Tuple[str, str]]]]
		def on_dependent_dependency_satisfied_callback(dependent, dependency_and_key_pairs):
			nonlocal found_pairs
			found_pairs.append((dependent, dependency_and_key_pairs))

		manager = AggregateDependentDependencyManager(
			on_dependent_dependency_satisfied_callback=on_dependent_dependency_satisfied_callback
		)

		manager.add_dependent(
			dependent="dependent 0",
			reusable_keys=[],
			nonreusable_keys=[
				"key"
			]
		)

		self.assertEqual([], found_pairs)

		manager.add_dependency(
			key="key",
			dependency="dependency 0",
			is_reusable=False
		)

		self.assertEqual([("dependent 0", [("dependency 0", "key")])], found_pairs)

	def test_one_dependency_and_one_dependent(self):

		found_pairs = []  # type: List[Tuple[str, List[Tuple[str, str]]]]
		def on_dependent_dependency_satisfied_callback(dependent, dependency_and_key_pairs):
			nonlocal found_pairs
			found_pairs.append((dependent, dependency_and_key_pairs))

		manager = AggregateDependentDependencyManager(
			on_dependent_dependency_satisfied_callback=on_dependent_dependency_satisfied_callback
		)

		manager.add_dependency(
			key="key",
			dependency="dependency 0",
			is_reusable=False
		)

		self.assertEqual([], found_pairs)

		manager.add_dependent(
			dependent="dependent 0",
			reusable_keys=[],
			nonreusable_keys=[
				"key"
			]
		)

		self.assertEqual([("dependent 0", [("dependency 0", "key")])], found_pairs)

	def test_one_dependent_and_one_unrelated_dependency(self):

		found_pairs = []  # type: List[Tuple[str, List[Tuple[str, str]]]]
		def on_dependent_dependency_satisfied_callback(dependent, dependency_and_key_pairs):
			nonlocal found_pairs
			found_pairs.append((dependent, dependency_and_key_pairs))

		manager = AggregateDependentDependencyManager(
			on_dependent_dependency_satisfied_callback=on_dependent_dependency_satisfied_callback
		)

		manager.add_dependent(
			dependent="dependent 0",
			reusable_keys=[],
			nonreusable_keys=[
				"key"
			]
		)

		self.assertEqual([], found_pairs)

		manager.add_dependency(
			key="other",
			dependency="dependency 0",
			is_reusable=False
		)

		self.assertEqual([], found_pairs)

	def test_one_dependency_and_one_unrelated_dependent(self):

		found_pairs = []  # type: List[Tuple[str, List[Tuple[str, str]]]]
		def on_dependent_dependency_satisfied_callback(dependent, dependency_and_key_pairs):
			nonlocal found_pairs
			found_pairs.append((dependent, dependency_and_key_pairs))

		manager = AggregateDependentDependencyManager(
			on_dependent_dependency_satisfied_callback=on_dependent_dependency_satisfied_callback
		)

		manager.add_dependency(
			key="key",
			dependency="dependency 0",
			is_reusable=False
		)

		self.assertEqual([], found_pairs)

		manager.add_dependent(
			dependent="dependent 0",
			reusable_keys=[],
			nonreusable_keys=[
				"other"
			]
		)

		self.assertEqual([], found_pairs)

	def test_one_dependent_and_one_reusable_dependency(self):

		found_pairs = []  # type: List[Tuple[str, List[Tuple[str, str]]]]
		def on_dependent_dependency_satisfied_callback(dependent, dependency_and_key_pairs):
			nonlocal found_pairs
			found_pairs.append((dependent, dependency_and_key_pairs))

		manager = AggregateDependentDependencyManager(
			on_dependent_dependency_satisfied_callback=on_dependent_dependency_satisfied_callback
		)

		manager.add_dependent(
			dependent="dependent 0",
			reusable_keys=[
				"key"
			],
			nonreusable_keys=[]
		)

		self.assertEqual([], found_pairs)

		manager.add_dependency(
			key="key",
			dependency="dependency 0",
			is_reusable=True
		)

		self.assertEqual([("dependent 0", [("dependency 0", "key")])], found_pairs)

	def test_two_reusable_dependencies_and_three_dependents_add_another_dependency_and_three_dependents(self):

		found_pairs = []  # type: List[Tuple[str, List[Tuple[str, str]]]]
		def on_dependent_dependency_satisfied_callback(dependent, dependency_and_key_pairs):
			nonlocal found_pairs
			found_pairs.append((dependent, dependency_and_key_pairs))

		manager = AggregateDependentDependencyManager(
			on_dependent_dependency_satisfied_callback=on_dependent_dependency_satisfied_callback
		)

		for index in range(2):
			manager.add_dependency(
				key="key",
				dependency=f"dependency {index}",
				is_reusable=True
			)
			self.assertEqual([], found_pairs)

		for index in range(3):
			manager.add_dependent(
				dependent=f"dependent {index}",
				reusable_keys=[
					"key"
				],
				nonreusable_keys=[]
			)
			if index == 0:
				self.assertEqual([("dependent 0", [("dependency 0", "key")])], found_pairs)
			elif index == 1:
				self.assertEqual([("dependent 0", [("dependency 0", "key")]), ("dependent 1", [("dependency 1", "key")])], found_pairs)
			elif index == 2:
				self.assertEqual([("dependent 0", [("dependency 0", "key")]), ("dependent 1", [("dependency 1", "key")]), ("dependent 2", [("dependency 0", "key")])], found_pairs)

		manager.add_dependency(
			key="key",
			dependency=f"dependency 2",
			is_reusable=True
		)

		self.assertEqual([("dependent 0", [("dependency 0", "key")]), ("dependent 1", [("dependency 1", "key")]), ("dependent 2", [("dependency 0", "key")])], found_pairs)

		for index in range(3, 3):
			manager.add_dependent(
				dependent=f"dependent {index}",
				reusable_keys=[
					"key"
				],
				nonreusable_keys=[]
			)
			if index == 0:
				self.assertEqual([("dependent 0", [("dependency 0", "key")]), ("dependent 1", [("dependency 1", "key")]), ("dependent 2", [("dependency 0", "key")]), ("dependent 3", [("dependency 1", "key")])], found_pairs)
			elif index == 1:
				self.assertEqual([("dependent 0", [("dependency 0", "key")]), ("dependent 1", [("dependency 1", "key")]), ("dependent 2", [("dependency 0", "key")]), ("dependent 3", [("dependency 1", "key")]), ("dependent 4", [("dependency 0", "key")])], found_pairs)
			elif index == 2:
				self.assertEqual([("dependent 0", [("dependency 0", "key")]), ("dependent 1", [("dependency 1", "key")]), ("dependent 2", [("dependency 0", "key")]), ("dependent 3", [("dependency 1", "key")]), ("dependent 4", [("dependency 0", "key")]), ("dependent 5", [("dependency 2", "key")])], found_pairs)

	def test_one_dependency_and_one_dependent_multiple_times(self):

		found_pairs = []  # type: List[Tuple[str, List[Tuple[str, str]]]]
		def on_dependent_dependency_satisfied_callback(dependent, dependency_and_key_pairs):
			nonlocal found_pairs
			found_pairs.append((dependent, dependency_and_key_pairs))

		manager = AggregateDependentDependencyManager(
			on_dependent_dependency_satisfied_callback=on_dependent_dependency_satisfied_callback
		)

		for index in range(1000000):
			manager.add_dependent(
				dependent="dependent 0",
				reusable_keys=[],
				nonreusable_keys=[
					"key"
				]
			)

			self.assertEqual(index, len(found_pairs))

			manager.add_dependency(
				key="key",
				dependency="dependency 0",
				is_reusable=False
			)

			self.assertEqual(index + 1, len(found_pairs))

	def test_one_dependent_and_one_dependency_and_one_dependent(self):

		found_pairs = []  # type: List[Tuple[str, List[Tuple[str, str]]]]
		def on_dependent_dependency_satisfied_callback(dependent, dependency_and_key_pairs):
			nonlocal found_pairs
			found_pairs.append((dependent, dependency_and_key_pairs))

		manager = AggregateDependentDependencyManager(
			on_dependent_dependency_satisfied_callback=on_dependent_dependency_satisfied_callback
		)

		manager.add_dependent(
			dependent="dependent 0",
			reusable_keys=[],
			nonreusable_keys=[
				"key"
			]
		)

		self.assertEqual([], found_pairs)

		manager.add_dependency(
			key="key",
			dependency="dependency 0",
			is_reusable=False
		)

		self.assertEqual([("dependent 0", [("dependency 0", "key")])], found_pairs)

		manager.add_dependent(
			dependent="dependent 0",
			reusable_keys=[],
			nonreusable_keys=[
				"key"
			]
		)

		self.assertEqual([("dependent 0", [("dependency 0", "key")])], found_pairs)

	def test_one_dependent_has_multiple_dependencies(self):

		found_pairs = []  # type: List[Tuple[str, List[Tuple[str, str]]]]
		def on_dependent_dependency_satisfied_callback(dependent, dependency_and_key_pairs):
			nonlocal found_pairs
			found_pairs.append((dependent, dependency_and_key_pairs))

		manager = AggregateDependentDependencyManager(
			on_dependent_dependency_satisfied_callback=on_dependent_dependency_satisfied_callback
		)

		dependencies = [
			{
				"key": "non 0",
				"dependency": "dep 0",
				"is_reusable": False
			},
			{
				"key": "non 1",
				"dependency": "dep 1",
				"is_reusable": False
			},
			{
				"key": "non 1",
				"dependency": "dep 2",
				"is_reusable": False
			},
			{
				"key": "reuse 0",
				"dependency": "dep 3",
				"is_reusable": True
			},
			{
				"key": "reuse 1",
				"dependency": "dep 4",
				"is_reusable": True
			},
		]

		dependency_and_key_pairs = [("dep 0", "non 0"), ("dep 1", "non 1"), ("dep 2", "non 1"), ("dep 3", "reuse 0"), ("dep 4", "reuse 1"), ("dep 4", "reuse 1")]
		dependency_and_key_pairs.sort()
		expected = [("dependent 0", dependency_and_key_pairs)]

		for index in range(100000):
			random.shuffle(dependencies)

			manager.add_dependent(
				dependent="dependent 0",
				reusable_keys=[
					"reuse 0",
					"reuse 1",
					"reuse 1"
				],
				nonreusable_keys=[
					"non 0",
					"non 1",
					"non 1"
				]
			)

			nonreusable_keys_total = 0
			for dependency in dependencies:

				if index == 0:
					self.assertEqual([], found_pairs)
				else:
					if nonreusable_keys_total != 3:
						self.assertEqual(index, len(found_pairs))
					else:
						self.assertEqual(index + 1, len(found_pairs))

				if index == 0:
					manager.add_dependency(**dependency)
				elif not dependency["is_reusable"]:
					nonreusable_keys_total += 1
					manager.add_dependency(**dependency)

			if index == 0:
				actual = found_pairs[0][1]
				actual.sort()
				self.assertEqual(expected, [(found_pairs[0][0], actual)])
			else:
				self.assertEqual(index + 1, len(found_pairs))
