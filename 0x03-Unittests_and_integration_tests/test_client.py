#!/usr/bin/env python3
"""Unit tests for GithubOrgClient.org"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient.org"""

    @parameterized.expand([
        ("google", {"repos_url": "https://api.github.com/orgs/google/repos"}),
        ("abc", {"repos_url": "https://api.github.com/orgs/abc/repos"}),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, expected_data, mock_get_json):
        """Test that GithubOrgClient.org returns
        correct data and get_json is called once
        """
        # url = f"https://api.github.com/orgs/{org_name}/repos"
        # expected_payload = {"repos_url": url}
        mock_get_json.return_value = expected_data

        client = GithubOrgClient(org_name)
        result = client.org

        expected_url = client.ORG_URL.format(org=org_name)
        # print(f"Expected result: {result}")
        # print(f"Expected data: {expected_data}")
        self.assertEqual(result, expected_data)
        mock_get_json.assert_called_once_with(expected_url)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
