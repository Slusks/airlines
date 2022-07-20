import csv
import pandas as pd
import os
from pathlib import Path
from timeit import default_timer as timer

# target = r"C:\airlineData\986642879_T_ONTIME_REPORTING.csv"
# file = "986629864_T_ONTIME_REPORTING.csv"
# month_list = ["Samtember", "January","February","March","April","May","June","July","August","September","October","November","December"]

# df = pd.read_csv(target, delimiter=',', encoding="utf-8-sig")
# year = str(df['YEAR'][3])
# month =  df['MONTH'][3]
# pyMonth = month.item()
# print(type(pyMonth))
mainDirectory = Path(r"C:/airlineData/")
masterFile = Path(mainDirectory/"combined/airlineDB.csv")


def combineCSV(passedDirectory, masterFile):
    combineList = []
    for file in os.listdir(passedDirectory):
        nf = pd.read_csv(passedDirectory/file, delimiter=',',encoding="utf-8-sig")
        combineList.append(nf)
    newFile = pd.concat(combineList)
    print(newFile)

def combineCSVChunks(passedDirectory, outputFile):
    CHUNK_SIZE = 50000
    first_one = True
    for file in os.listdir(passedDirectory):
        if not first_one:
            skip_row=[0]
        else:
            skip_row=[]
        chunk_container = pd.read_csv(passedDirectory/file, chunksize=CHUNK_SIZE, header=0, skiprows=skip_row)
        for chunk in chunk_container:
            chunk.to_csv(outputFile, mode="a", index=False)
        first_one=False



## Columns that are not strings:
#10-13
#17
#19-22
#26
#28-34
#36-45
#47
#49-60


    
    
print("start")
start = timer()
combineCSVChunks(mainDirectory/"dated", mainDirectory/"combined/totalAirlineData.csv")
elapsed_time = timer() - start
print("time:",elapsed_time)



