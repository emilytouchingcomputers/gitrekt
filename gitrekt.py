#NOTES
#I DONT KNOW WHAT THIS DOES?
#cat json.txt | python -m json.tool >> pretty.txt
#
from requests.auth import HTTPBasicAuth
import requests
import json
import argparse

#Take user/password/search term.  Need to add error handling.
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--user', default='invalid', type=str, help='Github Username')
parser.add_argument('-p', '--password', default='invalid', type=str, help='Github Password')
parser.add_argument('-t', '--term', default='invalid', type=str, help='Search Term')
args = parser.parse_args()

gitUser = args.user
gitPass = args.password
gitTerm = args.term

#file = open('/Users/username/Desktop/json.txt', 'w')
header_text_highlite = {'Accept': 'application/vnd.github.v3.text-match+json'}
with requests.Session() as session:
	search = session.get('https://api.github.com/search/code?q='+gitTerm+'+in:file', headers=header_text_highlite, auth=HTTPBasicAuth(gitUser, gitPass))
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
