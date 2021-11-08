
import csv


rows = []
inputfile = "output.csv"
outputfile = ""

channel_name = "AMCBalkan"
codec = "DASH"



# reading csv file
with open(inputfile, 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter = ',')
    # extracting each data row one by one
    for row in csvreader:
        if channel_name in row and codec in row:
            print(row) 
        
        





""""
sentense = ""
f = open(outputfile, "a")
f.write(sentense)
f.close()
"""