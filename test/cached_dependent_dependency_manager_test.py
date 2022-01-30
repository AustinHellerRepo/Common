from __future__ import annotations
import unittest
from typing import List, Tuple, Dict
from src.austin_heller_repo.common import CachedDependentDependencyManager


class CachedDependentDependencyManagerTest(unittest.TestCase):

	def test_initialize(self):

		def on_dependent_dependency_satisfied_callback(dependent, dependency):
			raise NotImplementedError()

		manager = CachedDependentDependencyManager(
			on_dependent_dependency_satisfied_callback=on_dependent_dependency_satisfied_callback,
			is_dependency_reusable=False
		)

		self.assertIsNotNone(manager)

	def test_one_dependent_and_one_dependency(self):

		found_pairs = []  # type: List[Tuple[str, str]]
		def on_dependent_dependency_satisfied_callback(dependent, dependency):
			nonlocal found_pairs
			found_pairs.append((dependent, dependency))

		manager = CachedDependentDependencyManager(
			on_dependent_dependency_satisfied_callback=on_dependent_dependency_satisfied_callback,
			is_dependency_reusable=False
		)

		manager.add_dependent(
			key="key",
			dependent="dependent 0"
		)

		self.assertEqual([], found_pairs)

		manager.add_dependency(
			key="key",
			dependency="dependency 0"
		)

		self.assertEqual([("dependent 0", "dependency 0")], found_pairs)

	def test_one_dependency_and_one_dependent(self):

		found_pairs = []  # type: List[Tuple[str, str]]
		def on_dependent_dependency_satisfied_callback(dependent, dependency):
			nonlocal found_pairs
			found_pairs.append((dependent, dependency))

		manager = CachedDependentDependencyManager(
			on_dependent_dependency_satisfied_callback=on_dependent_dependency_satisfied_callback,
			is_dependency_reusable=False
		)

		manager.add_dependency(
			key="key",
			dependency="dependency 0"
		)

		self.assertEqual([], found_pairs)

		manager.add_dependent(
			key="key",
			dependent="dependent 0"
		)

		self.assertEqual([("dependent 0", "dependency 0")], found_pairs)

	def test_one_dependent_and_one_unrelated_dependency(self):

		found_pairs = []  # type: List[Tuple[str, str]]
		def on_dependent_dependency_satisfied_callback(dependent, dependency):
			nonlocal found_pairs
			found_pairs.append((dependent, dependency))

		manager = CachedDependentDependencyManager(
			on_dependent_dependency_satisfied_callback=on_dependent_dependency_satisfied_callback,
			is_dependency_reusable=False
		)

		manager.add_dependent(
			key="key",
			dependent="dependent 0"
		)

		self.assertEqual([], found_pairs)

		manager.add_dependency(
			key="unrelated",
			dependency="dependency 0"
		)

		self.assertEqual([], found_pairs)

	def test_one_dependency_and_one_unrelated_dependent(self):

		found_pairs = []  # type: List[Tuple[str, str]]
		def on_dependent_dependency_satisfied_callback(dependent, dependency):
			nonlocal found_pairs
			found_pairs.append((dependent, dependency))

		manager = CachedDependentDependencyManager(
			on_dependent_dependency_satisfied_callback=on_dependent_dependency_satisfied_callback,
			is_dependency_reusable=False
		)

		manager.add_dependency(
			key="key",
			dependency="dependency 0"
		)

		self.assertEqual([], found_pairs)

		manager.add_dependent(
			key="unrelated",
			dependent="dependent 0"
		)

		self.assertEqual([], found_pairs)

	def test_one_dependent_and_one_reusable_dependency(self):

		found_pairs = []  # type: List[Tuple[str, str]]
		def on_dependent_dependency_satisfied_callback(dependent, dependency):
			nonlocal found_pairs
			found_pairs.append((dependent, dependency))

		manager = CachedDependentDependencyManager(
			on_dependent_dependency_satisfied_callback=on_dependent_dependency_satisfied_callback,
			is_dependency_reusable=True
		)

		manager.add_dependent(
			key="key",
			dependent="dependent 0"
		)

		self.assertEqual([], found_pairs)

		manager.add_dependency(
			key="key",
			dependency="dependency 0"
		)

		self.assertEqual([("dependent 0", "dependency 0")], found_pairs)

	def test_two_reusable_dependencies_and_three_dependents_add_another_dependency_and_three_dependents(self):
		found_pairs = []  # type: List[Tuple[str, str]]

		def on_dependent_dependency_satisfied_callback(dependent, dependency):
			nonlocal found_pairs
			found_pairs.append((dependent, dependency))

		manager = CachedDependentDependencyManager(
			on_dependent_dependency_satisfied_callback=on_dependent_dependency_satisfied_callback,
			is_dependency_reusable=True
		)

		for index in range(2):
			manager.add_dependency(
				key="key",
				dependency=f"dependency {index}"
			)
			self.assertEqual([], found_pairs)

		for index in range(3):
			manager.add_dependent(
				key="key",
				dependent=f"dependent {index}"
			)
			if index == 0:
				self.assertEqual([("dependent 0", "dependency 0")], found_pairs)
			elif index == 1:
				self.assertEqual([("dependent 0", "dependency 0"), ("dependent 1", "dependency 1")], found_pairs)
			elif index == 2:
				self.assertEqual([("dependent 0", "dependency 0"), ("dependent 1", "dependency 1"), ("dependent 2", "dependency 0")], found_pairs)

		manager.add_dependency(
			key="key",
			dependency="dependency 2"
		)

		self.assertEqual([("dependent 0", "dependency 0"), ("dependent 1", "dependency 1"), ("dependent 2", "dependency 0")], found_pairs)

		for index in range(3, 3):
			manager.add_dependent(
				key="key",
				dependent=f"dependent {index}"
			)
			if index == 3:
				self.assertEqual([("dependent 0", "dependency 0"), ("dependent 1", "dependency 1"), ("dependent 2", "dependency 0"), ("dependent 3", "dependency 1")], found_pairs)
			elif index == 4:
				self.assertEqual([("dependent 0", "dependency 0"), ("dependent 1", "dependency 1"), ("dependent 2", "dependency 0"), ("dependent 3", "dependency 1"), ("dependent 4", "dependency 0")], found_pairs)
			elif index == 5:
				self.assertEqual([("dependent 0", "dependency 0"), ("dependent 1", "dependency 1"), ("dependent 2", "dependency 0"), ("dependent 3", "dependency 1"), ("dependent 4", "dependency 0"), ("dependent 5", "dependency 2")], found_pairs)

	def test_one_dependency_and_one_dependent_multiple_times(self):

		found_pairs = []  # type: List[Tuple[str, str]]
		def on_dependent_dependency_satisfied_callback(dependent, dependency):
			nonlocal found_pairs
			found_pairs.append((dependent, dependency))

		manager = CachedDependentDependencyManager(
			on_dependent_dependency_satisfied_callback=on_dependent_dependency_satisfied_callback,
			is_dependency_reusable=False
		)

		for index in range(1000000):
			manager.add_dependency(
				key="key",
				dependency="dependency 0"
			)

			self.assertEqual(index, len(found_pairs))

			manager.add_dependent(
				key="key",
				dependent="dependent 0"
			)

			self.assertEqual(index + 1, len(found_pairs))
