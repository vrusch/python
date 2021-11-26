import mysql.connector
from numpy import NaN
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

#DB connect
mydb = mysql.connector.connect(
  host="10.0.0.6",
  user="root",
  password="atlantel",
  database="mydatabase"
)
mycursor = mydb.cursor()

sql = "SELECT date, channel_name, DASH_KALT, DASH_KALT_BE, DASH_BRPK, HLS_KALT, HLS_KALT_BE, HLS_BRPK FROM mydatabase.channel_test_upr"
mycursor.execute(sql)
myresult = mycursor.fetchall()
print("Zaznamu nacteno z DB: "+str(len(myresult)))