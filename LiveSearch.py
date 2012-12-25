__author__="bunkdeath"
__date__ ="$Dec 21, 2012 1:56:50 PM$"


class LiveSearch:
    
    def __init__(self, id, name):
        """
        """
        self.id = id
        self.name = name
        self.response = {}

    def set_response(self, response):
        """
        """
        self.response = response

    def get_response(self):
        '''
        get_response() => returns response object

        This method returns the response object for the live search
        '''
        return self.response
