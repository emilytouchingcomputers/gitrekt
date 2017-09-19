from requests.auth import HTTPBasicAuth
import requests
import re

gitUser = 'user'
gitPass = 'pass'
gitTerm = 'term'

#file = open('/Users/username/Desktop/json.txt', 'w')
header_text_highlite = {'Accept': 'application/vnd.github.v3.text-match+json'}
with requests.Session() as session:
        search = session.head('https://api.github.com/search/code?q='+gitTerm+'+in:file', headers=header_text_highlite, auth=HTTPBasicAuth(gitUser, gitPass))
        #mystring = search.headers
        link = search.headers.get('link', None)
        if link is not None:
                #print link[-20:]
                m = re.search('page=(\d+.)>; rel="last"', link)
                print m.group(1)
