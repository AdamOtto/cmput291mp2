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
	
	Return the cleaned conditions list
	If the conditions are found to be condtradictory the result is None
	'''
	conditions.sort()
	
	
	#due to GREATER conditions, this is the minimum date of a query
	minYear = None
	minMonth = None
	minDay = None
	#due to LESS conditions, this is the maximum date of a query
	maxYear = None
	maxMonth = None
	maxDay = None
	
	for con in conditions:
		if con[0] == DATEGREATER:
			#invalidate Date> if its date is less than the current highest Date> date, the min date.
			if con[1] < minYear or
			(con[1] == minYear and con[2] < minMonth) or
			(con[1] == minYear and con[2] == minMonth and con[3] <= minDay):
				con[0] = INVALID
			else:
				minYear = con[1]
				minMonth = con[2]
				minDay = con[3]
		elif con[0] == DATELESS:
			#invalid Date< if its date is greater than the current lowest Date< date, the max date.
			if con[1] > maxYear or
			(con[1] == maxYear and con[2] > maxMonth) or
			(con[1] == maxYear and con[2] == maxMonth and con[3] >= maxDay):
				con[0] = INVALID
			else:
				maxYear = con[1]
				maxMonth = con[2]
				maxDay = con[3]
	#The whole query is invalid if the min date is greater than the max date
	if minYear >= maxYear and minMonth>= maxMonth and minDay >= maxDay:
		print("You appear to have entered a DATELESS that is less than a DATEGREATER, query invalidated")
		return None
	
	#At this point in the cleaning, we can be certain 
	#that there is only 1 dateless and 1 dategreater condition, whose dates are stored already.
	'''
	trying a more pythonic version of the below
	exactYear
	for con in conditions:
	'''
		
	'''
	exact_found = False
	for i in range(len(conditions)):
		#if we have found the first DATEEXACT and it's not the last condition
		if conditions[i][0] == DATEEXACT and i < len(conditions)-2:
			if conditions[i+1][0] == DATEEXACT and (
				conditions[i][1] != conditions[i+1][1] or 
				conditions[i][2] != conditions[i+1][2] or 
				conditions[i][3] != conditions[i+1][3]):
				#two DATEEXACTS with different dates, our conditions list is invalid
				print("You appear to have entered two different DATEEXACT queries, query invalided")
				return None
			exact_found == True
			#@TODO the following does not handle if the dategreater is greater, or the dateless is less
			#than the dateexact, which makes the conditions invalid, or
			if conditions[i+1][0] == DATELESS or conditions[i+1][0] == DATEGREATER:
				#DATEEXACT followed by GREATER or LESS, the remaining conditions are re
				conditions = conditions[0:i+1]
	'''
			
			
def parseConditions(conditions):
	'''
	Given a list of conditions, parses each one using Dyllan's query searching functions.
	To avoid too much memory usage, will get a query's list, then if there is another query
	it will AND it with that queries list before continuing.
	'''
	#@TODO get a date function in data_retrival that will turn the integer part dates passed back into a string
	first_time = True
	for con in conditions:
		current_results = []
		if con[0] == TEXT:
			current_results = full_text(con[2], con[1])
		elif con[0] == NAME:
			current_results = full_name(con[2], con[1])
		elif con[0] == LOCATION:
			current_results = full_location(con[2], con[1])
		elif con[0] == DATEEXACT:
			current_results = date_exact(year, month, day, db, cur)
		elif con[0] == DATELESS:
			current_results = date_less(year, month, day, db, cur)
		elif con[0] == DATEGREATER:
			current_results = date_greater(year, month, day, db, cur)
		elif con[0] == INVALID:
			continue
		else:
			print("ERROR IN CONDITION PARSING")
			
		if first_time:
			total_results = set(current_results)
			first_time = False
		else:
			total_results = total_results & set(current_results)