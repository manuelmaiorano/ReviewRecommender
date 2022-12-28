import pytest
from unittest.mock import patch, MagicMock
import requests_cache
from data_retriveal import RepoRetriveal
from ranker import getRanking
from scorer import Scorer
import os
dirname = os.path.dirname(__file__)

DBPATH = os.path.join(dirname, 'data/test_db')
test_cache = requests_cache.CachedSession(DBPATH, allowable_codes=(200, 404))

def side_effect( url, params=None):
    headers = {"Accept": "application/vnd.github+json"}
    r = test_cache.get(url, headers=headers,
                    params=params,
                    timeout=10)
    r.raise_for_status()
    return r.json()

@patch('data_retriveal.RepoRetriveal.getFromUrl')
def test_getRanking(mock_request):
    mock_request.side_effect = side_effect
    repo = RepoRetriveal('opencv', 'opencv')
    scores = getRanking(repo, 23008, 10, 10)
    print(scores.getSorted())

    assert 'alalek'