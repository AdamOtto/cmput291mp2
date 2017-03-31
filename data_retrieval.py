from bsddb3 import db

def date_from_ints(year, month, day):
	if len(str(year)) > 4 or len(str(month)) > 2 or len(str(day)) > 2:
		return False
	return str(year).zfill(4) + '/' + str(month).zfill(2) + '/' + str(day).zfill(2)

def date_exact(date, da_database, da_cursor):
	
	correct_ids = []
	
	print("DATE" , date)
	#date = date + '\r'
	db_key = date.encode('ascii','ignore')
	print("DBKEY" , db_key)
	value = da_cursor.get(db_key, db.DB_SET)
	#print("Value from cursor",value)
	
	while (value != None):
		print("Return value:",value[1].decode("utf-8"))
		correct_ids.append(value[1].decode("utf-8"))
		value = da_cursor.next_dup()
		
		
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
	
	search_term = "t-" + text.lower() #+ "\r"
	db_key = search_term.encode('ascii','ignore')

	value = te_cursor.get(db_key, db.DB_SET)
	print("Value from cursor",value)
	while (value != None):
		print("Return value of:",value[1].decode("utf-8"))
		correct_ids.append(value[1].decode("utf-8"))
		value = te_cursor.next_dup()
	
	return correct_ids


def full_name(name, te_database, te_cursor):
	
	correct_ids = []
	
	search_term = "n-" + name.lower() #+ "\r"
	db_key = search_term.encode('ascii','ignore')
	
	value = te_cursor.get(db_key, db.DB_SET)
	#print("Value from cursor",value)
	while (value != None):
		print("Return value of:",value[1].decode("utf-8"))
		correct_ids.append(value[1].decode("utf-8"))
		value = te_cursor.next_dup()
	
	return correct_ids


def full_location(location, te_database, te_cursor):
	
	correct_ids = []
	
	search_term = "l-" + location.lower() #+ "\r"
	db_key = search_term.encode('ascii','ignore')
	value = te_cursor.get(db_key, db.DB_SET)
	#print("Value from cursor",value)
	
	while (value != None):
		print("Return value of",value[1].decode("utf-8"))
		correct_ids.append(value[1].decode("utf-8"))
		value = te_cursor.next_dup()
	
	return correct_ids	


#@TODO needs to be fixed
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

	print(correct_ids)	
	return correct_ids		
	
	
