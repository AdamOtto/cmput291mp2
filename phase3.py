import re

def isDateQuery(string):
	'''
	Given a string, determines if it is a date query, 
	that is, it starts with 'date' and one of ':', '<' or '>'
	returns False if not, True if it is
	'''
	if string[0:4] == 'date' and (string[4] == ':' or string[4] == '<' or string[4] == '>'):
		return True
	return False

def isFullTermQuery(string):
	'''
	Given a string, determines if it is a full term query,
	that is, it starts with one of 'text', 'name' or 'location' and
	then ':'
	
	If not, it is possible that this is a simple term query, which is
	just the term itself, eg 'germany'
	'''
	if (string[0:4] == 'text' or string[0:4] == 'name') and string[4] == ':':
		return True
	if string[0:8] == 'location' and string[8] == ':':
		return True
	return False

def isAlphaNumeric(string):
	'''
	Returns true if all chars in string are one of 0-9, a-z, A-Z, or _
	'''
	#checks for any character outside the parameters
	pattern = re.compile('[^0-9a-zA-Z_]')
	value = pattern.search(string)
	if value:
		return False
	return True

#Enumerate some query types
TEXT = 1
NAME = 2
LOCATION = 3
DATEEXACT = 4
DATELESS = 5
DATEGREATER = 6

print('Welcome to Phase 3 for Mini Project 2')

while True:
	queries = input('Please enter your query: ')
	#Queries must be case insensitive
	queries = queries.lower()
	#Queries can potentially be all passed at once, must process individually according to grammar
	queries = queries.split()
	for query in queries:
		if isDateQuery(query):
			#Find the query type and strip the type from the query
			date = query[5:]
			if query[4] == ':':
				qtype = DATEEXACT
			elif query[4] == '<':
				qtype = DATELESS
			elif query[4] == '>':
				qtype = DATEGREATER
			
			dates = date.split('/')
			if len(dates) != 3:
				print('You had a proper date query prefix, but this date is not formatted right: ', date)
				continue
			year = dates[0]
			month = dates[1]
			day = dates[2]
			if not year.isdigit() or not month.isdigit() or not day.isdigit():
				print('One of these date values is not a number: ', year, ', ',month,',',day)
				continue
			print('You have a date query of type: ', qtype)
			print('Looking for year = ' + year)
			print('Looking for month = ' + month)
			print('Looking for day = ' + day)
		elif isFullTermQuery(query):
			#Find the query type and strip the type from the query
			if query[0:4] == 'text':
				term = query[5:]
				qtype = TEXT
			elif query[0:4] == 'name':
				term = query[5:]
				qtype = NAME
			elif query[0:8] == 'location':
				term = query[9:]
				qtype = LOCATION
			
			#is this a termPattern query?
			if isAlphaNumeric(term[:-1]) and term[-1] == '%':
				print('This query is a prefix full term query')
			elif isAlphaNumeric(term):
				print('This is a non-prefix full term query')
			else:
				print('This full-term query has a proper type, but this term is improper: ', term)
		elif isAlphaNumeric(query):
			print('You have a simple term query')
		else:
			print('This is not a valid query: ' + query)
		



