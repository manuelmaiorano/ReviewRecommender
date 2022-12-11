import pytest
from scorer import *

def test_scorer():
    scorer = Scorer()
    scorer.addReviewerScore("Reviewer1", 10)
    scorer.addReviewerScore("Reviewer1", 20)
    scorer.addReviewerScore("Reviewer2", 15)
    scorer.addReviewerScore("Reviewer3", 20)
    
    #assert scorer.getSorted() == {"Reviewer1": 30}

    assert scorer.getSorted() == {"Reviewer2": 15, "Reviewer3": 20, "Reviewer1": 30}