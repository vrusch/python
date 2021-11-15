
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

#data = []
dt = {}

for x in myresult:
    #data.append(dict(channel = str([x[1]]), date = x[0], codec =[x[2]], stage = [x[3]], Relapsed =[x[4]], exit_msg =[x[5]]))
    dt[str(x[1])] = {}
    dt[str(x[1])][x[0]] = {}



#dx = pd.DataFrame(data)
print(dt)

#dictionary = {}
#dictionary["channel"] = {}
#dictionary["channel"]["DASH"] = [{"KALT" : 'true'}]
#dictionary["channel"]["DASH"] = [{"BRPK" : 'true'}]
#dictionary["channel"]["HLS"] = [{"KALT": 'true'}]
#dictionary["channel"]["HLS"] = [{"BRPK": 'true'}]

#fig = px.line(dx, x="date", y='Relapsed')
#fig.show()