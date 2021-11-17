
import mysql.connector
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

#sql = "SELECT date, channel_name, codec, stage, Relapsed, BEelapsed, exit_msg FROM channel_test"
sql = "SELECT date, channel_name, DASH_KALT, DASH_KALT_BE, DASH_BRPK, HLS_KALT, HLS_KALT_BE, HLS_BRPK FROM mydatabase.channel_test_upr"
mycursor.execute(sql)
myresult = mycursor.fetchall()
print(len(myresult))
''''''
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
  dash_brpk.append(float(x[4]))
  hls_kalt.append(float(x[5]))
  hls_kalt_be.append(float(x[6]))
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
dx = dx[(dx.channels == 'RTS1HD')]
print(dx)
mask = dx.channels.isin(dx.channels.unique())
print(mask)
dd = (dx[mask])
print(dd)
fig = px.line(dx[mask], x="dates", y=["dash_kalt", "dash_kalt_be", "dash_brpk", "hls_kalt", "hls_kalt_be", "hls_brpk"], markers=True)
fig.show()

'''
date = []
channel_name = []
codec = []
stage = []
Relapsed = []
BEelapsed = []
exit_msg = []

for x in myresult:
  date.append(x[0])
  channel_name.append(x[1])
  codec.append(x[2])
  stage.append(x[3])
  if x[4] == '':
    Relapsed.append(x[4])
  else:
    Relapsed.append(float(x[4]))
  if x[5] == '':
    BEelapsed.append(x[5])
  else:
    BEelapsed.append(float(x[5]))
  exit_msg.append(x[6])
  
  data = {}
  data['channel'] = channel_name
  data['date'] = date
  data['codec'] = codec
  data['stage'] = stage
  data['Relapsed'] = Relapsed
  data['BEelapsed'] = BEelapsed
  data['exit_msg'] = exit_msg

dx = pd.DataFrame(data)
#print(dx)
#dff = dx[(dx.channel == 'RTS1HD') & (dx.codec == 'DASH') & (dx.stage == 'KALT')]

dash_kalt = dx.query("codec in ['DASH'] and stage in ['KALT']")
print(dash_kalt)
mask = dx.channel.isin(dx.channel.unique())
fig = px.line(dx[mask], x="date", y=["Relapsed"], color='channel', markers=True)
#fig.show()
'''