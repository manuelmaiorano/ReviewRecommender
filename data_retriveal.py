import pydriller
import requests
import json
from dataclasses import dataclass

class RepoRetriveal:
    @dataclass
    class PullRequest:
        number: int
        author: str
        files: list[str]
        commenters: list[str]
        date: str
    
    def __init__(self, owner, repo, token):
        self.owner = owner
        self.repo = repo
        self.token = token
        self.base_url = f'https://api.github.com/repos/{owner}/{repo}'
        self.pydriller_url = f'https://github.com/{owner}/{repo}.git'

    def getPullByNumber(self, number):
        pull_url = f'{self.base_url}/pulls/{str(number)}'
        files_url = f'{pull_url}/files'
        comments_url = f'{pull_url}/comments'

        headers={"Accept": "application/vnd.github+json", "Authorization": "Bearer %s"%self.token}

        r = requests.get(pull_url, headers=headers)
        data = r.json()

        author_login = data['user']['login']
        author_url = f'https://api.github.com/users/{author_login}'
        date = data['created_at']

        r = requests.get(author_url, headers=headers)
        data = r.json()
        author = data['name']

        r = requests.get(comments_url, headers=headers)
        data = r.json()

        commenters = []
        for comment in data:
            commenters.append(comment['user']['login'])


        r = requests.get(files_url, headers=headers)
        data = r.json()

        file_names = []
        for file in data:
            file_names.append(file["filename"])

        return RepoRetriveal.PullRequest(number, author, file_names, commenters, date)

    def getCommitsIterable(self, to):
        return pydriller.Repository(path_to_repo=self.pydriller_url,
                                    only_no_merge=True,
                                    to=to).traverse_commits()
