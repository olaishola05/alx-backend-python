#!/usr/bin/env python3

"""Test cases for the public_repo_url function."""


import unittest
from unittest.mock import patch
from client import GithubOrgClient
from parameterized import parameterized


class TestGithubOrgClient(unittest.TestCase):
    """
    A test class to test the public_repo_url function
    """
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json', autospec=True)
    def test_org(self, company_name, mock_get_json):
        """Testing that GithubOrgClient.org returns
        the correct value and get_json is called once with expected arg
        """

        client = GithubOrgClient(company_name)
        expected_data = {"repos_url": client.ORG_URL.format(org=company_name)}
        mock_get_json.return_value = expected_data
        actual_org_data = client.org

        self.assertEqual(actual_org_data, expected_data)
        expected_url = client.ORG_URL.format(org=company_name)
        mock_get_json.assert_called_once_with(expected_url)


if __name__ == '__main__':
    unittest.main()
