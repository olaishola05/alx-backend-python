#!/usr/bin/env python3
"""Unit tests for GithubOrgClient.org"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


# class TestGithubOrgClient(unittest.TestCase):
#     """Test class for GithubOrgClient.org"""
#
#     @parameterized.expand([
#         ("google",),
#         ("abc",),
#     ])
#     @patch("client.get_json")
#     def test_org(self, org_name, mock_get_json):
#         """Test the org method of GithubOrgClient"""
#
#         expected_payload = {
#             "name": org_name,
#             "type": "Organization",
#         }
#         mock_get_json.return_value = expected_payload
#
#         client = GithubOrgClient(org_name)
#         result = client.org
#         expected_url = f"https://api.github.com/orgs/{org_name}"
#         mock_get_json.assert_called_once_with(expected_url)
#
#         self.assertEqual(result, expected_payload)

class TestGithubOrgClient(unittest.TestCase):
    """
    Test cases for the GithubOrgClient class from client module.
    This class contains tests to verify that the GithubOrgClient
    correctly interacts with the GitHub API without making actual HTTP calls.
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct value and calls
        get_json once."""
        # Set up mock return value
        expected_result = {"name": org_name, "type": "Organization"}
        mock_get_json.return_value = expected_result

        # Create client instance and call org property
        client = GithubOrgClient(org_name)
        result = client.org

        # Verify get_json was called once with expected URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

        # Verify the result matches the expected value
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
