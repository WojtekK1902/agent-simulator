from sklearn.naive_bayes import GaussianNB
from machine_learning.MemetizationManager import MemetizationManager

class NBMemetizationManager(MemetizationManager):
    def __new__(cls, *args, **kwargs):
        return super(NBMemetizationManager, cls).__new__(cls, *args, **kwargs)

    def __init__(self):
        MemetizationManager.__init__(self)

    def learn(self):
        gnb = GaussianNB()
        self._pred = gnb.fit([x[0] for x in self._info], [self._classify(x[1]) for x in self._info])

    def makeDecision(self, genotype):
        pred_predict = self._pred.predict([genotype])
        return pred_predict[0] > 0

    def _classify(self, param):
        if param > 0:
            return 1
        else:
            return 0

