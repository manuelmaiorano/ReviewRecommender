Usage
=====

Installation
------------
To use Review Recommender, first install it using pip:

.. code-block:: console

   (.venv) $ pip install review-recommender

To use as a command line tool:

.. code-block:: console

    usage: review_recommender [-h] owner repo num token

    Given pull request, rank revisors

    positional arguments:
    owner       the owner of the repository
    repo        the name of the repository
    num         the number of the pull request
    token       the github access token

    optional arguments:
    -h, --help  show this help message and exit

To import it as a package:

.. code-block:: python

    from review_recommender.data_retriveal import RepoRetriveal
    from review_recommender.tokenizer import Tokenizer
    from review_recommender.inverted_files import InvertedFile
    from review_recommender.scorer import Scorer

    #showcase of the various functionalities

    repo = RepoRetriveal(owner, repo, token)
    pull_10 = repo.getPullByNumber(10)
    inv_fil = InvertedFile()

    for pull in repo.getPullIterable(toPull, number):
        files = repo.getPullFles(pull)
        token_frequencies = Tokenizer.getTokenFreqs(files)
        inv_fil.add(pull, token_frequencies)

    scorer = Scorer()
    
    for reviewer in pull.reviewers:
        scorer.add(reviewer, 0.23)
    
    for commit in repo.getCommitIterable(pull_10.date, number):
        break