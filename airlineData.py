from pathlib import Path #https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f
import pathlib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import zipfile
import os
import time
import glob
import pandas as pd
import shutil
import csv




# Start Parameters
years = [2016, 2017, 2018, 2019, 2020]
month_names = ["January","February","March","April","May","June","July","August","September","October","November","December"]
destinationFolder = Path(r"C:/Users/sam/Documents/My Tableau Repository/Datasources/Airlines/carrierReporting") #this will be used in later production



#prelaunch chrome IAW prior to running this program: https://cosmocode.io/how-to-connect-selenium-to-an-existing-browser-that-was-opened-manually/
# first use this to launch browser with debugging flags: chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenum\ChromeProfile"
# On work computer and/or if having issues adding chrome.exe to path, can also use 'start chrome' and then the above tags
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
#change chrome driver path
chrome_driver = "C:/Python37/chromedriver.exe" #this has to be accomplished on whatever computer this is run on or the path has to change
driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)


###
mainDirectory = Path(r"C:/airlineData/")
###


#checking all the checkboxes for the data we want to download
def checkboxes():
    print("checkboxes")
    checkboxes = driver.find_elements_by_xpath("//input[@name='VarName']")
    count = 0
    print("checkboxes", checkboxes)
    for checkbox in checkboxes:
        if count == 61:
            print ("all set with checkboxes")
            break
        else:
            print("checkbox:", checkbox)
            count +=1
            print(count)
            if not checkbox.is_selected():
                checkbox.send_keys(" ")
                print ('click')
            else:
                print("already selected")
                continue

#Selecting the time period from the dropdown
def select_time(year, month):
    #select the year, iterate over years
    year_selector = driver.find_element_by_id('XYEAR')
    #print("year_selector", year_selector)
    for option in year_selector.find_elements_by_tag_name('option'):
        #print("option:", option)
        if option.text == str(year):
            option.click()
            print("Year:", year)
    # select the month, iterate over month_names for now. Should be noted each month corresponds to a numeric value
    month_selector = driver.find_element_by_name('FREQUENCY')
    for option in month_selector.find_elements_by_tag_name('option'):
        if option.text == month:
            option.click()# this is going to have to be sent an element of an iterable and also I hope click works here
            print("Month:", month)

#Trigger the download after month/year selected
def downloadDatabase():
        #Download selection
        print ("Downloading")
        submit_button = driver.find_element_by_xpath("//*[@id='content']/table[1]/tbody/tr/td[2]/table[3]/tbody/tr/td[2]/button[1]")
        submit_button.click()

#Pause the download while a file is downloading
def checkFileDownloaded(passedDirectory):
    print("checking downloads")
    time.sleep(10)
    while len(list(passedDirectory.glob('*.crdownload'))) > 0:
        print ("download in progress")
        time.sleep(5)
    if len(list(passedDirectory.glob('*.crdownload'))) == 0 and len(list(passedDirectory.glob('*.zip'))) >= 0:
        return True

#unzips the files and places them in the unzipped directory
def unzipFiles(passedDirectory, file):
    print("unzipping files")
    with zipfile.ZipFile(passedDirectory/file, "r") as zip_ref:
        zip_ref.extractall(passedDirectory/'unzipped')

#moves and renames the unzipped file. This is necessary because all of the files unzip with the same name
def changeFile(passedDirectory, filename, count):
    print("count:", count)
    print("changing file")
    unzippedDirectory = passedDirectory/'unzipped'
    finalDirectory = passedDirectory/'renamed'
    if len(filename) == 32:
        base_filename = filename[:-4]+'.csv'
    elif len(filename)==36:
        base_filename = filename[:-8]+'.csv'
    elif len(filename)== 37:
        base_filename = filename[:-9]+'.csv'
    else:
        print("weird file name length:", len(filename))
    new_filename = "database_"+str(count)+'.csv'
    print("new File name:", new_filename)
    print("unzippedDirectory:", unzippedDirectory)
    print("finalDirectory:", finalDirectory)

    shutil.move(unzippedDirectory / base_filename, finalDirectory / new_filename)

#moves and renames the files one more time, but by date
def dateFile(passedDirectory):
    for file in enumerate(os.listdir(passedDirectory)):
        print("file:", file)
        month_list = ["Samtember", "January","February","March","April","May","June","July","August","September","October","November","December"]
        df = pd.read_csv(passedDirectory/file[1], delimiter=',', encoding="utf-8-sig")
        year = str(df['YEAR'][3])
        numpymonth =  df['MONTH'][3]
        pyMonth = numpymonth.item()
        month = month_list[pyMonth]

        newFilename = month + "_" + year + ".csv"
        newDirectory = Path(r"C:/airlineData/dated")
        print("passed Directory:", passedDirectory)
        print("original Filename:", file[1])
        print("newFilename:", newFilename)

        shutil.move(passedDirectory / file[1], newDirectory / newFilename )
        print("file moved")

#combine all of the csv files
def combineCSV(passedDirectory, masterFile):
    dfList = [pd.read_csv(file, delimiter=',', encoding=encoding="utf-8-sig") for file in os.list(passedDirectory) if file.endswith('csv')]
    finaldf = pd.concat(dfList, axis=1, join="inner")
    


combineCSV(mainDirectory/"renamed")


#Running the Scripts:
print("starting")
# Completed checkboxes() 
# completed = (len(years)*len(month_names))
# completed print(completed)
# for year in years:
#     for month in month_names:
#         if month == "June" and year == 2020:
#             print ("downloaded all available databases")
#             break
#         else:
#             select_time(year, month)
#             downloadDatabase()
#             while True:
#                 if checkFileDownloaded(mainDirectory) == True:
#                     break
#                 else:
#                     continue


# for count, file in enumerate(os.listdir(mainDirectory)):
#     if file.endswith(".zip"):
#         print("mainDirectory:", mainDirectory)
#         print("file:", file)
#         unzipFiles(mainDirectory, file)
#         changeFile(mainDirectory, file, count)
#     else:
#         continue

#moving the files again so they have better names
rename_to_dated = Path(r"C:/airlineData/renamed")
dateFile(rename_to_dated)







#References
'''
https://www.transtats.bts.gov/tables.asp?Table_ID=236&SYS_Table_Name=T_ONTIME_REPORTING
https://www.transtats.bts.gov/DL_SelectFields.asp
https://cosmocode.io/how-to-connect-selenium-to-an-existing-browser-that-was-opened-manually/
https://sqa.stackexchange.com/questions/1355/what-is-the-correct-way-to-select-an-option-using-seleniums-python-webdriver
#checking all the checkboxes https://sqa.stackexchange.com/questions/3292/how-to-select-or-check-multiple-checkboxes-in-selenium
https://stackoverflow.com/questions/34338897/python-selenium-find-out-when-a-download-has-completed
https://stackoverflow.com/questions/48263317/selenium-python-waiting-for-a-download-process-to-complete-using-chrome-web
'''
