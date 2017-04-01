import re
from bsddb3 import db
from data_retrieval import *
from conditions import *

tw_database = db.DB()
tw_database.set_flags(db.DB_DUP)
tw_database.open('tw.idx',None, db.DB_HASH, db.DB_CREATE)
tw_cursor = tw_database.cursor()

te_database = db.DB()
te_database.set_flags(db.DB_DUP)
te_database.open('te.idx',None, db.DB_BTREE, db.DB_CREATE)
te_cursor = te_database.cursor()

da_database = db.DB()
da_database.set_flags(db.DB_DUP)
da_database.open('da.idx',None, db.DB_BTREE, db.DB_CREATE)
da_cursor = da_database.cursor()


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
	if (string[0:5] == 'text:' or string[0:5] == 'name:'):
		return True
	if string[0:9] == 'location:':
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


'''
A set of queries produces a conditions list, with the following spec for each condition:
[qtype, info...]
where each condition by qtype looks like:
[TEXT, prefix?, term]
[NAME, prefix?, term]
[LOCATION, prefix?, term]
[GENERAL, term]
[DATEEXACT, year, month, day]
[DATELESS, year, month, day]
[DATEGREATER, year, month, day]

prefix? is True if a prefix term, False if not
term is a string
year, month and day are integers

and the qtypes are enumerated as:
'''
#Enumerate some query types
INVALID = -1
TEXT = 1
NAME = 2
LOCATION = 3
GENERAL = 4
DATEEXACT = 5
DATELESS = 6
DATEGREATER = 7

print('Welcome to Phase 3 for Mini Project 2')

while True:
	conditions = []
	queries = input('Please enter your query (Enter nothing to exit): ')
	
	if not queries:
		print("Exiting phase 3")
		break
	
	#Queries must be case insensitive
	queries = queries.lower()
	
	#Queries can potentially be all passed at once, must process individually according to grammar
	queries = queries.split()
	
	for query in queries:
		results = []
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
			
			conditions.append([qtype, int(year), int(month), int(day)])
			
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
				
			if not term:
				print("You didn't enter any input so the results are empty!")
				pass
							
			elif isAlphaNumeric(term[:-1]) and term[-1] == '%':	
							
				conditions.append([qtype, True, term[:-1]])
				
			elif isAlphaNumeric(term):
				conditions.append([qtype, False, term])
				
			else:
				print('This full-term query has a proper type, but this term is improper: ', term)
				continue
		elif isAlphaNumeric(query):					
			conditions.append([GENERAL, query])
			
		else:
			print('This is not a valid query: ' + query)


	results = list(parseConditions(conditions, te_database, te_cursor, da_database, da_cursor))
	results.sort()
	print("\nQUERY RESULTS -------------------------------\n")
	displayResults(results, tw_database, tw_cursor)

	print("Query Finished, ", len(results), " results found")

	
tw_cursor.close()
te_cursor.close()
da_cursor.close()
tw_database.close()
te_database.close()
da_database.close()	



