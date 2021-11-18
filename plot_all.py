
import mysql.connector
from numpy import NaN
import pandas as pd
from pandas.core import indexing
import plotly.express as px

#DB connect
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="atlantel",
  database="mydatabase"
)
mycursor = mydb.cursor()

sql = "SELECT date, channel_name, DASH_KALT, DASH_KALT_BE, DASH_BRPK, HLS_KALT, HLS_KALT_BE, HLS_BRPK FROM mydatabase.channel_test_upr"
mycursor.execute(sql)
myresult = mycursor.fetchall()
print("Zaznamu nacteno z DB: "+str(len(myresult)))

dates = []
channels = []
dash_kalt = []
dash_kalt_be = []
dash_brpk = []
hls_kalt = []
hls_kalt_be = []
hls_brpk = []

for x in myresult:
  dates.append(x[0])
  channels.append(x[1])
  dash_kalt.append(float(x[2]))
  dash_kalt_be.append(float(x[3]))
  if x[4] == '':
    dash_brpk.append(NaN)
  else:
    dash_brpk.append(float(x[4]))
  hls_kalt.append(float(x[5]))
  hls_kalt_be.append(float(x[6]))
  if x[7] == '':
    hls_brpk.append(NaN)
  else:
    hls_brpk.append(float(x[7]))

  data = {}
  data['dates'] = dates
  data['channels'] = channels
  data['dash_kalt'] = dash_kalt
  data['dash_kalt_be'] = dash_kalt_be
  data['dash_brpk'] = dash_brpk
  data['hls_kalt'] = hls_kalt
  data['hls_kalt_be'] = hls_kalt_be
  data['hls_brpk'] = hls_brpk

dx = pd.DataFrame(data)
all_channels = dx.channels.unique()
dx = dx[(dx.channels == 'RTS1HD') | (dx.channels == 'RTS2HD')]
sel_channels = dx.channels.unique()
mask = dx.channels.isin(dx.channels.unique())

fig = px.line(dx[mask], x="dates", y=["dash_kalt", "dash_kalt_be", "dash_brpk", "hls_kalt", "hls_kalt_be", "hls_brpk"], color='channels', markers=True)
#fig.show()