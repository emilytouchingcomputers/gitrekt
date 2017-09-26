f = open('results_gsm1900.org_.html', 'r+')
e = open('results_filtered.html', 'w')
d = f.readlines()
f.seek(0)
for line in d:
	if "term" not in line:
		e.write(line)
f.close()
e.close
