__author__="bunkdeath"
__date__ ="$Dec 21, 2012 2:43:56 PM$"


import json
import time
import requests
from LogPoint import LogPoint
from Device import Device
from SearchJob import SearchJob
from Repos import Repo


class LogPointSearcher:
    '''
    Searcher class to search for following
    '''
    def __init__(self, ip, username, secret_key):
        self.ip = ip
        self.username = username
        self.secert_key = secret_key
        self.request_type = 'https'


    def get_log_points(self):
        '''
        Returns list of LogPoint object
        '''
        """
            send requests to given IP using username and secret_key for type = "logpoints"
            our webserver should return [{"name": "", "ip":""}]
        """

        logpoints = []
        
        response = self._get_allowed_data('loginspects')
        allowed_logpoint = response['allowed_loginspects'];
        
        for data in allowed_logpoint:
            logpoints.append(LogPoint(data["ip"], data["name"]))

        return logpoints


    def get_repos(self, logpoint=None):
        ''' 
        Search for repos for which the user have permission to access
        according to credential provided

        If no parameter passed, it searches for the repos within
        all logpoints

        If logpoint object is passed as a parameter,
        it searches for the repos within the logpoint referenced
        by the logpoint object

        Returns list of Repo object
        '''

        repos = []
        
        response = self._get_allowed_data('repos')
        allowed_repos = response.get('allowed_repos')
        for repo in allowed_repos:
            repos.append(Repo(repo.get('repo')))
        return repos

    def get_devices(self, logpoint=None):
        '''
        Search for devices for which the user have permission to access
        according to credential provided

        If no parameter passed, it searches for the devices within
        all logpoints

        If logpoint object is passed as a parameter,
        it searches for the devices within the logpoint referenced
        by the logpoint object

        Returns list of Device object
        '''
        
        devices = []

        response = self._get_allowed_data('devices')
        print response
        allowed_devices = response['allowed_devices'];

        for i in range(len(allowed_devices)):
            token = allowed_devices[i].split('/')
            device_ip = token[1]
            devices.append(Device(device_ip))
        
        return devices

    def get_live_searches(self):
        '''
        Returns list of LiveSearch object
        '''

        response =  self._get_allowed_data('livesearches')
        return response

    def get_timezone(self):
        '''
        Returns timezone of user according to credential provided
        '''
        """
            webserver should return UTC or Asia/Kathmandu
        """

        return self._get_allowed_data('user_preference')['timezone']

    def search(self, query, timerange=None, repo=None, timeout=30, limit=100):
        '''
        Returns SearchJob object
        '''

        return self._get_search_job(query)

    def _get_allowed_data(self, data_type):
        url = "%s://%s/%s" % (self.request_type, self.ip, "getalloweddata")

        data = {
                "username": self.username,
                "secret_key": self.secert_key,
                "type": data_type
                }

        ack = requests.post(url, data=data, timeout=10.0, verify=False)
        ret = ''

        try:
            ret = json.loads(ack.content)
        except:
            print ack.content

        return ret

    def _get_search_job(self, query):
        SEARCH_QUERY = "| chart count() by device_ip"
        SEARCH_QUERY = query
        RESULT_LIMIT = 10
        SEARCH_TIME_RANGE = "Last 10 minutes"
        SEARCH_REPOS = []
        url = "%s://%s/%s" % (self.request_type, self.ip, "getsearchlogs")

        data = {
                "username":self.username,
                "secret_key": self.secert_key,
                "requestData": json.dumps({
                               "timeout": 30,
                               "client_name": "gui",
                               "repos": SEARCH_REPOS,
                               "starts": {},
                               "limit": RESULT_LIMIT,
                               "time_range": SEARCH_TIME_RANGE,
                               "query": SEARCH_QUERY
                            })
                }

        ack = requests.post(url, data=data, timeout=10.0, verify=False)

        response = json.loads(ack.content)
        return SearchJob(self, query, response)
        

    def get_response(self, search_id):
        url = "%s://%s/%s" % (self.request_type, self.ip, "getsearchlogs")
        if search_id:
            data = {
                "username":self.username,
                "secret_key": self.secert_key,
                "requestData": json.dumps({
                           "search_id": search_id,
                           "waiter_id": "%s" % time.time(),
                           "seen_version": 0
                           })
                }

            start_time = time.time()
            response = {}
            i = 1
            while time.time() - start_time < 10.0:
                ack = requests.post(url, data=data, timeout=10.0, verify=False)
                res = json.loads(ack.content)
                if res.get('success'):
                    response = res
                if res['final'] == True:
                    print 'final'
                    break

            if not response:
                return {"success":False, "message":"No data from merger"}

            return response