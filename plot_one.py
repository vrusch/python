import matplotlib.pyplot as plt
import mysql.connector
import pandas as pd
import plotly.express as px

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

dash_kalt = []
dash_brpk = []
hls_kalt = []
hls_brpk = []
dash_kalt_be = []
hls_kalt_be = []
dates = []

for x in myresult:
  #print(x)
  if 'DASH' in x and 'KALT' in x:
    dates.append(x[4])
    dash_kalt.append(float(x[2]))
    dash_kalt_be.append(float(x[3]))
  elif 'DASH' in x and 'BRPK' in x:
    dash_brpk.append(float(x[2]))
  elif 'HLS' in x and 'KALT' in x:
    hls_kalt.append(float(x[2]))
    hls_kalt_be.append(float(x[3]))
  elif 'HLS' in x and 'BRPK' in x:
    hls_brpk.append(float(x[2]))
  else:
    print('trow')

data = {}
data['DATE'] = dates
data['DASH KALT'] = dash_kalt
data['DASH BRPK'] = dash_brpk
data['HLS KALT'] = hls_kalt
data['HLS BRPK'] = hls_brpk
data['DASH KALT BE'] = dash_kalt_be
data['HLS KALT BE'] = hls_kalt_be

dx = pd.DataFrame(data)
#print(dx.info()) 
print(dx)

'''
dx.plot(x= "DATE",marker = '.')
#plt.plot(x = 'DASH KALT', y = 'DATE')
plt.xlabel("Progress in time")
plt.ylabel("Elapsed time (ms)")
plt.title("Channel: " + channel_name)
plt.grid(linestyle = 'dashed', linewidth = 0.5)
plt.show()
'''
interpolation = 'hvh' # linear, spline, vhv, hvh, vh, hv

fig = px.area(dx, x="DATE", y=["DASH KALT", "DASH BRPK", "HLS KALT", "HLS BRPK"], markers=True, line_shape=interpolation)
fig.show()





