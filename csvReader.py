import csv
import pandas as pd

target = r"C:\airlineData\986642879_T_ONTIME_REPORTING.csv"
file = "986629864_T_ONTIME_REPORTING.csv"
month_list = ["Samtember", "January","February","March","April","May","June","July","August","September","October","November","December"]

df = pd.read_csv(target, delimiter=',', encoding="utf-8-sig")
year = str(df['YEAR'][3])
month =  df['MONTH'][3]
pyMonth = month.item()
print(type(pyMonth))

