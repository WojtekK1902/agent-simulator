#import abc

class Action(object):
    
    #__metaclass__ = abc.ABCMeta
      
    #@abc.abstractmethod  
    def doAction(self):
        '''Performs an action.'''
        pass

    #@abc.abstractmethod
    def rollback(self, index):
        '''Rollbacks an action if RuntimeError is raised.'''
        pass
