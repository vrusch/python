
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

sql = "SELECT date, channel_name, codec, stage, Relapsed, BEelapsed, exit_msg FROM channel_test"
mycursor.execute(sql)
myresult = mycursor.fetchall()

data = []


for x in myresult:
    data.append(dict(date = x[0], channel = [x[1]] , codec =[x[2]], stage = [x[3]], Relapsed =[x[4]], exit_msg =[x[5]]))

dx = pd.DataFrame(data)
print(dx)