from operator import itemgetter
from MemetizationManager import MemetizationManager
from RulesSet import RulesSet
from Rule import Rule
from implementation.Parameters import *

class AQMemetizationManager(MemetizationManager):
    def __new__(cls, *args, **kwargs):
        return super(AQMemetizationManager, cls).__new__(cls, *args, **kwargs)

    def __init__(self):
        MemetizationManager.__init__(self)
        self._rules = RulesSet()

    def learn(self):
        self._discretize([t[0] for t in self._info])
        pos = self._getPositives()
        neg = self._getNegatives()

        for p in pos:
            for n in neg:
                rules_temp = RulesSet()
                for x in range(len(n)):
                    if n[x] != p[x]:
                        rules_temp.add(Rule(x, n[x]))
                self._rules.conjuct(rules_temp)
            if self._rules.describesAll(pos) and not self._rules.describesAny(neg):
                break

    def makeDecision(self, genotype):
        return self._rules.describes(self._discretizeOne(genotype))

    def _getPositives(self):
        best = [t[0] for t in sorted(self._info, key=itemgetter(1))[:Parameters.aqPositiveNegativeCount]]
        return [self._discretizeOne(x) for x in best]

    def _getNegatives(self):
        worst = [t[0] for t in sorted(self._info, key=itemgetter(1), reverse=True)[:Parameters.aqPositiveNegativeCount]]
        return [self._discretizeOne(x) for x in worst]

    def _discretize(self, genotypes):
        length = genotypes[0]
        self._lowerbound = [0] * len(length)
        self._size = [0] * len(length)
        for i in range(len(length)):
            self._lowerbound[i] = min(genotypes, key=lambda g: g[i])[i]
            self._size[i] = (max(genotypes, key=lambda g: g[i])[i] - self._lowerbound[i]) / 5.0

    def _discretizeOne(self, genotype):
        return [int((x - self._lowerbound[i]) / self._size[i]) for (i, x) in enumerate(genotype)]

