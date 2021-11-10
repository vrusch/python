import matplotlib.pyplot as plt
import numpy as np
import mysql.connector
import pandas as pd

#DB connect
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="atlantel",
  database="mydatabase"
)

channel_name = 'RTS1HD'
codec = 'HLS'
stage = 'BRPK'

mycursor = mydb.cursor()
sql = "SELECT date, codec, stage, Relapsed FROM channel_test WHERE channel_name = 'RTS1HD'"
mycursor.execute(sql)
myresult = mycursor.fetchall()
print(len(myresult))

DASHKALT = []
DASHBRPK = []
HLSKALT = []
HLSBRPK = []

for x in myresult:
  if 'DASH' in x and 'KALT' in x:
    #DATE.append(x[0])
    DASHKALT.append(float(x[3]))
  elif 'DASH' in x and 'BRPK' in x:
    #DATE.append(x[0])
    DASHBRPK.append(float(x[3]))
  elif 'HLS' in x and 'KALT' in x:
    #DATE.append(x[0])
    HLSKALT.append(float(x[3]))
  elif 'HLS' in x and 'BRPK' in x:
    #DATE.append(x[0])
    HLSBRPK.append(float(x[3]))
  else:
    print('trow')

print(len(DASHKALT))
print(len(DASHBRPK))
print(len(HLSKALT))
print(len(HLSBRPK))

data = {}
data['DASH KALT'] = {}
data['DASH BRPK'] = {}
data['HLS KALT'] = {}
data['HLS BRPK'] = {}

data['DASH KALT'] = DASHKALT
data['DASH BRPK'] = DASHBRPK
data['HLS KALT'] = HLSKALT
data['HLS BRPK'] = HLSBRPK

#print(data)

df = pd.DataFrame(data)
print(df)

df.plot()

plt.show()




