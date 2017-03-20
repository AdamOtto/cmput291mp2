import xml.etree.ElementTree as ET

'''
This function is used to gather all the data in the xml files provided on eclass.

Will read line by line the xml file and print the results into three text files.
'''
def readXMLFile(fileName):

    with open(fileName, 'r') as xmlFile:
        for line in xmlFile:
           if (line.find("<status>") is 0):
               #first, get the necessary information for createTweetsTextFile
               ID = line[line.find("<id>") + len("<id>"):line.find("</id>")]
               createTweetsTextFile(ID, line)
               
               createTermsTextFile(ID, line)

               createDatesTextFile(ID, line[line.find("<created_at>") + len("<created_at>"):line.find("</created_at>")])
    return

'''
This function creates a text file with all the terms in a tweet.  It arrages them as follows
t/n/l-Term:ID
Where t signifies the term is a tweet, n signifies the term is a name and l signifies the term is a location.
Term is the word that appears in the tweet/name/location
And ID is the tweet ID it orginated from.
'''
def createTermsTextFile(tweetID, xmlData):
    term_file = open("terms.txt", "a")
    outputString = ""
    
    #Get all the terms in the text
    text = xmlData[xmlData.find("<text>") + len("<text>"): xmlData.find("</text>")]
    text = removeSpecialCharFromString(text).split(" ")
    for term in text:
        if len(term) > 2:
            outputString += "t-" + term.lower() + ":" + tweetID + "\n"

    #Get all the terms in the name
    text = xmlData[xmlData.find("<name>") + len("<name>"): xmlData.find("</name>")]
    text = removeSpecialCharFromString(text).split(" ")
    for name in text:
            if len(name) > 2:
                outputString += "n-" + name.lower() + ":" + tweetID + "\n"
    
    #Get all the terms in the location
    text = xmlData[xmlData.find("<location>") + len("<location>"): xmlData.find("</location>")]
    text = removeSpecialCharFromString(text).split(" ")
    for location in text:
            if len(location) > 2:
                outputString += "l-" + location.lower() + ":" + tweetID + "\n"

    #Print to the text file.
    term_file.write(outputString)
    term_file.close()    

'''
This function creates the text file with the dates of all tweets. it is constructed as follows.
d:ID
where d is the date is form year/month/day => NOTE: I may be wrong.
and ID is the tweet ID
'''
def createDatesTextFile(tweetID, xmlData):
    term_file = open("dates.txt", "a")
    term_file.write(xmlData + ":" + tweetID + "\n")
    term_file.close() 


'''
This function creates the text file with ID of the tweet and the info in xml format. it is constructed as follows.
ID:rec
where ID is the tweet ID
and rec is the record in xml format
'''
def createTweetsTextFile(ID, xmlData):
    term_file = open("tweets.txt", "a")
    outputString = ID + ":" + xmlData
    term_file.write(outputString)
    term_file.close() 


'''
Removes all characters from a string that aren't [0-9a-zA-Z_]
If a character doesn't match, it will be replace with whitespace.
Ex: 
doop = removeSpecialCharFromString("Th@is is $a$ dir&ty St(r)in-g.")
doop = Th is is  a  dir ty St r in g
'''
def removeSpecialCharFromString(dirtyString):
    cleanString = ""
    for char in dirtyString:
        #is char 0-9
        if (ord(char) >= 48 and ord(char) <= 57):
            cleanString += char
        #is char a-z
        elif (ord(char) >= 97 and ord(char) <= 122):
            cleanString += char
        #is char A-Z
        elif (ord(char) >= 65 and ord(char) <= 90):
            cleanString += char
        #is char A-Z
        elif char is " ":
            cleanString += char
        else:
            cleanString += " "
    return cleanString






