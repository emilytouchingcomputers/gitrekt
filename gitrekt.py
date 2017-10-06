#VERSION 0.3b
#October 4, 2017
##################################################################################################
#TODO:
#Some kind of JS baked into the html output for deleting/hiding unwanted or duplicate results
#Lightweight DB for 'recording' results?
#Probably improvements to the 'strict searching' functionality.  Currently doesn't write results
#to the file unless the result contains the exact search string.  This gets around the 
#'fuziness' of github search results, but can lead to missing things, especially with queries like
#(companyname vpn) which might not all get returned in the code snippet.
###################################################################################################
from requests.auth import HTTPBasicAuth
from gitrekt_paginator import pagination
from gitraw import get_raw_results
import requests
import json
import argparse
import re
import time
import sys
import cgi
import getpass
import os
####################################################################################################
#Arg Parsing
#Take user/password/search term.
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--user', default = 'invalid',  type=str, help='Github Username')
parser.add_argument('-t', '--term', default = 'invalid', type=str, help='Search Term')
parser.add_argument('-s', '--strict', default = 'off', type=str, help='Strict Searching: off || on')
args = parser.parse_args()

#Turn our args into vars
gitUser = args.user
gitTerm = args.term
gitPages = 0
gitStrict = args.strict
#This checks to make sure people filled out all of the args
if (gitUser == 'invalid' or gitTerm == 'invalid'):
	parser.print_help()
	sys.exit()
#This is for password input - it's invisible in the command line.
gitPass = getpass.getpass("GitHub Password: ")
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
if not os.path.exists(gitTerm + "/"):
	os.mkdir(gitTerm +"/")
f = open(gitTerm+ '/results_' + gitTerm + "_.html", 'w+')
while (counter < gitPages+1):
	with requests.Session() as session:
		try:
			with requests.Session() as session:
                		search = session.get('https://api.github.com/search/code?q='+gitTerm+'+in:file&page=' + str(counter), headers=header_text_highlite, auth=HTTPBasicAuth(gitUser, gitPass))
                		#Our results are stored in var data
                		data = search.text
                                #Load the results into the JSON parser
                                j = json.loads(data)
                                #This is really messy.  Sorry.  JSON parsing.
                                count = len(j["items"])
                                for x in range(0, count):
                                        string = ("<RESULT class='result'>")
                                        string +=("<b>REPO NAME: </b> " + j['items'][x]['repository']['name'])
                                        string +=("<br>")
                                        string +=("<b>FILE NAME: </b> " + j['items'][x]['name'])
                                        string +=("<br>")
                                        string +=("<b>URL: </b><a href=\" " + j['items'][x]['html_url'])
					string +=("\">LINK</a><br>")

					raw_url = (j['items'][x]['html_url'])
					raw_url = raw_url.replace('https://github.com', 'https://raw.githubusercontent.com')
					raw_url = raw_url.replace('/blob/', '/')
					string += ("<b>RAW: </b><a href=\"" + raw_url + "\">RAW_LINK</a><br>")

                                        m = re.search('github.com/(\w+.)/', j['items'][x]['html_url'])
                                        user = m.group(1)
                                        string +=("<b>USER: </b>" + user + "<br>")
					string +=("<b>SNIPPET: </b><pre> ") 
					code_string = (j['items'][x]['text_matches'][0]['fragment'])
					escaped = cgi.escape(code_string)
					string +=(escaped)
                                        string +=("</pre><br>")
                                        string +=("</RESULT>")
                                        string +=("<br><br>\n\n")
					#This is for 'strict searching' to remove 'fuzzy' results.  Needs to be a better way.
					if (gitStrict == 'on'): 
						if gitTerm in string:
							f.write(string)
					else:
						f.write(string)
					string = ""
                except Exception:
                        #We probably caught a rate limit
                        if "abuse-rate-limits" in data:
                                print ("RATE LIMITED!")
                                print("SLEEPING 60 SECONDS")
                                time.sleep(60)
                                print("RESUMING!")
                        pass
        #Increase our counter to change the search page to the next one 
        counter += 1
        print("CURRENT PAGE: "+ str(counter - 1)+ " of " + str(gitPages))

f.close()
####################################################################################################
print ("====FINISHED SEARCHING====")
response = raw_input("download raw code? y/n: ")
if (response == 'n'):
	exit()
else:
        filename = (gitTerm +'/results_' + gitTerm + "_.html")
	filepath = (gitTerm +'/')
	get_raw_results(filename, filepath)

