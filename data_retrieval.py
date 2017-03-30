from bsddb3 import db

def date_exact(date, da_database, da_cursor):
	
	correct_ids = []
	print("DATE" , date)
	date = date + '\r'
	db_key = date.encode('ascii','ignore')
	print("DBKEY" , db_key)
	value = da_database.get(db_key)
	print("Value from database",value)
	print("FIRST cursor value", da_cursor.first())
	
	value = da_cursor.get(db_key, db.DB_SET)
	print("Value from cursor",value)
	while (value != None):
		value = da_cursor.next_dup()
		print("Value from inside while",value)
		
	
	#print("________",value, "CUR", da_cursor.current())
	#value = da_cursor.next()
	#print(value[1].decode("utf-8"))
	#correct_ids.append(value[1].decode("utf-8"))
	#print("NEXT",da_cursor.next_dup())	
	#if (value == None):
	#	print("The date you were searhcing was not found.")
	#	return None
	#else:
#		#print(value)
#		correct_ids.append(value[1].decode("utf-8"))
#		#print(da_cursor.next_dup())
		
		#print("Return value of:", value.decode("utf-8"))
	return correct_ids
		
		
def date_less(date, da_database, da_cursor):
	
	correct_ids = []
	
	db_key = date.encode('ascii','ignore')
	data_dates = da_database.keys()
	
	for data_date in data_dates:
		if (data_date < db_key):		
			value = da_database.get(data_date)
			print("Return value of:", value.decode("utf-8"))
			correct_ids.append(value.decode("utf-8"))
	return correct_ids
	
def date_greater(date, da_database, da_cursor):
	
	correct_ids = []
	
	db_key = date.encode('ascii','ignore')
	data_dates = da_database.keys()
	for data_date in data_dates:
		if (data_date > db_key):		
			value = da_database.get(data_date)
			print("Return value of:", value.decode("utf-8"))
			correct_ids.append(value.decode("utf-8"))
			
	return correct_ids
			
def full_text(text, te_database, te_cursor):
	
	correct_ids = []
	
	search_term = "t-" + text
	db_key = search_term.encode('ascii','ignore')
	tweet = te_database.get(db_key)	
	print(tweet)
	correct_ids.append(tweet)
	return correct_ids


def full_name(name, te_database, te_cursor):
	
	correct_ids = []
	
	search_term = "n-" + name
	db_key = search_term.encode('ascii','ignore')
	tweet = te_database.get(db_key)	
	print(tweet)	
	correct_ids.append(tweet)
	
	return correct_ids


def full_location(location, te_database, te_cursor):
	
	correct_ids = []
	
	search_term = "l-" + location
	db_key = search_term.encode('ascii','ignore')
	tweet = te_database.get(db_key)	
	print(tweet)	
	correct_ids.append(tweet)
	
	return correct_ids


def partial_match(term, tw_database, tw_cursor):
	
	correct_ids = []
	
	db_key = term[:-1].encode('ascii','ignore')
	tweets = tw_database.values()
	#print(data_dates)
	for data_tweet in tweets:
		#if (data_date > db_key):
		tweet = data_tweet.decode("utf-8")
		#print(tweet[70:70+len(term)-1])
		if(tweet[71] == '@'):
			index = 0
			while (tweet[71 + index] != ' '):
				index += 1
			if tweet[71+index:71+index+len(term)] == term:
				correct_ids.append(tweet)
				
				print(tweet)
		else:
			if tweet[70:70+len(term)-1] == term[:-1]:
				correct_ids.append(tweet)
				
				print(tweet)	
	return correct_ids


def simple_term(term, te_database, te_cursor):
	
	correct_ids = []
	
	text_id = full_text(term, te_database, te_cursor)
	name_id = full_name(term, te_database, te_cursor)
	location_id = full_location(term, te_database, te_cursor)
	
	correct_ids.extend(text_id)
	correct_ids.extend(name_id)
	correct_ids.extend(location_id)
	#db_key = term.encode('ascii','ignore')
	#tweets = tw_database.values()
	#print(data_dates)
	#for data_tweet in tweets:
		#if (data_date > db_key):
	#	tweet = data_tweet.decode("utf-8")
	#	if term in tweet:
	#		print("Return value of:", tweet)
	#		correct_ids.append(tweet)
			
		#value = te_database.get(data_date)
		#.decode("utf-8"))
		
	return correct_ids		
	
	