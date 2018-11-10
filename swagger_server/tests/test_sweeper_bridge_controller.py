# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from swagger_server.models.inline_response2002 import InlineResponse2002  # noqa: E501
from swagger_server.models.inline_response2003 import InlineResponse2003  # noqa: E501
from swagger_server.models.inline_response2004 import InlineResponse2004  # noqa: E501
from swagger_server.models.inline_response2005 import InlineResponse2005  # noqa: E501
from swagger_server.models.inline_response2006 import InlineResponse2006  # noqa: E501
from swagger_server.models.inline_response2007 import InlineResponse2007  # noqa: E501
from swagger_server.test import BaseTestCase


class TestSweeperBridgeController(BaseTestCase):
    """SweeperBridgeController integration test stubs"""

    def test_accounts_account_id_algos_get(self):
        """Test case for accounts_account_id_algos_get

        
        """
        response = self.client.open(
            '/sweeper/v1/accounts/{accountId}/algos'.format(accountId='accountId_example'),
            method='GET',
            content_type='application/x-www-form-urlencoded')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_accounts_account_id_analysis_algo_id_get(self):
        """Test case for accounts_account_id_analysis_algo_id_get

        
        """
        response = self.client.open(
            '/sweeper/v1/accounts/{accountId}/analysis/{algoId}'.format(accountId='accountId_example', algoId='algoId_example'),
            method='GET',
            content_type='application/x-www-form-urlencoded')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_accounts_account_id_fixture_history_get(self):
        """Test case for accounts_account_id_fixture_history_get

        
        """
        query_string = [('maxCount', 8.14)]
        response = self.client.open(
            '/sweeper/v1/accounts/{accountId}/fixtureHistory'.format(accountId='accountId_example'),
            method='GET',
            content_type='application/x-www-form-urlencoded',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_accounts_account_id_fixtures_get(self):
        """Test case for accounts_account_id_fixtures_get

        
        """
        response = self.client.open(
            '/sweeper/v1/accounts/{accountId}/fixtures'.format(accountId='accountId_example'),
            method='GET',
            content_type='application/x-www-form-urlencoded')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_accounts_account_id_get(self):
        """Test case for accounts_account_id_get

        
        """
        response = self.client.open(
            '/sweeper/v1/accounts/{accountId}'.format(accountId='accountId_example'),
            method='GET',
            content_type='application/x-www-form-urlencoded')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_accounts_account_id_leagues_get(self):
        """Test case for accounts_account_id_leagues_get

        
        """
        response = self.client.open(
            '/sweeper/v1/accounts/{accountId}/leagues'.format(accountId='accountId_example'),
            method='GET',
            content_type='application/x-www-form-urlencoded')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_accounts_account_id_statistics_algo_id_get(self):
        """Test case for accounts_account_id_statistics_algo_id_get

        
        """
        response = self.client.open(
            '/sweeper/v1/accounts/{accountId}/statistics/{algoId}'.format(accountId='accountId_example', algoId='algoId_example'),
            method='GET',
            content_type='application/x-www-form-urlencoded')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_accounts_account_id_statistics_league_id_algo_id_get(self):
        """Test case for accounts_account_id_statistics_league_id_algo_id_get

        
        """
        response = self.client.open(
            '/sweeper/v1/accounts/{accountId}/statistics/{leagueId}/{algoId}'.format(accountId='accountId_example', leagueId='leagueId_example', algoId='algoId_example'),
            method='GET',
            content_type='application/x-www-form-urlencoded')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_authorize_post(self):
        """Test case for authorize_post

        
        """
        data = dict(login='login_example',
                    password='password_example')
        response = self.client.open(
            '/sweeper/v1/authorize',
            method='POST',
            data=data,
            content_type='application/x-www-form-urlencoded')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_leagues_get(self):
        """Test case for leagues_get

        
        """
        response = self.client.open(
            '/sweeper/v1/leagues',
            method='GET',
            content_type='application/x-www-form-urlencoded')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
