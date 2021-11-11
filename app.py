
import mysql.connector


#DB connect
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="atlantel",
  database="mydatabase"
)
date = "2021-10-11 11:55:35"
partnerID = '3200'
channelNumber = '001'
channelName = 'blablabla vk'
RelapsedHLS = '0.56897'
KALT_executionTime = 'NONE'
exit_msg = 'fghfghfgh'
payload = 'chdghdhgdhdgh'


mycursor = mydb.cursor()

sql = "INSERT INTO channel_test (date, partnerID, channel_number, channel_name, codec, stage, Relapsed, BEelapsed, exit_msg, payload) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
val = (date, partnerID, channelNumber, channelName, 'HLS', 'KALT', RelapsedHLS, KALT_executionTime, exit_msg, payload)
mycursor.execute(sql, val)
mydb.commit()
lastID = mycursor.lastrowid
print("1 record inserted, ID:" + str(lastID))