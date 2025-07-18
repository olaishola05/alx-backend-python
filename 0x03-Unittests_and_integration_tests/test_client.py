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
        """Test the org method of GithubOrgClient"""

        expected_payload = {
            "name": org_name,
            "type": "Organization",
        }
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org
        self.assertEqual(result, expected_payload)

        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
