'''
Created on Dec 21, 2012

@author: mama
'''

class Repo:
    
    def __init__(self, repo_name, logpoint=None):
        """
        """
#        self.logpoint = logpoint
#        self.name = "%s/%s" % (self.logpoint.name, name)
        self.name = repo_name
    
    def __str__(self):
        """
        """
        return self.name