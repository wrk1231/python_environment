import urllib.request,urllib.parse,urllib.error
from urllib import * 
import re
fhand = urllib.request.urlopen('http://www.dr-chuck.com/page1.htm')
counts = dict()
for line in fhand:
	line = line.decode().strip()
	another_site  = re.findall("href=\"([^ ]+)\"", line)
	if another_site:
		print(str(another_site[0]))


# 	words = line.decode().strip()
# 	for word in words:
# 		counts[word] = counts.get(word,0) + 1
# print(counts )
