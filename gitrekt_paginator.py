from requests.auth import HTTPBasicAuth
import requests
import re
def pagination(gitUser, gitPass, gitTerm):
	header_text_highlite = {'Accept': 'application/vnd.github.v3.text-match+json'}
	with requests.Session() as session:
       		search = session.head('https://api.github.com/search/code?q='+gitTerm+'+in:file', headers=header_text_highlite, auth=HTTPBasicAuth(gitUser, gitPass))
        	#mystring = search.headers
        	link = search.headers.get('link', None)
        	if link is not None:
                	#print link
                	m = re.search('page=(\d+.)>; rel="last"', link)
                	print("MAX PAGES: " + m.group(1))
			maxPages = m.group(1)
			return maxPages
