import os
import time
import glob


directory = r"C:\airlineData"



def checkFileDownloaded(passedDirectory):
    print("checking downloads")
    directory = passedDirectory
while len(glob.glob('*.crdownload')) > 0:
    print ("download in progress")
    time.sleep(5)
    pass
else:
    break



checkFileDownloaded(directory)