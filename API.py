# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="bunkdeath"
__date__ ="$Dec 24, 2012 2:28:01 PM$"



import json
import time
import requests
import ConfigParser

CONFIG_FILE = "search.conf" #name of config file containing loginspect ip, username, secret key

SEARCH_QUERY = "| chart count() by device_ip"
RESULT_LIMIT = 10
SEARCH_TIME_RANGE = "Last 10 minutes"
SEARCH_REPOS = []

def _get_config_parameters():
    parser = ConfigParser.SafeConfigParser()
    parser.read(CONFIG_FILE)

    ip = parser.get("config", "loginspect_ip")
    request_type = parser.get("config", "request_type")
    username = parser.get("config", "username")
    user_key = parser.get("config", "secret_key")

    return (ip, request_type, username, user_key)

def _get_allowed_data(ip, request_type, username, user_key, data_type):
    url = "%s://%s/%s" % (request_type, ip, "getalloweddata")

    data = {
            "username":username,
            "secret_key": user_key,
            "type": data_type
            }

    ack = requests.post(url, data=data, timeout=10.0, verify=False)

    print ack
    print ack.content
    ret = 'Sorry'

    try:
        ret = json.loads(ack.content)
    except:
        print 'sorry'

    return ret

def _get_search_results(ip, request_type, username, user_key):
    url = "%s://%s/%s" % (request_type, ip, "getsearchlogs")

    data = {
            "username":username,
            "secret_key": user_key,
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

    search_id = response.get('search_id')
    if response.get('success') and search_id:
        data = {
            "username":username,
            "secret_key": user_key,
            "requestData": json.dumps({
                       "search_id": search_id,
                       "waiter_id": "%s" % time.time(),
                       "seen_version": 0
                       })
            }

        start_time = time.time()
        response = {}
        while time.time() - start_time < 10.0:
            ack = requests.post(url, data=data, timeout=10.0, verify=False)
            res = json.loads(ack.content)
            if res.get('success'):
                response = res
            if res['final'] == True:
                break

        if not response:
            return {"success":False, "message":"No data from merger"}

        return response

    return response

def main():
    ip, request_type, username, user_key = _get_config_parameters()

    #FIND LIVESEARCHES CREATED BY USER
    #print _get_allowed_data(ip, request_type, username, user_key, "livesearches")

    #FIND REPOS ALLOWED FOR USER
    response = _get_allowed_data(ip, request_type, username, user_key, "repos")

    print response

    #FIND DEVICES ALLOWED FOR USER
    #print _get_allowed_data(ip, request_type, username, user_key, "devices")

    #FIND LOGINSPECT ALLOWED FOR USER
    #print _get_allowed_data(ip, request_type, username, user_key, "loginspects")

    #FIND USER PREFERENCES
    #print _get_allowed_data(ip, request_type, username, user_key, "user_preference")

    #PRINT SEARCH RESULTS
#    response = _get_search_results(ip, request_type, username, user_key)
#    print response
