#!/usr/bin/env python3
"""Unit tests for GithubOrgClient.org"""

import unittest
from unittest.mock import patch, PropertyMock
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

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns expected list of repos and calls
        mocked methods once."""
        # Mock payload for get_json
        mock_repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": None}
        ]
        mock_get_json.return_value = mock_repos_payload

        # Use context manager to mock _public_repos_url
        mock_url_path = 'client.GithubOrgClient._public_repos_url'
        with patch(mock_url_path, new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/google/repos"

            # Create client instance and call public_repos
            client = GithubOrgClient("google")
            result = client.public_repos()

            # Verify the result is the expected list of repo names
            expected_repos = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected_repos)

            # Verify mocked property was called once
            mock_url.assert_called_once()

            # Verify get_json was called once
            mock_get_json.assert_called_once()


if __name__ == '__main__':
    unittest.main()
