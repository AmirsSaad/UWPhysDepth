import shutil
import os

def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles

source = "/Users/oferhazut/Downloads/backup/Media/"
dirs_list = os.listdir(source)

for dirs in dirs_list:
# Get the list of all files in directory tree at given path
    dirfullPath = os.path.join(source, dirs)
    listOfFiles = getListOfFiles(dirfullPath)
#destination = "/Users/oferhazut/Downloads/backup/Media 2/"
    for files in listOfFiles:
        if '.DS_Store' not in files:
            shutil.move(files, dirfullPath)
    