import xml.etree.ElementTree as ET

'''
This function is used to gather all the data in the xml files provided on eclass.
'''
def readXMLFile(fileName):
    tree = ET.parse(fileName)
    root = tree.getroot()
    
    #Elements of the xml can be obtained through elements in root.
    #Ex: The first element can be reached with root[0][0].text => ID.

    #All of this code is used for testing and demonstrating how to access the data in the xml file.
    #This code can be commented out/in, it doesn't affect the functionality of the function. 
    ''' 
    for child in root:
        print("ID: " + child[0].text + 
        ", Created at: " + child[1].text +
        "\ntext: " + child[2].text)
        print("retweet count: " + child[3].text)
        #All of the users data is stored in root[i][4].
        #Some of these fields are empty, so a None check may be required.
        print("Name: " + child[4][0].text)
        print("Location: " + child[4][1].text)
        if child[4][2].text is not None:
            print("Description: " + child[4][2].text)
        if child[4][3].text is not None:
            print("URL: " + child[4][3].text)
        print("\n")
    '''
    return root


'''
This function creates a text file with all the terms in a tweet.  It arrages them as follows
t/n/l-Term:ID
Where t signifies the term is a tweet, n signifies the term is a name and l signifies the term is a location.
Term is the word that appears in the tweet/name/location
And ID is the tweet ID it orginated from.
'''
def createTermsTextFile(xmlData):
    term_file = open("terms.txt", "w")
    for status in xmlData:
        #Get the important data for writing
        text = removeSpecialCharFromString(status[2].text).split(" ")
        tweetID = status[0].text
        #Write out all the terms in the tweet <text>.
        for term in text:
            if len(term) > 2:
                term_file.write("t-" + term.lower() + ":" + tweetID + "\n")
        #Get all the terms in <name> and write the to the file.
        userName = removeSpecialCharFromString(status[4][0].text).split(" ")
        for name in userName:
            if len(name) > 2:
                term_file.write("n-" + name.lower() + ":" + tweetID + "\n")
        #Get all the terms in <location> and write the to the file.
        userLocation = removeSpecialCharFromString(status[4][1].text).split(" ")
        for location in userLocation:
            if len(location) > 2:
                term_file.write("l-" + location.lower() + ":" + tweetID + "\n")
    term_file.close()    

'''
This function creates the text file with the dates of all tweets. it is constructed as follows.
d:ID
where d is the date is form year/month/day => NOTE: I may be wrong.
and ID is the tweet ID
'''
def createDatesTextFile(xmlData):
    term_file = open("dates.txt", "w")
    for status in xmlData:
        #Get the important data for writing
        tweetID = status[0].text
        date = status[1].text
        term_file.write(date + ":" + tweetID + "\n")

    term_file.close() 


'''
This function creates the text file with ID of the tweet and the info in xml format. it is constructed as follows.
ID:rec
where ID is the tweet ID
and rec is the record in xml format
'''
def createTweetsTextFile(xmlData):
    term_file = open("tweets.txt", "w")
    for status in xmlData:
        #Construct the output string
        outputString = ""
        outputString += status[0].text
        outputString += ":<status> <id>"
        outputString += status[0].text
        outputString += "</id> <created_at>"
        outputString += status[1].text
        outputString += "</created_at> <text>"
        outputString += status[2].text
        outputString += "</text> <retweet_count>"
        outputString += status[3].text
        outputString += "</retweet_count> <user> <name>"
        outputString += status[4][0].text
        outputString += "</name> <location>"
        outputString += status[4][1].text
        outputString += "</location> <description>"
        if status[4][2].text is not None:
             outputString += status[4][2].text
        outputString += "</description> <url>"
        if status[4][3].text is not None:
             outputString += status[4][3].text
        outputString += "</url> </user> </status>\n"


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






