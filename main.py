from xmlReader import *

#Dont put in an incorrect file name or the program will crash
#data = readXMLFile('wrongFileName.txt')
data = readXMLFile('10.txt')
print("I just read an XML file!")

createTermsTextFile(data)
createDatesTextFile(data)
createTweetsTextFile(data)
print("I just wrote three files")

