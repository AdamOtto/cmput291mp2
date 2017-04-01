from bsddb3 import db

#Takes the integers year, month and day an converts it to a string of the form
# YYYY/MM/DD and will return an error if the int is too big 
def date_from_ints(year, month, day):


	if len(str(year)) > 4 or len(str(month)) > 2 or len(str(day)) > 2:
		return False
	return str(year).zfill(4) + '/' + str(month).zfill(2) + '/' + str(day).zfill(2)


#This function return the ids of tweets that match the date given
#def date_exact(date, da_database, da_cursor):

#----------comments at the start of dates are for new implementation -----------	
def date_exact(year, month, day, da_database, da_cursor): 
	
	date = date_from_ints(year, month, day)
	if date == False:
		print('You had a proper date query prefix, but this date is not formatted right: ', date)
	
	correct_ids = []
	
	#print("DATE" , date)
	#date = date + '\r'
	db_key = date.encode('ascii','ignore')
	#print("DBKEY" , db_key)
	value = da_cursor.get(db_key, db.DB_SET)
	#print("Value from cursor",value)
	
	while (value != None):
		#print("Return value:",value[1].decode("utf-8"))
		correct_ids.append(value[1].decode("utf-8"))
		value = da_cursor.next_dup()
		
	return correct_ids


#this function returns all ids of tweets which dates are less than the one specified	
#def date_less(date, da_database, da_cursor):
	
def date_less(year, month, day, da_database, da_cursor):
   
    date = date_from_ints(year, month, day)
    if date == False:
        print('You had a proper date query prefix, but this date is not formatted right: ', date)  
   
    correct_ids = []
    db_key = date.encode('ascii','ignore')
    print("db_key: " + str(db_key))
    #data_dates = da_database.keys()
    #print("data_dates: " + str(data_dates))
    #for data_date in data_dates:
    #   if (data_date < db_key):
    #       value = da_database.get(data_date)
    #       correct_ids.append(value.decode("utf-8"))
    #       #value = da_cursor.next_dup()
	
    current = da_cursor.set_range(db_key)
    current = da_cursor.prev()
    i = 0
    while current:
        correct_ids.append(current[1].decode("utf-8"))
        current = da_cursor.prev()
    return correct_ids
	
	
	
#this function returns all ids of tweets which dates are greater than the one specified	
#def date_greater(date, da_database, da_cursor):
	
def date_greater(year, month, day, da_database, da_cursor): 
	
	date = date_from_ints(year, month, day+1)
	if date == False:
		print('You had a proper date query prefix, but this date is not formatted right: ', date)	
	
	correct_ids = []
	
	db_key = date.encode('ascii','ignore')
	
	#This method does not account for the fact that there are duplicate keys for dates.
	'''
	data_dates = da_database.keys()
	for data_date in data_dates:
		if (data_date > db_key):		
			value = da_database.get(data_date)
			#print("Return value of:", value.decode("utf-8"))
			correct_ids.append(value.decode("utf-8"))
		
	return correct_ids
	'''
	
	current = da_cursor.set_range(db_key)
	#print(current)
	while current:
		correct_ids.append(current[1].decode("utf-8"))
		current = da_cursor.next()
	
	return correct_ids
	
			

#given a query that specifies text at the start, this function returns the ids
# of tweets with that term in there text
def full_text(text, prefix, te_database, te_cursor): 
	
	correct_ids = []
	
	search_term = "t-" + text.lower() #+ "\r"
	
	if prefix == True:
		correct_ids = partial_match(search_term, te_database, te_cursor)
		
	else:	
		db_key = search_term.encode('ascii','ignore')
		
		value = te_cursor.get(db_key, db.DB_SET)
		#print("Value from cursor",value)
		while (value != None):
			#print("Return value of:",value[1].decode("utf-8"))
			correct_ids.append(value[1].decode("utf-8"))
			value = te_cursor.next_dup()

	return correct_ids


#given a query that specifies name at the start, this function returns the ids
# of tweets with that term in there name
def full_name(name, prefix, te_database, te_cursor):
	
	correct_ids = []
	
	search_term = "n-" + name.lower() #+ "\r"
	
	if prefix == True:
		correct_ids = partial_match(search_term, te_database, te_cursor)
		
	else:	
		db_key = search_term.encode('ascii','ignore')
		
		value = te_cursor.get(db_key, db.DB_SET)
		#print("Value from cursor",value)
		while (value != None):
			#print("Return value of:",value[1].decode("utf-8"))
			correct_ids.append(value[1].decode("utf-8"))
			value = te_cursor.next_dup()

	return correct_ids


#given a query that specifies location at the start, this function returns the ids
# of tweets with that term in there location
def full_location(location, prefix, te_database, te_cursor):
	
	correct_ids = []
	
	search_term = "l-" + location.lower() #+ "\r"
	if prefix == True:
		correct_ids = partial_match(search_term, te_database, te_cursor)
		
	else:
		db_key = search_term.encode('ascii','ignore')
		value = te_cursor.get(db_key, db.DB_SET)
		#print("Value from cursor",value)
		
		while (value != None):
			#print("Return value of",value[1].decode("utf-8"))
			correct_ids.append(value[1].decode("utf-8"))
			value = te_cursor.next_dup()
	
	return correct_ids	


#given a query that has a % at the end will match the characters before that
# to the given term keys, returning ids of the tweets.
def partial_match(term, te_database, te_cursor):
	
	correct_ids = []
	
	#db_key = term[:-1].encode('ascii','ignore')
	#te_database.set_bt_compare(te_database, db_key);
	#search_term = "t-" + term.lower()[:-1] #+ "\r"
	keys = te_database.keys()
	#print(data_dates)
	for key in keys:
		#if (data_date > db_key):
		search_key = key.decode("utf-8")
		#print("TERM",search_term)
		#print("KEY",search_key)
		#print (search_key[2:])
		if term in search_key:
			#db_key = search_key.encode('ascii','ignore')
			value = te_cursor.get(key, db.DB_SET)
			#print("Value from cursor",value)
			
			while (value != None):
				print("Return value of",value[1].decode("utf-8"))
				if value[1].decode("utf-8") in correct_ids:
					value = te_cursor.next_dup()
					continue
				
				correct_ids.append(value[1].decode("utf-8"))
				print("SEARCH",term)
				print("VALUE",value[0].decode("utf-8"))				
				value = te_cursor.next_dup()
				#if search_term in value[0].decode("utf-8"):
				#	print("SEARCH",search_term)
				#	print("VALUE",value[0].decode("utf-8"))
				#	continue
				#else:
				#	break
			#break
			
			
	print(correct_ids)
	return correct_ids


#If no specific term is specified, searches and returns ids from all of them.
def simple_term(term, te_database, te_cursor):
	
	correct_ids = []
	
	text_id = full_text(term, False, te_database, te_cursor)
	name_id = full_name(term, False, te_database, te_cursor)
	location_id = full_location(term, False, te_database, te_cursor)
	
	correct_ids.extend(text_id)
	correct_ids.extend(name_id)
	correct_ids.extend(location_id)
	
	#print(correct_ids)	
	return correct_ids		

#get_tweet
#Returns a list with all the information regarding a single tweet.
#Handles the '\r' at the end of returned ID's.
def get_tweet(current_id, tw_database, tw_cursor):
	#Encode the ID into a key and remove that pesky \r
	#db_key = current_id[:len(current_id) - 1].encode('ascii','ignore')
	db_key = current_id.encode('ascii','ignore')

	#Fetch the tweet from the hash table.
	result = tw_database.get(db_key)	
	result = result.decode("utf-8")

	#Seperate out the individual elements for easy displaying later
	TweetComponents = [""] * 8
	TweetComponents[0] = result[result.find("<id>") + len("<id>"):result.find("</id>")]
	TweetComponents[1] = result[result.find("<name>") + len("<name>"):result.find("</name>")]
	TweetComponents[2] = result[result.find("<location>") + len("<location>"):result.find("</location>")]
	TweetComponents[3] = result[result.find("<created_at>") + len("<created_at>"):result.find("</created_at>")]
	TweetComponents[4] = result[result.find("<retweet_count>") + len("<retweet_count>"):result.find("</retweet_count>")]
	TweetComponents[5] = result[result.find("<description>") + len("<description>"):result.find("</description>")]
	TweetComponents[6] = result[result.find("<url>") + len("<url>"):result.find("</url>")]
	TweetComponents[7] = result[result.find("<text>") + len("<text>"):result.find("</text>")]
	return TweetComponents

#displayResults
#Given a list of ID's, searches for the tweet info from the tw_db and displays the tweet info to the screen.
def displayResults(correct_ids, tw_database, tw_cursor):
	print("Query Results:")
	for ids in correct_ids:
		tweet = get_tweet(ids, tw_database, tw_cursor)
		print("ID: " + tweet[0])
		print("Username: " + tweet[1])
		print("Location: " + tweet[2])
		print("Created: " + tweet[3])
		print("retweeted: " + tweet[4] + " time(s)")
		print("Description: " + tweet[5])
		print("URL: " + tweet[6])
		print("Text: " + tweet[7] + "\n")
