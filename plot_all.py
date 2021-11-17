
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

sql = "SELECT date, channel_name, codec, stage, Relapsed, BEelapsed, exit_msg FROM channel_test"
mycursor.execute(sql)
myresult = mycursor.fetchall()
print(len(myresult))

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
print(dx)
#dff = dx[(dx.channel == 'RTS1HD') & (dx.codec == 'DASH') & (dx.stage == 'KALT')]
#dxa = dx.query("channel in ['RTS1HD'] and codec in ['DASH'] and stage in ['KALT']")
channels = dx.channel.unique()
mask = dx.channel.isin(channels)
fig = px.line(dx[mask], x="date", y="Relapsed", color='channel', markers=True)

#fig = px.line(dxa, x='date', y='Relapsed', markers=True, symbol="stage"
fig.show()