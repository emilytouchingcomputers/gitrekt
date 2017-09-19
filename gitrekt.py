#cat json.txt | python -m json.tool >> pretty.txt
from requests.auth import HTTPBasicAuth
import requests
import json
gitUser = 'user'
gitPass = 'pass'
#file = open('/Users/mbishop22/Desktop/json.txt', 'w')
header_text_highlite = {'Accept': 'application/vnd.github.v3.text-match+json'}
with requests.Session() as session:
	#auth = session.get('https://api.github.com/search/code?q=t-mobile+in:file', auth=HTTPBasicAuth(gitUser, gitPass))
	#print auth.json()
	search = session.get('https://api.github.com/search/code?q=search+in:file', headers=header_text_highlite, auth=HTTPBasicAuth(gitUser, gitPass))
	#print search.headers
	data = search.text
	#print data
	j = json.loads(data)
	count = len(j["items"])
	for x in range(0, count):
		print("Repo Name: " + j['items'][x]['repository']['name'])
		print("Filename: " + j['items'][x]['name'])
		print("Matched Code: " + j['items'][x]['text_matches'][0]['fragment'])
		print("Repo URL: " + j['items'][x]['html_url'])
		print("*************************************************************")
		print("")
		print("")

