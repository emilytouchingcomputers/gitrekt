#Handles figuring out how many pages of search results we get
#Very wonky, and there has to be a better way.
#Broke it out of gitrekt.py because it was making the code unbearable to read
from requests.auth import HTTPBasicAuth
import requests
import re
#gitUser, gitPass, gitTerm are from gitrekt.py
#username, password, search term respectively.
def pagination(gitUser, gitPass, gitTerm):
	#No clue what this does but I'm scared to delete it
	header_text_highlite = {'Accept': 'application/vnd.github.v3.text-match+json'}
	with requests.Session() as session:
       		search = session.head('https://api.github.com/search/code?q='+gitTerm+'+in:file', headers=header_text_highlite, auth=HTTPBasicAuth(gitUser, gitPass))
        	#link is current page, next page, last page
		link = search.headers.get('link', None)
        	if link is not None:
                	#print link
			#regex to grab the page number of the last page of results
			try:
                		m = re.search('page=(\d+.)>; rel="last"', link)
			#print the number of pages (i.e. the number of the last page)
                		#print("MAX PAGES: " + m.group(1))
				maxPages = m.group(1)
			except:
				maxPages = 1
			#return maxpages to gitrekt.py for our while loop for searching
			return maxPages
