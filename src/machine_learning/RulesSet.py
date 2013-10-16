class RulesSet(object):
    def __init__(self):
        self._rules = set()

    def add(self, rule):
        self._rules.add(rule)

    def conjuct(self, rules_to_add):
        for r1 in rules_to_add.getRules():
            for r2 in self._rules:
                r2.conjuct(r1)

    def getRules(self):
        return self._rules

    def describesAll(self, genotypes):
        for genotype in genotypes:
            for rule in self._rules:
                if not rule.describes(genotype):
                    return False
        return True

    def describesAny(self, genotypes):
        for genotype in genotypes:
            for rule in self._rules:
                if rule.describes(genotype):
                    return True
        return False

    def describes(self, genotype):
        for rule in self._rules:
            if not rule.describes(genotype):
                return False
        return True
