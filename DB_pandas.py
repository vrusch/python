import matplotlib.pyplot as plt
import mysql.connector
import pandas as pd

#DB connect
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="atlantel",
  database="mydatabase"
)
mycursor = mydb.cursor()

channel_name = 'PINKFamily'
sql = "SELECT codec, stage, Relapsed, BEelapsed, date FROM channel_test WHERE channel_name = '"+channel_name+"'"
mycursor.execute(sql)
myresult = mycursor.fetchall()
print(len(myresult))

DASHKALT = []
DASHBRPK = []
HLSKALT = []
HLSBRPK = []
DASHKALTBE = []
HLSKALTBE = []

for x in myresult:
  print(x)
  if 'DASH' in x and 'KALT' in x:
    DASHKALT.append(float(x[2]))
    DASHKALTBE.append(float(x[3]))
  elif 'DASH' in x and 'BRPK' in x:
    DASHBRPK.append(float(x[2]))
  elif 'HLS' in x and 'KALT' in x:
    HLSKALT.append(float(x[2]))
    HLSKALTBE.append(float(x[3]))
  elif 'HLS' in x and 'BRPK' in x:
    HLSBRPK.append(float(x[2]))
  else:
    print('trow')

data = {}
data['DASH KALT'] = DASHKALT
data['DASH BRPK'] = DASHBRPK
data['HLS KALT'] = HLSKALT
data['HLS BRPK'] = HLSBRPK
data['DASH KALT BE'] = DASHKALTBE
data['HLS KALT BE'] = HLSKALTBE

df = pd.DataFrame(data)
print(df.info()) 
print(df)

'''
df.plot(marker = '.')
plt.xlabel("Progress in time")
plt.ylabel("Elapsed time (ms)")
plt.title("Channel: " + channel_name)
plt.grid(linestyle = 'dashed', linewidth = 0.5)
plt.show()
'''



