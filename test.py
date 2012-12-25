## To change this template, choose Tools | Templates
## and open the template in the editor.
#
#__author__="bunkdeath"
#__date__ ="$Dec 24, 2012 2:27:03 PM$"
#
#import urllib2
#import json
#
#url = 'http://api.twitter.com/1/trends/44418.json'
#
## download the json string
#json_string = urllib2.urlopen(url).read()
#print json_string
## de-serialize the string so that we can work with it
#the_data = json.loads(json_string)
#
## get the list of trends
#trends = the_data[0]['trends']
#
## print the name of each trend
#for trend in trends:
#    print trend['name']


#j = '{"timerange_second":0,"vid":"","description":"","searchname":"Remote Interactive Logon Sessions","query_info":{"every_time_unit":"second","query_type":"chart","query_filter":"((action=\'logged on\' OR action=\'logged off\' OR action='Logon' OR action='Logoff')  AND logon_type=10) OR ( event_id=551 OR event_id=4647)","lucene_query":"((action:logged\\ on OR action:logged\\ off OR action:logon OR action:logoff) _num_logon_type:[10 TO 10]) OR (_num_event_id:[551 TO 551] OR _num_event_id:[4647 TO 4647])","aliases":["group","count()"],"columns":["group","count()"],"grouping":["log_ts","user","logon_id","action","source_address","device_ip"]},"generated_by":"dashboard","timerange_day":1,"timerange_minute":0,"life_id":"6fc62f25c365a74d8694e9379ea71d17a9b6bec2","limit":100,"timerange_hour":0,"tid":"","query":"((action='logged on' OR action='logged off' OR action='Logon' OR action='Logoff')  AND logon_type=10) OR ( event_id=551 OR event_id=4647)| rename target_user as user  | chart count() by log_ts, user, logon_id, action, source_address, device_ip order by logon_id desc"    }'

j = open('text', 'r').read()
#print j

import json

a = json.loads(j)
print a['query_info']['lucene_query']