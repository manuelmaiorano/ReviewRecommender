import data_retriveal
from datetime import datetime
from collections import defaultdict
import pytz

token = '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'
repo = data_retriveal.RepoRetriveal('chaoss', 'grimoirelab-perceval', token)

def getRanking(repo, pullNumber, scoreFunc):
    reviewRank = defaultdict(lambda: 0)
    pull = repo.getPullByNumber(pullNumber)
    print(pull)
    pull_date = datetime.fromisoformat(pull.date[:-1])
    pull_date_aware = pytz.utc.localize(pull_date)
    n_commits = 0
    for commit in repo.getCommitsIterable(to=pull_date_aware):
        n_commits += 1
        commit_date = commit.committer_date
        author = commit.author.name
        files = commit.modified_files
        delta = (pull_date_aware - commit_date).total_seconds()
        for file in files:
            fileName = file.filename 
            if author != pull.author and  fileName in pull.files:
                reviewRank[author] += scoreFunc(delta)

    print(n_commits)
    return reviewRank


if __name__ == '__main__':

    def scoreFunc(seconds):
        return 1

    print(getRanking(repo, 10, scoreFunc))
