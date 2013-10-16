import unittest as test 
from agent.Agent import Agent

class AgentTest(test.TestCase):
    
    def setUp(self):
        self._agents = dict((i, Agent(i, None)) for i in xrange(1, 5))
        self._agents[1].addChildren(self._agents[2])
        self._agents[2].setParent(self._agents[1])
        self._agents[2].addChildren(self._agents[3], self._agents[4])
        self._agents[3].setParent(self._agents[2])
        self._agents[4].setParent(self._agents[2])
    
    def testGetDescendants1(self):
        descendants = self._agents[1].getDescendants(parent=False)
        self.assertTrue(all([(aId in [2, 3, 4]) 
            for aId in map(lambda x: x.getId(), descendants)]))
        self.assertEqual(3, len(descendants))
        
    def testGetDescendants2(self):
        descendants = self._agents[1].getDescendants(parent=True)
        self.assertTrue(all([(aId in [1, 2, 3, 4]) 
            for aId in map(lambda x: x.getId(), descendants)]))
        self.assertEqual(4, len(descendants))
 
    def testGetDescendants3(self):
        descendants = self._agents[2].getDescendants(parent=False)
        self.assertTrue(all([(aId in [3, 4]) 
            for aId in map(lambda x: x.getId(), descendants)]))
        self.assertEqual(2, len(descendants))
    
    def testGetDescendants3(self):
        descendants = self._agents[2].getDescendants(parent=True)
        self.assertTrue(all([(aId in [2, 3, 4]) 
            for aId in map(lambda x: x.getId(), descendants)]))
        self.assertEqual(3, len(descendants))

if __name__ == '__main__':
    test.main()
