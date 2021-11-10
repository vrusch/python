import matplotlib.pyplot as plt
import numpy as np
import mysql.connector

#DB connect
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="atlantel",
  database="mydatabase"
)

channel_name = 'RTS1HD'
codec = 'HLS'
stage = 'BRPK'

mycursor = mydb.cursor()
#sql = "SELECT date, channel_name, stage, exit_msg, Relapsed FROM channel_test WHERE Relapsed > '0.6'"
sql = "SELECT Relapsed FROM channel_test WHERE channel_name = 'RTS1HD' and codec = 'HLS' and stage = 'BRPK'"
mycursor.execute(sql)
myresult = mycursor.fetchall()
print(len(myresult))

#for x in myresult:
    #print(x)


yp = []

for x in myresult:
    yp.append(float(x[0]))

ypoints = np.array(yp)

plt.plot(ypoints, '.-b')
plt.grid(color = 'green', linestyle = '--', linewidth = 0.5)
plt.title("Channel: " + channel_name + " Streamer: " + codec + " Stage: " + stage)
plt.xlabel("Progress in time")
plt.ylabel("Elapsed time (ms)")
plt.show()

