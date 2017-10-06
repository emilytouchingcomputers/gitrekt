#TODO
#Download each raw file and then sort them by username or something?
#
import mechanize
import re

def get_raw_results(filename, filepath):
	f = open(filename, 'r')
	w = open(filepath + 'output.txt', 'w')
	for line in f:
		m = re.search(r'((https://raw.githubusercontent.com.+)\">)', line)
		if m:
			link = m.group(2)
			w.write(link +'\n')
