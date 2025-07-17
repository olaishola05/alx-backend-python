#!/usr/bin/env python3

"""Test cases for the access_nested_map function."""

import unittest
from parameterized import parameterized
from utils import access_nested_map
from typing import Mapping, Sequence, Any


class TestAccessNestedMap(unittest.TestCase):
    """
    A test class to test the return value of the nested_map function
    """

    @parameterized.expand([
        ("nested_map_1", {"a": 1}, ["a"], 1),
        ("nested_map_2", {"a": {"b": 2}}, ["a"], {"b": 2}),
        ("nested_map_3", {"a": {"b": 2}}, ["a", "b"], 2)
    ])
    def test_access_nested_map(self, name: str, nested_map: Mapping, path: Sequence, expected: Any) -> None:
        self.assertEqual(access_nested_map(nested_map, path), expected)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
