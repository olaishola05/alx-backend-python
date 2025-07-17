#!/usr/bin/env python3

import unittest
from parameterized import parameterized
from utils import access_nested_map

class TestAccessNestedMap(unittest.TestCase):
    """
    A test class to test the return value of the nested_map function
    """

    @parameterized.expand([
        ("nested_map_1", {"a": 1},["a"], 1),
        ("nested_map_2", {"a": {"b": 2}},["a"], {"b": 2}),
        ("nested_map_3", {"a": {"b": 2}},["a", "b"], 2)
    ])
    def test_access_nested_map(self, name, nested_map, path, expected):
        """
            A method that tests the return value of the access_nested_map function using
            the @parameterized decorator to run multiple tests with different parameters.

            :param name: A string representing the name of the test case.
            :param nested_map: A mapping (e.g., dictionary) representing the nested structure to be tested.
            :param path: A tuple representing the sequence of keys to access the value in the nested map.
            :param expected: The expected value to be returned by the access_nested_map function.
            :return: None
        """
        with self.subTest(name):
            actual_result = access_nested_map(nested_map, path)
            self.assertEqual(actual_result, expected)


# if __name__ == '__main__':
#     unittest.main(argv=['first-arg-is-ignored'], exit=False)
