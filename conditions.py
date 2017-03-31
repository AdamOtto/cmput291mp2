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
INVALID = -1
TEXT = 1
NAME = 2
LOCATION = 3
GENERAL = 4
DATEEXACT = 5
DATELESS = 6
DATEGREATER = 7


def cleanConditions(conditions):
	'''
	Takes a list of conditions and removes redundant conditions
	1. if multiple DATEEXACT conditions are present and the dates are not equal make the conditions list = None
	2. removes redundant greater or less than conditions
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
			if minYear == minMonth == minDay == None:
				minYear = con[1]
				minMonth = con[2]
				minDay = con[3]
			elif con[1] < minYear or
			(con[1] == minYear and con[2] < minMonth) or
			(con[1] == minYear and con[2] == minMonth and con[3] <= minDay):
				con[0] = INVALID
			else:
				minYear = con[1]
				minMonth = con[2]
				minDay = con[3]
		elif con[0] == DATELESS:
			#invalid Date< if its date is greater than the current lowest Date< date, the max date.
			if maxYear == maxMonth == maxDay == None:
				maxYear = con[1]
				maxMonth = con[2]
				maxDay = con[3]
			elif con[1] > maxYear or
			(con[1] == maxYear and con[2] > maxMonth) or
			(con[1] == maxYear and con[2] == maxMonth and con[3] >= maxDay):
				con[0] = INVALID
			else:
				maxYear = con[1]
				maxMonth = con[2]
				maxDay = con[3]
	#The whole query is invalid if the min date is greater than the max date
	if minYear is not None and maxYear is not None and 
	minYear >= maxYear and minMonth>= maxMonth and minDay >= maxDay:
		print("You appear to have entered a DATELESS that is less than a DATEGREATER, query invalidated")
		return None
	
	#At this point in the cleaning, we can be certain 
	#that there is a max of 1 dateless and 1 dategreater condition, whose dates are stored already.
	
	#remove redundant exact dates
	exactYear = None
	exactMonth = None
	exactDay = None
	for con in conditions:
		if con[0] = DATEEXACT:
			if exactYear == exactMonth == exactDay == None:
				#first exactdate condition, set the exact date
				exactYear = con[1]
				exactMonth = con[2]
				exactDay = con[3]
			elif exactYear == con[1] and exactMonth == con[2] and exactDay == con[3]:
				#redundant exactdate condition, invalidate condition
				con[0] = INVALID
			else:
				#contradictory exactdates, all conditions invalid
				print("You have entered two contradicting DATEEXACT dates, query invalidated")
				return None
	
	#We now have a maximum of 1 of each date type query, the Date> and Date< have 
	#been bounds checked, all that remains is a bounds check on the exact vs < and >
	
	if exactYear is not None:
		if minYear is not None:
			if exactYear < minYear and exactMonth < minMonth and exactDay < minDay:
				print("You have entered an DATEEXACT less than a DATEGREATER, query invalidated")
				return None
		if maxYear is not None:
			if exactYear > maxYear and exactMonth < maxMonth and exactDay < maxDay:
				print("You have entered an DATEEXACT more than a DATELESS, query invalidated")
				return None
		# If we made it this far, there is a single valid dateexact, all other date conditions are invalid
		for con in conditions:
			if con[0] == DATELESS or con[0] == DATEGREATER:
				con[0] = INVALID
	
	#Invalid dates parsed out, we now sort the list from least likely to have large outputs, to most
	def sortKey(condition):
		'''
		Given a condition, returns a tuple of values that when sorted will make the least likely
		to have large outputs condition come before those that are more likely.
		The key is a list of 5 values, if a key value doesn't apply, it's value is 0
		[is not an exact query, -(term length), year, month, day]
		'''
		if condition[0] in [TEXT, NAME, LOCATION]:
			if condition[1] == True:
				return [1, -len(condition[2]), 0, 0, 0]
			return [0, -len(condition[2]), 0, 0, 0]
		if condition[0] == DATEEXACT:
			return [0, 0, condition[1], condition[2], condition[3]]
		if condition in [DATELESS, DATEGREATER]:
			return [1, 0, condition[1], condition[2], condition[3]]
		return [2, 0, 0, 0, 0] #For INVALID queries
	
	#create a new list of conditions, sorted by the above criteria
	output = sorted(conditions, key = sortKey)
	return output
				
	
	
			
			
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