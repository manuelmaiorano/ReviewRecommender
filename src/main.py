import data_retriveal
import argparse
from inverted_files import InvertedFile
from tokenizer import Tokenizer
from scorer import Scorer
from dataclasses import dataclass
import time

def loadingBarCallback(done, total):
    numOfTicks = 50
    percentage = int(done/total*100)
    print('done: ' + '-'* int(done/total* numOfTicks) + f'{percentage} %', end="\r")
    if percentage == 100: print('\n')

def parse():
    parser = argparse.ArgumentParser(
                        prog = 'ReviewRecommender',
                        description = 'Given pull request, rank revisors')

    parser.add_argument('owner') 
    parser.add_argument('repo') 
    parser.add_argument('num', type=int)
    parser.add_argument('token')

    args = parser.parse_args()
    repo = data_retriveal.RepoRetriveal(args.owner, args.repo, args.token)
    return repo, args.num

def getRanking(repo: data_retriveal.RepoRetriveal, pullNumber):
    NUM_OF_PULLS = 5
    NUM_OF_COMMITS = 5

    tokenizer = Tokenizer()
    scorer = Scorer()
    invertedFile = InvertedFile()

    print('collecting pulls...')
    done = 0
    for pull in repo.getPullIterable(pullNumber, NUM_OF_PULLS):
        done += 1
        loadingBarCallback(done, NUM_OF_PULLS)
        files = repo.getPullFiles(pull)
        pullTokenFreqs = tokenizer.getTokenFreqs(files)
        invertedFile.add(pull, pullTokenFreqs)

    print('collecting commits...')
    done = 0
    for commit in repo.getCommitsIterable(pull.date, NUM_OF_COMMITS):
        done += 1
        loadingBarCallback(done, NUM_OF_COMMITS)
        files = repo.getCommitFiles(commit)
        commitTokenFreqs = tokenizer.getTokenFreqs(files)
        invertedFile.add(commit, commitTokenFreqs)

    invertedFile.calculateIDF()
    
    newPull =repo.getPullByNumber(pullNumber)
    newPullTokenFreqs = tokenizer.getTokenFreqs(repo.getPullFiles(newPull))
    similar = invertedFile.getSimilar(newPullTokenFreqs)

    print('getting rank...')
    for item, score in similar.items():
        if isinstance(item, data_retriveal.RepoRetriveal.Commit) \
            and not item.author_login == newPull.author_login:
            scorer.addReviewerScore(item.author_login, score)
        elif isinstance(item, data_retriveal.RepoRetriveal.PullRequest):
            for commenter in item.commenters:
                if not commenter == newPull.author_login:
                    scorer.addReviewerScore(commenter, score)

    #invertedFile.dump()
    return scorer


if __name__ == '__main__':
    repo = data_retriveal.RepoRetriveal('python', 'cpython')
    pullNumber = 100151
    tic = time.perf_counter()
    print(getRanking(repo, pullNumber).prettyFormat())
    toc = time.perf_counter()
    print(f'elapsed: {toc -tic}')
