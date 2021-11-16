
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

dt = {}
poc = 0

for x in myresult:
    poc = poc + 1
    #print(x)
    dt[poc] = {'channel' : x[1], 'date' : x[0], 'codec' : x[2], 'stage' : x[3], 'Relapsed' : x[4], 'BEelapsed' : x[5]}
    #data.append(dict(channel = str([x[1]]), date = x[0], codec =[x[2]], stage = [x[3]], Relapsed =[x[4]], exit_msg =[x[5]]))
  
  


dx = pd.DataFrame(dt)
print(dx)

#dictionary = {}
#dictionary["channel"] = {}
#dictionary["channel"]["DASH"] = [{"KALT" : 'true'}]
#dictionary["channel"]["DASH"] = [{"BRPK" : 'true'}]
#dictionary["channel"]["HLS"] = [{"KALT": 'true'}]
#dictionary["channel"]["HLS"] = [{"BRPK": 'true'}]

#fig = px.line(dx, x=0, y=4)
#fig.show()