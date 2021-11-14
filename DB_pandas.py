
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

sql = "SELECT channel_name, stage, codec, Relapsed, BEelapsed, date FROM channel_test"
mycursor.execute(sql)
myresult = mycursor.fetchall()

data = {}


for x in myresult:
  if x[0] in data:
    if 'DASH' in x:
      data[str(x[0])]['DASH'] = x[3]
    if 'HLS' in x:
      data[str(x[0])]['HLS'] = x[3]
  else:
    data[str(x[0])] = []
    data[str(x[0])]['DASH'] = {}
    data[str(x[0])]['HLS'] = {}
    if 'DASH' in x:
      data[str(x[0])]['DASH'] = x[3]
    if 'HLS' in x:
      data[str(x[0])]['HLS'] = x[3]
    

print(data)




