from pathlib import Path #https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import downloadhandle









# Start Parameters
years = [2016, 2017, 2018, 2019, 2020]
month_names = ["January","February","March","April","May","June","July","August","September","October","November","December"]
month_values = [1,2,3,4,5,6,7,8,9,10,11,12]
destinationFolder = Path(r"C:/Users/sam/Documents/My Tableau Repository/Datasources/Airlines/carrierReporting")
#URL = "https://www.transtats.bts.gov/tables.asp?Table_ID=236&SYS_Table_Name=T_ONTIME_REPORTING" 
#URL="https://www.transtats.bts.gov/DL_SelectFields.asp"


#prelaunch chrome IAW prior to running this program: https://cosmocode.io/how-to-connect-selenium-to-an-existing-browser-that-was-opened-manually/
# first use this to launch browser with debugging flags: chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenum\ChromeProfile"
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
#change chrome driver path
chrome_driver = "C:/Python37/chromedriver.exe"
driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)
print (driver.title)


#checking all the checkboxes
def checkboxes():
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
    year_selector = driver.find_element_by_name('XYEAR')
    for option in year_selector.find_elements_by_link_text(str(year)):
        if option.text == str(year):
            option.click()
            print("Year:", year)
            break
    # select the month, iterate over month_names for now. Should be noted each month corresponds to a numeric value
    month_selector = driver.find_element_by_name('FREQUENCY')
    for option in month_selector.find_elements_by_link_text(month):
        if option.text == month:
            option.click()# this is going to have to be sent an element of an iterable and also I hope click works here
            print("Month:", month)
            break

def downloadDatabase():
        #Download selection
        print ("Downloading")
        submit_button = driver.find_element_by_xpath("//*[@id='content']/table[1]/tbody/tr/td[2]/table[3]/tbody/tr/td[2]/button[1]")
        submit_button.click()

downloadhandle
checkboxes()
for year in years:
    for month in month_names:
        if month == "April" and year == 2020:
            print ("downloaded all available databases")
            break
        else:
            print (month,' ',year)
            select_time(year, month)
            #downloadDatabase()

#References
'''
 https://cosmocode.io/how-to-connect-selenium-to-an-existing-browser-that-was-opened-manually/
 https://sqa.stackexchange.com/questions/1355/what-is-the-correct-way-to-select-an-option-using-seleniums-python-webdriver
#checking all the checkboxes https://sqa.stackexchange.com/questions/3292/how-to-select-or-check-multiple-checkboxes-in-selenium
'''
