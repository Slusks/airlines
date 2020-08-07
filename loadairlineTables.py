from pathlib import Path
import os

mainDirectory = Path(r"C:/airlineData/")


def writeSQL(passedDirectory):
    for file in os.listdir(passedDirectory):
        print("LOAD DATA LOCAL INFILE 'C:/airlineData/dated/" + str(file) +"' into table airlinedata")
        print("FIELDS TERMINATED BY ','")
        print("LINES TERMINATED BY '\\n'")
        print("IGNORE 1 LINES;")

writeSQL(mainDirectory/"dated")