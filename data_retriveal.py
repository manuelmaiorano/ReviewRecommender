import requests
from dataclasses import dataclass
from datetime import datetime
import pytz
import base64

class RepoRetriveal:
    @dataclass
    class PullRequest:
        number: int
        author_login: str
        commenters: list[str]
        date: datetime

    @dataclass
    class Commit:
        sha: str
        author_login: str
        files: list[str]
        date: datetime
    
    def __init__(self, owner, repo, token=None):
        self.owner = owner
        self.repo = repo
        self.token = token
        self.base_url = f'https://api.github.com/repos/{owner}/{repo}'
        self.pydriller_url = f'https://github.com/{owner}/{repo}.git'
        self.headers = {"Accept": "application/vnd.github+json"}
        if token: self.headers["Authorization"] = f"Bearer {token}"

    def getFromUrl(self, url, params=None):
        r = requests.get(url, headers=self.headers, params=params)
        r.raise_for_status()
        return r.json()

    def getPullByNumber(self, number):
        pull_url = f'{self.base_url}/pulls/{str(number)}'
        comments_url = f'{pull_url}/comments'

        data = self.getFromUrl(pull_url)
        author_login = data['user']['login']
        date_str = data['created_at']
        date = datetime.fromisoformat(date_str[:-1])
        date = pytz.utc.localize(date)

        data = self.getFromUrl(comments_url)
        commenters = []
        for comment in data:
            commenters.append(comment['user']['login'])

        return RepoRetriveal.PullRequest(number, author_login, commenters, date)

    def getCommitBySha(self, sha):
        commit_url = f'{self.base_url}/commits/{sha}'

        data = self.getFromUrl(commit_url)
        author_login = data['author']['login']
        date_str = data['commit']['author']['date']
        date = datetime.fromisoformat(date_str[:-1])
        date = pytz.utc.localize(date)

        files = []
        for item in data['files']:
            files.append(item['filename'])

        return RepoRetriveal.Commit(sha, author_login, files, date)

    def getCommitsIterable(self, toDate: datetime):
        commit_url = f'{self.base_url}/commits'
        date_str = toDate.isoformat()[:-6]+'Z'
        data = self.getFromUrl(commit_url, params={'since': date_str})

        for item in data:
            yield self.getCommitBySha(item['sha'])

    def getPullIterable(self, toNumber):
        pull_url = f'{self.base_url}/pulls'
        data = self.getFromUrl(pull_url, params={'state': 'closed'})

        for item in data:
            if item['number'] < toNumber:
                yield self.getPullByNumber(item['number'])


    def getPullFiles(self, pull: PullRequest):  
        files_url = f'{self.base_url}/pulls/{str(pull.number)}/files'
        data = self.getFromUrl(files_url)
        return self.getFileContentList(data)

    def getCommitFiles(self, commit: Commit):
        commit_url = f'{self.base_url}/commits/{commit.sha}'
        data = self.getFromUrl(commit_url)
        return self.getFileContentList(data['files'])

    def getFileContentList(self, files_data):
        files = []
        for item in files_data:
            content_url = item['contents_url']
            file_data = self.getFromUrl(content_url)
            content = file_data['content']
            files.append(base64.b64decode(content).decode('utf-8'))
        
        return files
