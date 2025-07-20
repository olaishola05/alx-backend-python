#!/usr/bin/env python3

"""Unit tests for GithubOrgClient.org"""
import sys
import os
import unittest
from unittest.mock import patch, PropertyMock, Mock, MagicMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


# class TestGithubOrgClient(unittest.TestCase):
#     """
#     Test cases for the GithubOrgClient class from client module.
#     This class contains tests to verify that the GithubOrgClient
#     correctly interacts with the GitHub API without making actual HTTP calls.
#     """
#
#     @parameterized.expand([
#         ("google",),
#         ("abc",),
#     ])
#     @patch('client.get_json', autospec=True)
#     def test_org(self, org_name, mock_get_json):
#         """Test that GithubOrgClient.org returns correct value and calls
#         get_json once."""
#         # Set up mock return value
#         expected_response = {"name": org_name, "type": "Organization"}
#         mock_get_json.return_value = expected_response
#
#         # Create client instance and call org property
#         client = GithubOrgClient(org_name)
#         result = client.org
#
#         # Verify get_json was called once with expected URL
#         expected_url = f"https://api.github.com/orgs/{org_name}"
#         mock_get_json.assert_called_once_with(expected_url)
#
#         # Verify the result matches the expected value
#         self.assertEqual(result, expected_response)
#
#     @patch('client.get_json', autospec=True)
#     def test_public_repos(self, mock_get_json):
#         """Test that public_repos returns expected list of repos and calls
#         mocked methods once."""
#
#         mock_repos_payload = [
#             {"name": "repo1", "license": {"key": "mit"}},
#             {"name": "repo2", "license": {"key": "apache-2.0"}},
#             {"name": "repo3", "license": None}
#         ]
#         mock_get_json.return_value = mock_repos_payload
#         mock_url_path = 'client.GithubOrgClient._public_repos_url'
#         with patch(mock_url_path, new_callable=PropertyMock) as mock_url:
#             mock_url.return_value = "https://api.github.com/orgs/google/repos"
#
#             client = GithubOrgClient("google")
#             result = client.public_repos()
#
#             expected_repos = ["repo1", "repo2", "repo3"]
#             self.assertEqual(result, expected_repos)
#
#             # Verify mocked property was called once
#             mock_url.assert_called_once()
#
#             # Verify get_json was called once
#             mock_get_json.assert_called_once()
#
#     @parameterized.expand([
#         ({"license": {"key": "my_license"}}, "my_license", True),
#         ({"license": {"key": "other_license"}}, "my_license", False),
#     ])
#     def test_has_license(self, repo, license_key, expected):
#         """Test that has_license returns expected boolean based on repo
#         license."""
#         client = GithubOrgClient("google")
#         result = client.has_license(repo, license_key)
#         self.assertEqual(result, expected)


class TestGithubOrgClient(unittest.TestCase):
    """
    Test cases for the GithubOrgClient class from client module.
    This class contains tests to verify that the GithubOrgClient
    correctly interacts with the GitHub API without making actual HTTP calls.
    """

    @parameterized.expand([
        ("google", {"repos_url": "https://api.github.com/orgs/google/repos"}),
        ("abc", {"repos_url": "https://api.github.com/orgs/abc/repos"}),
    ])
    @patch('client.get_json', autospec=True)
    def test_org(self, org_name: str, expected_org_data: dict, mock_get_json: MagicMock):
        """Test that GithubOrgClient.org returns correct value and calls
        get_json once."""
        # Set up mock return value
        # get_json directly returns the dictionary payload
        mock_get_json.return_value = expected_org_data

        # Create client instance and call org property
        client = GithubOrgClient(org_name)
        result = client.org  # Access as property

        # Verify get_json was called once with expected URL
        expected_url = client.ORG_URL.format(org=org_name)
        mock_get_json.assert_called_once_with(expected_url)

        # Verify the result matches the expected value
        self.assertEqual(result, expected_org_data)

    # @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    # def test__public_repos_url(self, mock_org_property: PropertyMock):
    #     """Test that _public_repos_url returns the correct URL based on mocked org data."""
    #     # Set up the mock return value for the org property
    #     expected_repos_url = "https://api.github.com/orgs/test_org/repos_from_mock"
    #     mock_org_property.return_value = {"repos_url": expected_repos_url}
    #
    #     # Create client instance (org_name doesn't strictly matter here as org is mocked)
    #     client = GithubOrgClient("test_org")
    #
    #     # Access the _public_repos_url property
    #     result_url = client._public_repos_url
    #
    #     # Verify GithubOrgClient.org property was accessed
    #     mock_org_property.assert_called_once()
    #
    #     # Verify the result matches the expected repos_url
    #     self.assertEqual(result_url, expected_repos_url)

    # @patch('client.get_json', autospec=True)
    # def test_public_repos(self, mock_get_json: MagicMock):
    #     """Test that public_repos returns expected list of repos and calls
    #     mocked methods once."""
    #
    #     # This payload is what get_json should return when called for repos
    #     mock_repos_payload = [
    #         {"name": "repo1", "license": {"key": "mit"}},
    #         {"name": "repo2", "license": {"key": "apache-2.0"}},
    #         {"name": "repo3", "license": None}
    #     ]
    #     mock_get_json.return_value = mock_repos_payload
    #
    #     # This is the URL that _public_repos_url would return
    #     mock_public_repos_url_value = "https://api.github.com/orgs/google/repos"
    #
    #     # Patch _public_repos_url (it's a property, so use PropertyMock)
    #     with patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock) as mock_url_property:
    #         mock_url_property.return_value = mock_public_repos_url_value
    #
    #         client = GithubOrgClient("google")  # org_name here doesn't affect mocks
    #         result = client.public_repos()
    #
    #         # Expecting just the names, if public_repos in client.py extracts them
    #         # If public_repos returns full dicts, adjust this expectation
    #         expected_repos_names = ["repo1", "repo2", "repo3"]
    #         self.assertEqual(result, expected_repos_names)
    #
    #         # Verify _public_repos_url property was accessed
    #         mock_url_property.assert_called_once()
    #
    #         # Verify get_json was called once with the correct URL
    #         mock_get_json.assert_called_once_with(mock_public_repos_url_value)

    # @parameterized.expand([
    #     ({"license": {"key": "my_license"}}, "my_license", True),
    #     ({"license": {"key": "other_license"}}, "my_license", False),
    #     ({}, "my_license", False),  # No 'license' key at all
    #     ({"license": None}, "my_license", False),  # 'license' key exists, but value is None
    #     ({"license": {"key": "my_license", "name": "MIT"}}, "my_license", True),  # Extra fields in license dict
    # ])
    # def test_has_license(self, repo: dict, license_key: str, expected: bool):
    #     """Test that has_license returns expected boolean based on repo
    #     license."""
    #     # No patching needed as has_license is a pure function
    #     client = GithubOrgClient("google")  # Org name doesn't affect this static method
    #     result = client.has_license(repo, license_key)
    #     self.assertEqual(result, expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration test cases for the GithubOrgClient class.
    This class contains integration tests that mock external requests
    but test the full flow of the GithubOrgClient methods.
    """

    @classmethod
    def setUpClass(cls):
        """Set up class fixtures and start request patcher."""
        def side_effect(url):
            """Side effect function to return appropriate payload based on
            URL."""
            mock_response = Mock()
            if url == "https://api.github.com/orgs/google":
                mock_response.json.return_value = cls.org_payload
            elif url == "https://api.github.com/orgs/google/repos":
                mock_response.json.return_value = cls.repos_payload
            else:
                mock_response.json.return_value = None
            return mock_response

        # Start patcher for requests.get
        cls.get_patcher = patch('requests.get', side_effect=side_effect)
        cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Stop the request patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns expected list of repos from
        fixtures."""
        client = GithubOrgClient("google")
        result = client.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test that public_repos with license filter returns expected
        apache-2.0 repos from fixtures."""
        client = GithubOrgClient("google")
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)


if __name__ == '__main__':
    unittest.main()
