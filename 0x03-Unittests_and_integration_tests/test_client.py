#!/usr/bin/env python3
"""Unit tests for GithubOrgClient.org"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient.org"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        # url = f"https://api.github.com/orgs/{org_name}/repos"
        # expected_payload = {"repos_url": url}
        expected_payload = {
            "login": org_name,
            "repos_url": f"https://api.github.com/orgs/{org_name}/repos",
        }
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        # expected_url = GithubOrgClient.ORG_URL.format(org=org_name)
        self.assertEqual(result, expected_payload)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        # print("Called with:", mock_get_json.call_args)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
