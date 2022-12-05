import pytest
import json
import requests
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone
from data_retriveal import *

class TestSingleRetriveal:
    DATAPATH = 'test/data_retriveal/data/'
    BASEPULLURL = 'https://api.github.com/repos/chaoss/grimoirelab-perceval/pulls/10'

    COMMITURL = 'https://api.github.com/repos/chaoss/grimoirelab-perceval/commits/'
    COMMITSHA = 'f7cec4254eac3e10c4c75d54b9d5c4d6d88ccd6e'

    URL2FILENAME = {BASEPULLURL: 'pull_request_10_response.json',
                    BASEPULLURL + '/comments': 'pull_request_10_comments_response.json',
                    COMMITURL + COMMITSHA: 'commit.json'}

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

    @patch('requests.get')
    def test_getCommitBySha(self, mock_request):
        repo = RepoRetriveal('chaoss', 'grimoirelab-perceval')
        mock_request.side_effect = self.side_effect
        commit = repo.getCommitBySha('f7cec4254eac3e10c4c75d54b9d5c4d6d88ccd6e')
        filesInfo = self.loadJsonFile('commit.json')['files']
        assert commit == RepoRetriveal.Commit(sha='f7cec4254eac3e10c4c75d54b9d5c4d6d88ccd6e', 
                                                author_login='sduenas', 
                                                filesInfo=filesInfo, 
                                                date=datetime(2022, 11, 7, 9, 0, 33, tzinfo=timezone.utc))
       
class TestIterables:
    @patch('data_retriveal.RepoRetriveal.getPullByNumber')
    def test_getPullIterable(self, mock_method):
        repo = RepoRetriveal('owner', 'repo')
        mock_method.return_value = None

        numberRetrieved = 0
        for pull in repo.getPullIterable(100, 30):
            numberRetrieved += 1
        
        assert numberRetrieved == 30

    @patch('data_retriveal.RepoRetriveal.getFromUrl')
    @patch('data_retriveal.RepoRetriveal.getCommitBySha')
    def test_getCommitIterable(self, mock_method, mock_request):
        repo = RepoRetriveal('owner', 'repo')
        mock_request.return_value = [{'sha': 'fakesha'}] * 100
        mock_method.return_value = {'sha': 'fakesha'}

        numberRetrieved = 0
        for commit in repo.getCommitsIterable(datetime.now(), 101):
            numberRetrieved += 1
        
        assert numberRetrieved == 101
