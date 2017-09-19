from requests.auth import HTTPBasicAuth
from gitrekt_paginator import pagination
import requests
import json
import argparse
import re
####################################################################################################
#Arg Parsing
#Take user/password/search term.
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--user', default = 'invalid',  type=str, help='Github Username')
parser.add_argument('-p', '--password', default = 'invalid',  type=str, help='Github Password')
parser.add_argument('-t', '--term', default = 'invalid', type=str, help='Search Term')
args = parser.parse_args()

#Turn our args into vars
gitUser = args.user
gitPass = args.password
gitTerm = args.term
gitPages = 0
#This checks to make sure people filled out all of the args
if (gitUser == 'invalid' or  gitPass == 'invalid' or gitTerm == 'invalid'):
	parser.print_help()

####################################################################################################

#Search functionality
#Gets the max number of results pages so we can go through all of them since github api only returns one page at a time
gitPages = pagination(gitUser, gitPass, gitTerm)
header_text_highlite = {'Accept': 'application/vnd.github.v3.text-match+json'}
#While loop and counter for getting all pages of results
counter = 0
while (counter <= gitPages):
	with requests.Session() as session:
		search = session.get('https://api.github.com/search/code?q='+gitTerm+'+in:file&page=' + str(counter), headers=header_text_highlite, auth=HTTPBasicAuth(gitUser, gitPass))
		#Our results are stored in var data
		data = search.text
	        #Load those results into the json parser
		try:
			j = json.loads(data)
			#Bro I don't even know.  Wrote this code months ago and can't figure out whats going on.  JSON parsing is hard.
			count = len(j["items"])
			for x in range(0, count):
				print("<BEGIN>")
				print("Repo Name: " + j['items'][x]['repository']['name'])
				print("Filename: " + j['items'][x]['name'])
				print("Matched Code: " + j['items'][x]['text_matches'][0]['fragment'])
				print("Repo URL: " + j['items'][x]['html_url'])
				print("<END>")
				#print("*************************************************************")
				print("")
		except:
			continue
		#Increase our counter to change the search page to the next one	
		counter += 1
		#Print what the next page of results is
		print("*********************************************************************NEXT PAGE: "+ str(counter))
####################################################################################################
