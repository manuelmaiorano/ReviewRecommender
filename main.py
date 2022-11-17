import data_retriveal
from datetime import datetime
from collections import defaultdict
import pytz
import argparse

parser = argparse.ArgumentParser(
                    prog = 'ReviewRecommender',
                    description = 'Given pull request, rank revisors')

parser.add_argument('owner') 
parser.add_argument('repo') 
parser.add_argument('num', type=int)
parser.add_argument('token')

args = parser.parse_args()
repo = data_retriveal.RepoRetriveal(args.owner, args.repo, args.token)

def getRanking(repo, pullNumber, scoreFunc):
    reviewRank = defaultdict(lambda: 0)
    pull = repo.getPullByNumber(pullNumber)
    print(pull)
    pull_date = datetime.fromisoformat(pull.date[:-1])
    pull_date_aware = pytz.utc.localize(pull_date)
    for commit in repo.getCommitsIterable(to=pull_date_aware):
        commit_date = commit.committer_date
        author = commit.author.name
        files = commit.modified_files
        delta = (pull_date_aware - commit_date).total_seconds()
        for file in files:
            fileName = file.filename 
            if author != pull.author and  fileName in pull.files:
                reviewRank[author] += scoreFunc(delta)

    return reviewRank


if __name__ == '__main__':

    def scoreFunc(seconds):
        return 1

    print(getRanking(repo, args.num, scoreFunc))
