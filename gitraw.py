import mechanize
import re

def get_raw_results(filename):
	f = open('filename', 'r')
	w = open('
	for line in f:
		m = re.search(r'((https://raw.githubusercontent.com.+)\">)', line)
		if m:
			link = m.group(2)
			print(link)
