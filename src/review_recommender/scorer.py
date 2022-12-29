class Scorer:
    def __init__(self):
        self.reviewerToScore = {}
        
    def addReviewerScore(self, reviewer, score):

        if reviewer not in self.reviewerToScore:
            self.reviewerToScore[reviewer] = 0
        self.reviewerToScore[reviewer] += score

    def getSorted(self):
        reviewer = dict(sorted(self.reviewerToScore.items(), 
                               key=lambda item: item[1], 
                               reverse=True))
        return reviewer

    def prettyFormat(self):
        totalScore = 0
        for score in self.reviewerToScore.values(): totalScore += score

        finalString = 'Reviewer         | Score      ' + '\n'
        finalString += '-----------------------------' + '\n'
        for reviewer, score in self.getSorted().items():
            spaces = ' ' * (len('Reviewer         ') - len(reviewer))
            finalString += (reviewer + spaces + '|' + f'{score/totalScore*100: .2f} %' + '\n')

        return finalString


