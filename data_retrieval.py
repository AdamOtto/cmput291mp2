from bsddb3 import db

#Takes the integers year, month and day an converts it to a string of the form
# YYYY/MM/DD and will return an error if the int is too big 
def date_from_ints(year, month, day):


	if len(str(year)) > 4 or len(str(month)) > 2 or len(str(day)) > 2:
		return False
	return str(year).zfill(4) + '/' + str(month).zfill(2) + '/' + str(day).zfill(2)


#This function return the ids of tweets that match the date given	
def date_exact(year, month, day, da_database, da_cursor): 
	
	date = date_from_ints(year, month, day)
	if date == False:
		print('You had a proper date query prefix, but this date is not formatted right: ', date)
	
	correct_ids = []
	
	db_key = date.encode('ascii','ignore')
	value = da_cursor.get(db_key, db.DB_SET)
	
	while (value != None):
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
	
	current = da_cursor.set_range(db_key)
	
	while current:
		correct_ids.append(current[1].decode("utf-8"))
		current = da_cursor.next()
	
	return correct_ids
	
			

#given a query that specifies text at the start, this function returns the ids
# of tweets with that term in there text
def full_text(text, prefix, te_database, te_cursor): 
	
	correct_ids = []
	
	search_term = "t-" + text.lower()
	
	if prefix == True:
		correct_ids = partial_match(search_term, te_database, te_cursor)
		
	else:	
		db_key = search_term.encode('ascii','ignore')
		
		value = te_cursor.get(db_key, db.DB_SET)
		
		while (value != None):
			correct_ids.append(value[1].decode("utf-8"))
			value = te_cursor.next_dup()

	return correct_ids


#given a query that specifies name at the start, this function returns the ids
# of tweets with that term in there name
def full_name(name, prefix, te_database, te_cursor):
	
	correct_ids = []
	
	search_term = "n-" + name.lower()
	
	if prefix == True:
		correct_ids = partial_match(search_term, te_database, te_cursor)
		
	else:	
		db_key = search_term.encode('ascii','ignore')
		value = te_cursor.get(db_key, db.DB_SET)

		while (value != None):
			correct_ids.append(value[1].decode("utf-8"))
			value = te_cursor.next_dup()

	return correct_ids


#given a query that specifies location at the start, this function returns the ids
# of tweets with that term in there location
def full_location(location, prefix, te_database, te_cursor):
	
	correct_ids = []
	
	search_term = "l-" + location.lower()
	if prefix == True:
		correct_ids = partial_match(search_term, te_database, te_cursor)
		
	else:
		db_key = search_term.encode('ascii','ignore')
		value = te_cursor.get(db_key, db.DB_SET)
		
		while (value != None):
			correct_ids.append(value[1].decode("utf-8"))
			value = te_cursor.next_dup()
	
	return correct_ids	


#given a query that has a % at the end will match the characters before that
# to the given term keys, returning ids of the tweets.
def partial_match(term, te_database, te_cursor):
	
	correct_ids = []
	
	db_key = term.encode('ascii','ignore')
	value = te_cursor.set_range(db_key, db.DB_SET)
	t_length = len(term)
	
	while value and value[0].decode("utf-8")[:t_length] == term:
		correct_ids.append(value[1].decode("utf-8"))
		value = te_cursor.next()
	
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
		
	return correct_ids		


#get_tweet
#Returns a list with all the information regarding a single tweet.
#Handles the '\r' at the end of returned ID's.
def get_tweet(current_id, tw_database, tw_cursor):
	#Encode the ID into a key and remove that pesky \r
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
