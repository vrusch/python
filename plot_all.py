
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

dt = {}
poc = 0

for x in myresult:
    poc = poc + 1
    #print(x)
    dt[poc] = {'channel' : x[1], 'date' : x[0], 'codec' : x[2], 'stage' : x[3], 'Relapsed' : x[4], 'BEelapsed' : x[5]} 


dx = pd.DataFrame(dt)
print(dx)

#fig = px.line(dx, x='date')
#fig.show()