import datetime
import mysql.connector
import schedule
import time
from KALT_config import *
import logging
import logging.handlers as handlers
import csv


#specificke promenne pro test
partnerID = '3200'
inputfile = "opc_tlrs.csv"

#DB connect
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="atlantel",
  database="mydatabase"
)

#logovani a rotovani logu
logger = logging.getLogger('my_app')
logger.setLevel(logging.INFO)
logHandler = handlers.RotatingFileHandler('./log/channel_availability_test.log', maxBytes=5242880, backupCount=5)
logHandler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)-0s %(levelname)-0s %(message)s")
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

#ziskani credentials a API hlavicek, phoenixURL
credentials = user_login(partnerID, 4)
head = headers(partnerID)
headerPOST = head[0]
headerGET = head[1]
phoenixURL = head[2]

#ziskani user ks
ks = KALT_ks(apiVersion, partnerID, credentials[0], credentials[1], credentials[2], phoenixURL, headerPOST)
if ks == 'ERROR':
    logger.info("No login ks returned")
else:
    the_datetime = datetime. datetime. fromtimestamp(ks[3]) 
    logger.info("[LOGIN]KS EXPIRATION: ", the_datetime )
    logger.info("[LOGIN]BE execution Time: "+str(ks[2]))
    logger.info("[LOGIN]Elapsed Time: "+str(ks[1]))
    logger.info("[LOGIN]User KS: " + ks[0])

def func():
    date =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info("=============================================================================================")
    logger.info("======= NEXT ROUND START: " + date + " ===============================================")
    logger.info("=============================================================================================")
    print("ROUND START: " + date)
    #otevrit csv a vrati stream
    with open(inputfile, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter = ';')
        for row in csvreader:
            channelNumber = row[2]
            channelName = row[0]
            assetId = row[1]
            logger.info("=============================================================================================")
            logger.info("[TEST]Start test for channel name: " + channelName + " #" + channelNumber + " with ID: " + assetId)
            r = get_context(assetId, ks[0], headerPOST, phoenixURL)
            responseDASH = r[0].json()
            responseHLS = r[1].json()


    #(assetId, codec, response , headerGET)
    #analyzeDASH -KALT
            logger.info("--> Start analyze DASH")
            KALT_Relapsed = r[2]
            KALT_executionTime = responseDASH['executionTime']
            try:
                urlDASH = responseDASH['result']['sources'][0]['url']
                exit_msg = "OK"
                payload = urlDASH
                logger.info("[RESULT][KALT][DASH]["+channelName+"]["+channelNumber+"]REASON: OK --KALT returned URL")
                DASH_kalt_reason = True
            except:
                Etype = responseDASH['result']['actions'][0]['type']
                Emsg = responseDASH['result']['messages'][0]['message']

                #send_alarm("[" + channelName+ "][" + channelNumber + "]ERROR: type: " + Etype + ", " + channelName+"][" + channelNumber + "]ERROR: message: " + Emsg)

                exit_msg = "ERROR"
                payload = "ERROR type: " + Etype + "; Error reason: " + Emsg
                logger.error("[ERROR][KALT][DASH]["+channelName+"]["+channelNumber+"]ERROR: --KALT not returned any URL")
                logger.error("[ERROR][KALT][DASH]["+channelName+"]["+channelNumber+"]ERROR: type: " + Etype)
                logger.error("[ERROR][KALT][DASH]["+channelName+"]["+channelNumber+"]ERROR: message: " + Emsg)
                DASH_kalt_reason = False
            finally:
                #date, partnerID, channel#, name, codec, stage ,Relapsed, BEelapsed, exit_msg, payload
                date =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                mycursor = mydb.cursor()
                sql = "INSERT INTO channel_test (date, partnerID, channel_number, channel_name, codec, stage, Relapsed, BEelapsed, exit_msg, payload) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (date, partnerID, channelNumber, channelName, 'DASH', 'KALT', KALT_Relapsed, KALT_executionTime, exit_msg, payload)
                #print(val)
                mycursor.execute(sql, val)
                mydb.commit()
                lastID = mycursor.lastrowid
                logger.info("1 record inserted, ID:" + str(lastID))

            #analyzeDASH -BRPK
            if DASH_kalt_reason:
                logger.info("--> CONTINUE TEST FOR DASH -- STAGE BRPR")
                GETresponse = requests.get(urlDASH, headers=headerGET)
                get_responsecode = GETresponse.status_code
                if get_responsecode == 200:
                    Gelapsed = GETresponse.elapsed.microseconds/1000000
                    logger.info("[RESULT][BRPK][DASH]["+channelName+"]["+channelNumber+"]Response reason: "+str(GETresponse.reason))

                    exit_msg = "OK" 
                    payload = "Reason: "+str(GETresponse.reason)+" Status code: "+str(get_responsecode) 
                else:
                    Gelapsed = GETresponse.elapsed.microseconds/1000000
                    logger.error("[ERROR][BRPK][DASH]["+channelName+"]["+channelNumber+"]Response reason: "+str(GETresponse.reason))
                    logger.error("[ERROR][BRPK][DASH]["+channelName+"]["+channelNumber+"]Response status code: "+str(get_responsecode))
                    logger.error("[ERROR][BRPK][DASH]["+channelName+"]["+channelNumber+"]Elapsed time: "+str(Gelapsed)) 

                    #send_alarm("[ERROR][BRPK][DASH]["+channelName+"]["+channelNumber+"]BRPK not get Manifest. (wrong URL?); Response status code: "+str(get_responsecode))
                    
                    exit_msg = "ERROR: --BRPK not get Manifest. (wrong URL?)"
                    payload = "--BRPK not get Manifest. (wrong URL?) Reason: "+str(GETresponse.reason)+" Status code: "+str(get_responsecode)         

            else:
                logger.warning("[RESULT][BRPK][DASH]["+channelName+"]["+channelNumber+"]ERROR: --KALT not returned any URL")

                #send_alarm("[RESULT][BRPK][DASH]["+channelName+"]["+channelNumber+"]ERROR: --KALT not returned any URL")

                exit_msg = "ERROR"
                payload = "--KALT not returned any URL"
                Gelapsed = ""

            #date, partnerID, channel#, name, codec, stage ,Relapsed, BEelapsed, exit_msg, payload
            date =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            mycursor = mydb.cursor()
            sql = "INSERT INTO channel_test (date, partnerID, channel_number, channel_name, codec, stage, Relapsed, BEelapsed, exit_msg, payload) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (date, partnerID, channelNumber, channelName, 'DASH', 'BRPK', Gelapsed, '', exit_msg, payload)
            #print(val)
            mycursor.execute(sql, val)
            mydb.commit()
            lastID = mycursor.lastrowid
            logger.info("1 record inserted, ID:" + str(lastID))



    #(assetId, codec, response , headerGET)
    #analyzeHLS: -KALT
            logger.info("--> Start analyze HLS")
            KALT_Relapsed = r[2]
            KALT_executionTime = responseHLS['executionTime']
            try:
                urlHLS = responseHLS['result']['sources'][0]['url']
                exit_msg = "OK"
                payload = urlHLS
                logger.info("[RESULT][KALT][HLS]["+channelName+"]["+channelNumber+"]REASON: OK --KALT returned URL")
                HLS_kalt_reason = True
            except:
                Etype = responseHLS['result']['actions'][0]['type']
                Emsg = responseHLS['result']['messages'][0]['message']

                #send_alarm("[" + channelName+ "][" + channelNumber + "]ERROR: type: " + Etype + ", " + channelName+"][" + channelNumber + "]ERROR: message: " + Emsg)

                exit_msg = "ERROR"
                payload = "ERROR type: " + Etype + "; Error reason: " + Emsg
                logger.error("[ERROR][KALT][HLS]["+channelName+"]["+channelNumber+"]ERROR: --KALT not returned any URL")
                logger.error("[ERROR][KALT][HLS]["+channelName+"]["+channelNumber+"]ERROR: type: " + Etype)
                logger.error("[ERROR][KALT][HLS]["+channelName+"]["+channelNumber+"]ERROR: message: " + Emsg)
                HLS_kalt_reason = False
            finally:
                #date, partnerID, channel#, name, codec, stage ,Relapsed, BEelapsed, exit_msg, payload
                date =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                mycursor = mydb.cursor()
                sql = "INSERT INTO channel_test (date, partnerID, channel_number, channel_name, codec, stage, Relapsed, BEelapsed, exit_msg, payload) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (date, partnerID, channelNumber, channelName, 'HLS', 'KALT', KALT_Relapsed, KALT_executionTime, exit_msg, payload)
                #print(val)
                mycursor.execute(sql, val)
                mydb.commit()
                lastID = mycursor.lastrowid
                logger.info("1 record inserted, ID:" + str(lastID))

            #analyzeHLS -BRPK
            if HLS_kalt_reason:
                logger.info("--> CONTINUE TEST FOR HLS -- STAGE BRPR")
                GETresponse = requests.get(urlHLS, headers=headerGET)
                get_responsecode = GETresponse.status_code
                if get_responsecode == 200:
                    Gelapsed = GETresponse.elapsed.microseconds/1000000
                    logger.info("[RESULT][BRPK][HLS]["+channelName+"]["+channelNumber+"]Response reason: "+str(GETresponse.reason))

                    exit_msg = "OK" 
                    payload = "Reason: "+str(GETresponse.reason)+" Status code: "+str(get_responsecode) 
                else:
                    Gelapsed = GETresponse.elapsed.microseconds/1000000
                    logger.error("[ERROR][BRPK][HLS]["+channelName+"]["+channelNumber+"]Response reason: "+str(GETresponse.reason))
                    logger.error("[ERROR][BRPK][HLS]["+channelName+"]["+channelNumber+"]Response status code: "+str(get_responsecode))
                    logger.error("[ERROR][BRPK][HLS]["+channelName+"]["+channelNumber+"]Elapsed time: "+str(Gelapsed)) 

                    #send_alarm("[ERROR][BRPK][DASH]["+channelName+"]["+channelNumber+"]BRPK not get Manifest. (wrong URL?); Response status code: "+str(get_responsecode))
                    
                    exit_msg = "ERROR"
                    payload = "--BRPK not get Manifest. (wrong URL?) Reason: "+str(GETresponse.reason)+" Status code: "+str(get_responsecode)         

            else:
                logger.warning("[RESULT][BRPK][HLS]["+channelName+"]["+channelNumber+"]ERROR: --KALT not returned any URL")

                #send_alarm("[RESULT][BRPK][HLS]["+channelName+"]["+channelNumber+"]ERROR: --KALT not returned any URL")

                exit_msg = "ERROR"
                payload = "--KALT not returned any URL"
                Gelapsed = ""

            #date, partnerID, channel#, name, codec, stage ,Relapsed, BEelapsed, exit_msg, payload
            date =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            mycursor = mydb.cursor()
            sql = "INSERT INTO channel_test (date, partnerID, channel_number, channel_name, codec, stage, Relapsed, BEelapsed, exit_msg, payload) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (date, partnerID, channelNumber, channelName, 'HLS', 'BRPK', Gelapsed, '', exit_msg, payload)
            mycursor.execute(sql, val)
            mydb.commit()
            lastID = mycursor.lastrowid
            logger.info("1 record inserted, ID:" + str(lastID))


now =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info ("  ====>> JOB START RUN AT: "+ now)
print("  ====>> JOB START RUN AT: "+ now)
schedule.every(5).minutes.do(func)
  
while True:
    schedule.run_pending()
    time.sleep(1)