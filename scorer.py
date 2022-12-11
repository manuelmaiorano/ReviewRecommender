class Scorer:
    def __init__(self):
        self.reviewerToScore = {}
        
    def addReviewerScore(self, reviewer, score):

        if reviewer not in self.reviewerToScore:
            self.reviewerToScore[reviewer] = 0
        self.reviewerToScore[reviewer] += score

    def getSorted(self):
        reviewer = dict(sorted(self.reviewerToScore.items(), key=lambda item: item[1]))
        return reviewer

