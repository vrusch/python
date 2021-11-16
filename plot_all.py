
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
  Relapsed.append(x[4])
  BEelapsed.append(x[5])
  exit_msg.append(x[6])
  
  data = {}
  data['date'] = date
  data['channel'] = channel_name
  data['codec'] = codec
  data['stage'] = stage
  data['Relapsed'] = Relapsed
  data['BEelapsed'] = BEelapsed
  data['exit_msg'] = exit_msg

#print(data)
dx = pd.DataFrame(data)
#print(dx.info()) 
print(dx)

fig = px.line(dx, x='date', y='Relapsed')
fig.show()