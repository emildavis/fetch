#!/usr/bin/python

#fetch.py
#written for python 3
#started 12/21/2017
#Author: Emil Davis
#emil.davis@roadrunner.com

##########################
#CHANGELOG
#12/21/2017 - basic functionality works. 
#12/21/2017 - add case insensitive
#01/05/2018 - add search sub-directories
#01/05/2018 - add command line argument for starting directory
#01/08/2018 - cleanup printout is bit messy
#NOT NEEDED BASH CAN DO THIS - add command line argument to open file using default application
#02/19/2018 - fixed BUG: When using the specify directory command line argument the print on screen has an extra '/' appended to the output
#02/19/2018 - display to the user what the start directory is
#06/13/2018 - print file size in human readable format rounded to two decimal places - in ISO format 1GB=1000MB
#10/22/2018 - fixed BUG: searching the root ('/') directory will result in a 'file not found' application crash
#03/22/2019 - fixed BUG: when program encounters a file it does not have read access on, program crashes
#03/22/2019 - add functionality to search within text files


#TODO add print file details size, modify date, permissions command line argument
#TODO add ability for user to choose to search within text files or not with a command line arugument
#TODO BUG: when NOT using the -s switch directories and files are not printed with the identifier
#TODO notify the user they are searching within sub directories  
#TODO add display for MS filesize in addition to the current standard filesize (1000[iso] vs 1024[Microsoft])
#TODO change how command line arguments workto make them "right"
#TODO change command line arguments to a how a 'standard' program works: fetch.py [arguments] [startDirectory] [searchTerm]. I think I can use a list to store the arguments and just parse that list. I can then make the default action with no arguments to search with the pwd for matching filenames.
#TODO print line number of a result when searching within a text file


#END OF HEADER
##########################

import os  #for file system access
import sys #for command line arguments
#text = sys.argv[1].lower()

searchInSubDir = False
startPoint = os.getcwd()


if len(sys.argv)<2:
    print('Usage: fetch.py [searchTerm] [arguments] [startDirectory]')
    print('-s or --sub to include subdirectories')
    sys.exit()

if len(sys.argv)>2:
#    startPoint=os.getcwd()
    if sys.argv[2].lower() == '-s' or sys.argv[2].lower() == '--sub':
            searchInSubDir=True
#            startPoint==os.getcwd()
if len(sys.argv)==4:
    startPoint=sys.argv[3]
    #if statement to fix bug that was changing startPoint to null if startPoint==/, changed next if to elif
    if startPoint=='/':
        True
    #strips the ending / character off the string so I can parse this string later
    elif startPoint[-1] == '/':
        startPoint=startPoint[:-1]


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
    isdir=False
#    print('Starting in: '+startPoint)
#    print('searchString is: '+searchString)
#    print('test startPoint being null:',startPoint)
    try:
        for fileName in os.listdir(startPoint):
     #       print(fileName)
    #        if os.path.isdir(fileName):
            if os.path.isdir(startPoint+'/'+fileName):
                isdir=True
                if searchString in fileName.lower():
     #               print(fileName+'     in '+startPoint)
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
    # open and search inside text files for searchString        
            #if '.txt' in fileName:
            if fileName[-4:]=='.txt' or fileName[-4:]=='.log' or fileName[-3:]=='.sh' or fileName[-5:]=='.conf':
     #           print('searched file name is: ',' ',fileName)
                if isdir==False:
                    file=open(startPoint+'/'+fileName,'r')
                    try:
                        for line in file:
                            if searchString in line:
                                size=getFileSize(os.path.join(startPoint,fileName))
                                print(size,'File: '+startPoint+'/'+fileName,' ',line)
                    except:
                        True
                        print('Exception error searching in: ',fileName,'. Continuing search')
                    file.close
    except:
        True
        print('#### Exception Error opening file: ',fileName)
                        
text = sys.argv[1].lower()

#clear screen first using ANSI VT100 clear screen code
#Note: This will only work in a Linux/Unix terminal or emulator
print("\033[H\033[J")

#print('############# THIS IS THE TEST VERSION ##################')

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
