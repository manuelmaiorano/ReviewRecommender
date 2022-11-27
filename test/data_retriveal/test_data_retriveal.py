import pytest
import json
import requests
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone
from data_retriveal import *

class TestRepoRetriveal:
    DATAPATH = 'test/data_retriveal/data/'
    BASEURL = 'https://api.github.com/repos/chaoss/grimoirelab-perceval/pulls/10'
    URL2FILENAME = {BASEURL: 'pull_request_10_response.json',
                    BASEURL + '/comments': 'pull_request_10_comments_response.json'}

    def loadJsonFile(self, filename):
        with open(self.DATAPATH + filename) as f:
            response = json.load(f)
        return response

    def side_effect(self, url, headers, params):
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.raise_for_status.return_value = None
            try:
                mock_response.json.return_value = self.loadJsonFile(self.URL2FILENAME[url])
            except KeyError:
                mock_response.status_code = 404
                mock_response.raise_for_status.side_effect = requests.HTTPError()
            return mock_response

    @patch('requests.get')
    def test_getPullByNumber(self, mock_request):
        repo = RepoRetriveal('chaoss', 'grimoirelab-perceval')
        
        mock_request.side_effect = self.side_effect

        pull = repo.getPullByNumber(10)
        assert pull == RepoRetriveal.PullRequest(number=10, 
                                                author_login='albertinisg', 
                                                commenters=['sduenas', 'sduenas', 'sduenas', 
                                                            'sduenas', 'sduenas'], 
                                                date=datetime(2016, 2, 9, 15, 2, 38, tzinfo=timezone.utc))

    @patch('requests.get')
    def test_getPullByNumber_badrepo(self, mock_request):
        repo = RepoRetriveal('badowner', 'badrepo')
        mock_request.side_effect = self.side_effect
        with pytest.raises(requests.HTTPError):
            repo.getPullByNumber(10)