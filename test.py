import mysql.connector
import datetime

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="atlantel",
  database="mydatabase"
)

mycursor = mydb.cursor()

partnerID = "3200"
channel_number = "654"
channel_name = "NationalGeographic"
date =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
stage = "KALT"
Relapsed = "0.154136"
BEelapsed = "0.1324381"
exit_msg = "OK: --KALT returned URL"
payload = "https://aw-ucdn-3201-prod.tv.cetin.cz/bpk-tv/National_Geographic_SRB_2010/output3/index.m3u8?accountId=3200&deviceType=22&subscriptionType=20967&ip=86.49.29.20&primaryToken=263b564c01090e2e_be7c155c20eb988ccad55ec7e3f427a2"


sql = "INSERT INTO channel_test (partnerID, channel_number, channel_name, date, stage, Relapsed, BEelapsed, exit_msg, payload) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
val = (partnerID, channel_number, channel_name, date, stage, Relapsed, BEelapsed, exit_msg, payload)

mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")