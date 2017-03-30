from xmlReader import *

#Dont put in an incorrect file name or the program will crash
#data = readXMLFile('wrongFileName.txt')
fileName = input("Please type in the .xml file you would like to extract from:")
readXMLFile(fileName)
print("done.\nTo sort the files and remove duplicates type in the following into your terminal.\nsort fileName.txt | uniq > newFileName.txt")
