import data_retriveal
from datetime import datetime
from collections import defaultdict


if __name__ == '__main__':

    reviewRank = defaultdict(lambda: 0)
    token = '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'
    repo = data_retriveal.RepoRetriveal('chaoss', 'grimoirelab-perceval', token)
    pull = repo.getPullByNumber(10)
    print(pull)
    pull_date = datetime.fromisoformat(pull.date[:-1])

    for commit in repo.getCommitsIterable(extensions=['.py']):
        #if commit.committer_date < pull_date: continue
        #print(commit.committer_date, commit.committer_timezone)
        author = commit.author.name
        files = commit.modified_files
        for file in files:
            fileName = file.filename 
            if author != pull.author and  fileName in pull.files:
                reviewRank[author] += 1

    print(reviewRank)
