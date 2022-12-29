import argparse
from review_recommender.ranker import getRanking
from review_recommender.data_retriveal import RepoRetriveal

def parse():
    parser = argparse.ArgumentParser(
                        prog = 'ReviewRecommender',
                        description = 'Given pull request, rank revisors')

    parser.add_argument('owner') 
    parser.add_argument('repo') 
    parser.add_argument('num', type=int)
    parser.add_argument('token')

    args = parser.parse_args()
    repo = RepoRetriveal(args.owner, args.repo, args.token)
    return repo, args.num

if __name__ == '__main__':
    repo, pullNumber = parse()
    print(getRanking(repo, pullNumber).prettyFormat())
