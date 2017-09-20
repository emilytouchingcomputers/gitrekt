from requests.auth import HTTPBasicAuth
from gitrekt_paginator import pagination
import requests
import json
import argparse
import re
import time
import sys
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
#No clue what this is for but it breaks the script if it's not here
header_text_highlite = {'Accept': 'application/vnd.github.v3.text-match+json'}
#While loop and counter for getting all pages of results
counter = 1
#Yeah so turns out gitPages was returning a string and it was ruining this while test, so now we cast it to int because that wasted 4 hours of my life.
gitPages = int(gitPages)
while (counter != gitPages):
	with requests.Session() as session:
		try:
			with requests.Session() as session:
                		search = session.get('https://api.github.com/search/code?q='+gitTerm+'+in:file&page=' + str(counter), headers=header_text_highlite, auth=HTTPBasicAuth(gitUser, gitPass))
                		#Our results are stored in var data
                		data = search.text
				#Load the results into the JSON parser
				j = json.loads(data)
				#Bro I don't even know.  Wrote this code months ago and can't figure out whats going on.  JSON parsing is hard.
				count = len(j["items"])
				for x in range(0, count):
					print("<RESULT>")
					print("<REPO_NAME> " + j['items'][x]['repository']['name'])
					print("</REPO_NAME>")
					print("<FILENAME> " + j['items'][x]['name'])
					print("</FILENAME>")
					print("<CODE> " + j['items'][x]['text_matches'][0]['fragment'])
					print("</CODE>")
					print("<REPO_URL> " + j['items'][x]['html_url'])
					print("</REPO_URL>")
					print("</RESULT>")
					print("")
		except Exception:
			#We probably caught a rate limit
			if "abuse-rate-limits" in data:
                        	print ("RATE LIMITED!")
                        	print("SLEEPING 60 SECONDS")
                        	time.sleep(60)
                        	print("RESUMING!")
			continue
	#Increase our counter to change the search page to the next one	
	counter += 1
	#Print what the next page of results is
	#print("*********************************************************************NEXT PAGE: "+ str(counter))
####################################################################################################
