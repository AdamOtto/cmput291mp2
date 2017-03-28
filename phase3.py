import re
print('Welcome to Phase 3 for Mini Project 2')

while True:
	queries = input('Please enter your query: ')
	#Queries must be case insensitive
	queries = queries.lower()
	#Queries can potentially be all passed at once, must process individually according to grammar
	queries = queries.split()
	for query in queries:
		if isDateQuery(query):
			print('You have a date query')
		elif isFullTermQuery(query):
			print('You have a full term query')
		elif isAlphaNumeric(query):
			print('You have a simple term query')
		else:
			print('This is not a valid query: ' + query)
		

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
	value = pattern.seach(string)
	if value:
		return False
	return True

