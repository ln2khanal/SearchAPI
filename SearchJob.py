# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="bunkdeath"
__date__ ="$Dec 24, 2012 11:36:15 AM$"

class SearchJob:
    def __init__(self, searcher, query, response):
        self._success = False
        self._has_error = True
        self._error_message = ''
        self._is_final = True
        self._type = ''
        self._is_timeout = True
        self._is_cancel = True
        self._timerange = ''

        #extra added items

        self._query = query
        self._searcher = searcher
        self.search_id = ''

        if response:
            self._parse_query(response)
        
        
        return

    def has_error(self):
        '''
        Checks if the response has some error

        returns true if response has error

        returns false if response has no error
        '''
        return not self._success

    def is_final(self):
        '''
        Checks if the response from the server is final i.e. no
        further result is left(reach the limit)  from server
        to respond

        returns true if search has reached its limit

        returns false if some result are to be respond
        '''
        return self._is_final

    def get_response(self):
        response = self._searcher.get_response(self.search_id)
        
        return response

    def get_type(self):
        self._type

    def is_timeout(self):
        self._is_timeout

    def is_cancel(self):
        pass

    def get_timerange(self):
        return self._timerange

    def get_error(self):
        return self._error_message

    def _set_error_message(self, message):
        self._error_message = message
        if message == 'timeout':
            self._is_timeout = True
        elif message == 'cancelled':
            self._is_cancel = True


    def _parse_query(self, response):
        self._success = response.get('success')
        self._search_id = response.get('search_id')
        self._set_error_message(response.get('message'))
        
        if self._success:
            self._type = response.get('query_type')
            self._timerange = response.get('time_range')
            self.search_id = response.get('search_id')