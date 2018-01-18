import re
import socket
test_file = open("test.txt")
for line in test_file:
	line = line.rstrip()
	if re.search('^co+', line):
		print line

x = 'my 2 students: get scores of: 99 and 85'
emailadd = 'hello  wrk1231@gmail.com welcome to email me !'
y = re.findall('[0-9]+', x)
z1 = re.findall('^m.+?:', x)
z2 = re.findall('^m.+:', x)
extract_email = re.findall('\S+@(\S+)', emailadd)
extract_email2 = re.findall('@([\S]*)', emailadd)
extract_email3 = re.findall('@([^ ]*)', emailadd)
print extract_email,extract_email2,extract_email3
print z1,z2

GET http://www.dr-chunk.com/page1.htm HTTP/1.0 