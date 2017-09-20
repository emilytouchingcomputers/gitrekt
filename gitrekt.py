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
header_text_highlite = {'Accept': 'application/vnd.github.v3.text-match+json'}
#While loop and counter for getting all pages of results
counter = 1
while (counter != gitPages):
	print("TOP OF THE WHILE LOOP")
	with requests.Session() as session:
		print("IN THE WITH LOOP")
		search = session.get('https://api.github.com/search/code?q='+gitTerm+'+in:file&page=' + str(counter), headers=header_text_highlite, auth=HTTPBasicAuth(gitUser, gitPass))
		#Our results are stored in var data
		data = search.text
		#Was catching errors when we rate limited.
		#This clearly screws up JSON parsing as well, so we deal with that in the TRY/EXCEPT block below
		#if "abuse-rate-limits" in data:
		#	print ("RATE LIMITED!")
		#	print("SLEEPING 60 SECONDS")
		#	time.sleep(60)
		#	print("RESUMING!")
	        #Load those results into the json parser
		try:
			print("IN THE TOP OF THE TRY STATEMENT")
			with requests.Session() as session:
                		search = session.get('https://api.github.com/search/code?q='+gitTerm+'+in:file&page=' + str(counter), headers=header_text_highlite, auth=HTTPBasicAuth(gitUser, gitPass))
                		#Our results are stored in var data
                		data = search.text
				j = json.loads(data)
				#Bro I don't even know.  Wrote this code months ago and can't figure out whats going on.  JSON parsing is hard.
				count = len(j["items"])
				for x in range(0, count):
					print("<BEGIN>")
					print("Repo Name: " + j['items'][x]['repository']['name'])
					#print("Filename: " + j['items'][x]['name'])
					#print("Matched Code: " + j['items'][x]['text_matches'][0]['fragment'])
					#print("Repo URL: " + j['items'][x]['html_url'])
					print("<END>")
					print(counter)
					#print("*************************************************************")
					print("")
			print("BOTTOM OF THE TRY STATEMENT")
		except Exception:
			print("TOP OF THE EXCEPTION")
			#We caught a rate limit and it screwed us up. 
			#Since we still tried to parse it, and then we pass to the counter +=1
			#We need to decrease the counter by one to continue where we left off so 
			#We won't miss a page
			print("EXCEPTION!")
			if "abuse-rate-limits" in data:
                        	print ("RATE LIMITED!")
                        	print("SLEEPING 60 SECONDS")
                        	time.sleep(60)
                        	print("RESUMING!")
			continue
		#Increase our counter to change the search page to the next one	
	counter += 1
	print("WE JUST INCREMENTED THE COUNTER WOWZERS")
		#Print what the next page of results is
	print("*********************************************************************NEXT PAGE: "+ str(counter))
####################################################################################################
