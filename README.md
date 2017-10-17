GitRekt
===================
**github code search recon tool**

Use
-------------

python gitrekt.py -u github_username -t search_term -s on -w wordlist.txt

> **Args:**
> - -**u**: 'github username'.  Your github username.
> - -**t**: 'search term'.  Whatever you want to search for.  i.e. "google.com"
> - -**s**: 'strict search'.  Only returns a match if it's 1:1 for your search term, i.e. "google.com" won't return com.google 
> - -**w** 'wordlist'.  "Banned" words. Use this to filter out words or repo names.  If you get a lot of hits for "HTTPS-Everywhere" and don't want them in your results, just add HTTPS-Everywhere to a text file and pass that file in with the -w arg.
