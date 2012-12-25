'''
Created on Dec 21, 2012

@author: mama
'''
class LogPoint:
    
    def __init__(self, ip, name=None):
        """
        """
        self.ip = ip
        if name:
            self.name = name
        else:
            self.name = self.ip.replace(".", "_")
    
    def __str__(self):
        """
        """
        return self.name