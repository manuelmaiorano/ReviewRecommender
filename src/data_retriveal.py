from __future__ import annotations
import requests
from dataclasses import dataclass
from datetime import datetime 
import pytz
import base64
import math


class RepoRetriveal:
    @dataclass
    class PullRequest:
        number: int
        author_login: str
        reviewers: list[str]
        date: datetime

        def __hash__(self) -> int:
            return self.number

    @dataclass
    class Commit:
        sha: str
        author_login: str
        filesInfo: list
        date: datetime

        def __hash__(self) -> int:
            return self.sha.__hash__()

    @dataclass
    class RepoFile:
        filepath: str
        content: str

    def __init__(self, owner, repo, token=None):
        self.owner = owner
        self.repo = repo
        self.token = token
        self.base_url = f'https://api.github.com/repos/{owner}/{repo}'
        self.headers = {"Accept": "application/vnd.github+json"}
        if token:
            self.headers["Authorization"] = f"Bearer {token}"
        self.s = requests.Session()
        self.timeout = 10

    def getFromUrl(self, url, params=None):
        r = self.s.get(url, headers=self.headers,
                       params=params,
                       timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def getPullByNumber(self, number):
        pull_url = f'{self.base_url}/pulls/{str(number)}'
        reviews_url = f'{pull_url}/reviews'

        data = self.getFromUrl(pull_url)
        author_login = data['user']['login']
        date_str = data['created_at']
        date = datetime.fromisoformat(date_str[:-1])
        date = pytz.utc.localize(date)

        data = self.getFromUrl(reviews_url)
        reviewers = []
        for review in data:
            reviewers.append(review['user']['login'])

        return RepoRetriveal.PullRequest(number, author_login,
                                         reviewers, date)

    def getCommitBySha(self, sha):
        commit_url = f'{self.base_url}/commits/{sha}'

        data = self.getFromUrl(commit_url)
        author_login = data['author']['login']
        date_str = data['commit']['author']['date']
        date = datetime.fromisoformat(date_str[:-1])
        date = pytz.utc.localize(date)

        filesInfo = data['files']

        return RepoRetriveal.Commit(sha, author_login, filesInfo, date)

    def getCommitsIterable(self, toDate: datetime, numberOfCommits):
        MAX_PER_PAGE = 100
        commit_url = f'{self.base_url}/commits'
        date_str = toDate.isoformat()[:-6]+'Z'

        if numberOfCommits <= MAX_PER_PAGE:
            commitsPerPage = numberOfCommits
            numOfPages = 1
        else:
            commitsPerPage = MAX_PER_PAGE
            numOfPages = math.ceil(numberOfCommits/MAX_PER_PAGE)

        currentPage = 1
        currentNumOfCommits = 0
        while currentPage <= numOfPages:
            params = {'until': date_str,
                      'per_page': commitsPerPage,
                      'page': currentPage}
            data = self.getFromUrl(commit_url, params=params)

            for item in data:
                if currentNumOfCommits >= numberOfCommits: break
                yield self.getCommitBySha(item['sha'])
                currentNumOfCommits += 1
            currentPage += 1

    def getPullIterable(self, toNumber, numberOfPulls):

        numOfPullsRetrieved = 0
        numOfPullsBackward = 0
        while numOfPullsRetrieved < numberOfPulls:
            numOfPullsBackward += 1
            try:
                pull = self.getPullByNumber(toNumber - numOfPullsBackward)
                numOfPullsRetrieved += 1
            except requests.HTTPError:
                continue
            yield pull

    def getPullFiles(self, pull: PullRequest):
        files_url = f'{self.base_url}/pulls/{str(pull.number)}/files'
        data = self.getFromUrl(files_url)
        return self.getFileContentList(data)

    def getCommitFiles(self, commit: Commit):
        return self.getFileContentList(commit.filesInfo)

    def getFileContentList(self, files_data):
        files = []
        for item in files_data:
            content_url = item['contents_url']
            file_data = self.getFromUrl(content_url)
            raw_content = file_data['content']
            try:
                decoded_content = base64.b64decode(raw_content).decode('utf-8')
            except UnicodeDecodeError:
                continue
            file = RepoRetriveal.RepoFile(item['filename'], decoded_content)
            files.append(file)

        return files
