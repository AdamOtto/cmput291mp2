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
INVALID = -1
TEXT = 1
NAME = 2
LOCATION = 3
GENERAL = 4
DATEEXACT = 5
DATELESS = 6
DATEGREATER = 7
'''

def cleanConditions(conditions):
	'''
	Takes a list of conditions and removes redundant conditions
	1. if multiple DATEEXACT conditions are present and the dates are not equal make the conditions list = None
	2. @TODO removes redundant greater or less than conditions
	THIS RELIES ON THE FACT THAT THE CONSTANTS FOR QTYPE ARE ENUMERATED AS LISTED IN THE ABOVE SPEC
	'''
	conditions.sort()
	
	#@TODO make this find max and min dates to clean off redundant LESS and GREATER then conditions
	'''
	#due to GREATER conditions, this is the minimum date of a query
	minYear = None
	minMonth = None
	minDay = None
	#due to LESS conditions, this is the maximum date of a query
	maxYear = None
	maxMonth = None
	maxDay = None
	
	for con in conditions:
		if con[0] == DATELESS:
			if con[1] < maxYear
				con[0] = INVALID
		elif con[0] == DATEGREATER:
	'''
			
	invalid = False
	for i in range(len(conditions)):
		#if we have found the first DATEEXACT and it's not the last condition
		if conditions[i][0] == DATEEXACT and i < len(conditions)-2:
			if conditions[i+1][0] == DATEEXACT and (
				conditions[i][1] != conditions[i+1][1] or 
				conditions[i][2] != conditions[i+1][2] or 
				conditions[i][3] != conditions[i+1][3]):
				#two DATEEXACTS with different dates, our conditions list is invalid
				invalid = True
				break
			#@TODO the following does not handle if the dategreater is greater, or the dateless is less
			#than the dateexact, which makes the conditions invalid, or 
			'''
			if conditions[i+1][0] == DATELESS or conditions[i+1][0] == DATEGREATER:
				#DATEEXACT followed by GREATER or LESS, the remaining conditions are re
				conditions = conditions[0:i+1]
			'''
			
def parseConditions(conditions):
	'''
	Given a list of conditions, parses each one using Dyllan's query searching functions.
	Too avoid too much memory usage, will get a query's list, then if there is another query
	will AND it with that queries list before continuing.
	'''
	#@TODO
	pass