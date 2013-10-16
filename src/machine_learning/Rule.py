class Rule(object):
    def __init__(self, index, value):
        self._parts = [(index, value)]

    def conjuct(self, r):
        self._parts.extend(r.getParts())

    def getParts(self):
        return self._parts

    def describes(self, genotype):
        for (index, value) in self._parts:
            if genotype[index] == value:
                return False
        return True
