#!/usr/bin/python3.6

#searchProgram.py
#started 12/21/2017


#basic functionality works. 
#DONE 12/21/2017 - add case insensitive
#DONE 01/05/2018 - add search sub-directories
#DONE 01/05/2018 - add command line argument for starting directory
#TODO add print file details size, modify date, permissions command line argument
#DONE 06/13/2018 - print file size in human readable format rounded to two decimal places
#NOT NEEDED BASH CAN DO THIS - add command line argument to open file using default application
#DONE 01/08/2018 - cleanup printout is bit messy
#DONE 02/19/2018 - BUG: When using the specify directory command line argument the print on screen has an extra '/' appended to the output
#TODO add functionality to search within files with a command line arugument
#TODO BUG: when NOT using the -s switch directories and files are not printed with the identifier
#TODO notify the user they are searching within sub directories  
#DONE 02/19/2018 - display to the user what the start directory is
#
#
#


import os  #for file system access
import sys #for command line arguments
#text = sys.argv[1].lower()

searchInSubDir = False
startPoint = os.getcwd()

if len(sys.argv)<2:
    print('Usage: searchProgram.py [searchTerm] [arguments] [startDirectory]')
    print('-s or --sub to include subdirectories')
    sys.exit()

if len(sys.argv)>2:
#    startPoint=os.getcwd()
    if sys.argv[2].lower() == '-s' or sys.argv[2].lower() == '--sub':
            searchInSubDir=True
#            startPoint==os.getcwd()
if len(sys.argv)==4:
    startPoint=sys.argv[3]
    if startPoint[-1] == '/':
        startPoint=startPoint[:-1]

#startPoint=os.getcwd()
searchString=sys.argv[1].lower()




#define functions that are the main body of the program

def searchCurrentDirectoryOnly(searchString):
    results=False
    for fileName in os.listdir():
        fileNameLower=fileName.lower()
        if searchString in fileNameLower:
            results=True
            print(fileName)
    if results!=True:
        print('None\n')
        print('Try searching sub directories with -s or --sub\n')
        print('Usage: searchProgram.py [searchTerm] [arguments]')

#define function to return size of a file in a human readable string
#fileLocation is assumed to be a string of the full path and filename
def getFileSize(fileLocation):
    fileSize=os.path.getsize(fileLocation)
    if fileSize < 1000:
        return str(fileSize)+'B'
    elif fileSize < 1000000:
        fileSize = round(fileSize/1000,2)
        return str(fileSize)+'kB'
    elif fileSize < 1000000000:
        fileSize = round(fileSize/1000000,2)
        return str(fileSize)+'MB'
    elif fileSize < 1000000000000:
        fileSize = round(fileSize/1000000000,2)
        return str(fileSize)+'GB'
    elif fileSize < 1000000000000000:
        fileSize = round(fileSize/1000000000000,2)
        return str(fileSize)+'TB'
    else:
        return 'HUGE FILE'

def searchDirectory(startPoint, searchString):
#    print('Starting in: '+startPoint)
#    print('searchString is: '+searchString)
    for fileName in os.listdir(startPoint):
#        print(fileName)
#        if os.path.isdir(fileName):
        if os.path.isdir(startPoint+'/'+fileName):
            if searchString in fileName.lower():
#                print(fileName+'     in '+startPoint)
#                print('Directory: '+startPoint+'/'+fileName)
                print('Dir: '+startPoint+'/'+fileName)
#            print('startPoint is: '+startPoint)
            searchDirectory(startPoint+'/'+fileName, searchString)
        elif searchString in fileName.lower():
#            print('File: '+fileName+'     in '+startPoint)
#            print('Fil: '+startPoint+'/'+fileName)
#            size=os.path.getsize(os.path.join(startPoint,fileName))
            size=getFileSize(os.path.join(startPoint,fileName))
            print(size,'File: '+startPoint+'/'+fileName)

text = sys.argv[1].lower()

#clear screen first using ANSI VT100 clear screen code
#Note: This will only work in a Linux/Unix terminal or emulator
print("\033[H\033[J")



#print search location
print('Searching for filenames containing:', searchString)
#print('in:', os.getcwd())
print()
print('Starting in Directory:',startPoint)
print()
print('Results:')



#search in sub directories
#print('testing recursive search function')
if searchInSubDir:
#    searchDirectory(os.getcwd(), searchString)
#    print('Starting in: ',startPoint)
    searchDirectory(startPoint, searchString)

else:
    searchCurrentDirectoryOnly(searchString)
