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
logger = logging.getLogger('TLRS_avia_app')
logger.setLevel(logging.INFO)
logHandler = handlers.RotatingFileHandler('./log/TLRS_availability_channel_test.log', maxBytes=5242880, backupCount=5)
logHandler.setLevel(logging.WARNING)
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
    logger.error("No login ks returned")
else:
    ks_exp = datetime. datetime.fromtimestamp(ks[3])
    user_ks = ks[0] 
    ks_exp_check = ks_exp - datetime.timedelta(hours=2)
    logger.info("[LOGIN]USES USER: " + str(credentials[0]))
    logger.info("[LOGIN]KS EXPIRATION: " + str(ks_exp))
    logger.info("[LOGIN]KS : " + str(user_ks))
    logger.info("[LOGIN]KS CHANGE AT: " + str(ks_exp_check))


def func():
    dateX1 =  datetime.datetime.now()
    dateX1a =  dateX1.strftime("%Y-%m-%d %H:%M:%S")
    logger.info(" -> TEST ROUND START AT: " + dateX1a)

    #otevrit csv a vrati stream
    with open(inputfile, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter = ';')
        for row in csvreader:
            channelNumber = row[2]
            channelName = row[0]
            assetId = row[1]
            
            #kontrola platnosti ks
            global ks_exp
            global user_ks
            #ks_exp_check = datetime.datetime.strptime(ks_exp, '%Y-%m-%d %H:%M:%S')
            ks_exp_check = ks_exp - datetime.timedelta(hours=2)
            if datetime.datetime.now() > ks_exp_check:
                logger.warning("[LOGIN]KS EXPIRE SOON, SO CHANGE IT")
                logger.warning("[LOGIN]NEW KS EXPIRATION: " + str(ks_exp))
                ks = KALT_ks(apiVersion, partnerID, credentials[0], credentials[1], credentials[2], phoenixURL, headerPOST)
                ks_exp = datetime.datetime.fromtimestamp(ks[3]) 
                user_ks = ks[0]
                ks_exp_check = ks_exp - datetime.timedelta(hours=2)
                logger.warning("[LOGIN]KS CHANGE AT: " + str(ks_exp_check))

            logger.debug("[TEST]Start test for channel name: " + channelName + " #" + channelNumber + " with ID: " + assetId)
            r = get_context(assetId, user_ks, headerPOST, phoenixURL)
            responseDASH = r[0]
            responseHLS = r[1]
            RelapsedDASH = r[2]
            RelapsedHLS = r[3]
            RQdate = r[4]
            
        ############################################################################################################################################ 
        #analyzeDASH -KALT
            logger.debug("--> Start analyze DASH")
            if responseDASH != None:
                responseDASHraw = responseDASH
                responseDASH = responseDASH.json()
                DASH_K_BE_execTime = responseDASH['executionTime']
                try:
                    DASH_K_url = responseDASH['result']['sources'][0]['url']
                    DASH_K_exit_msg = "OK"
                    DASH_K_payload = DASH_K_url
                    logger.debug("[RESULT][DASH][KALT]["+channelName+"]["+channelNumber+"] OK --KALT returned URL")
                    DASH_kalt_reason = True
                except:
                    if responseDASH['result']:
                        logger.error("[ERROR][DASH][KALT]["+channelName+"]["+channelNumber+"] Response" + str(responseDASHraw.content))
                        Etype = responseDASH['result']['actions'][0]['type']
                        Emsg = responseDASH['result']['messages'][0]['message']
                        DASH_K_exit_msg = "ERROR"
                        DASH_K_payload = "--KALT Error type: " + Etype + "; Error reason: " + Emsg
                        logger.error("[ERROR][DASH][KALT]["+channelName+"]["+channelNumber+"] KALT not returned any URL")
                        logger.error("[ERROR][DASH][KALT]["+channelName+"]["+channelNumber+"] Type: " + Etype)
                        logger.error("[ERROR][DASH][KALT]["+channelName+"]["+channelNumber+"] Message: " + Emsg)
                        DASH_kalt_reason = False
                    else:
                        logger.error("[ERROR][DASH][KALT]["+channelName+"]["+channelNumber+"] KALT not result")
                        DASH_K_url = 'NONE'
                        DASH_K_exit_msg = "ERROR"
                        DASH_K_payload = "NONE RESULT"
                        DASH_kalt_reason = False
                        RelapsedDASH = 'NaN'

                #analyzeDASH -BRPK
                if DASH_kalt_reason:
                    TIMEOUT = 0
                    logger.debug("--> CONTINUE TEST FOR DASH -- STAGE BRPR")
                    try: 
                        GETresponse = requests.get(DASH_K_url, headers=headerGET, timeout=8)
                    except requests.exceptions.Timeout: 
                        TIMEOUT = 1
  
                    if TIMEOUT == 0:
                        get_responsecode = GETresponse.status_code
                        if get_responsecode == 200:
                            DASH_B_elapsed = GETresponse.elapsed.total_seconds()
                            logger.debug("[RESULT][DASH][BRPK]["+channelName+"]["+channelNumber+"]Response reason: "+str(GETresponse.reason))
                            DASH_B_exit_msg = "OK" 
                            DASH_B_payload = "Status code: "+str(get_responsecode) 
                        else:
                            #DASH_B_elapsed = GETresponse.elapsed.microseconds/1000000
                            DASH_B_elapsed = 'NaN'
                            logger.error("[ERROR][DASH][BRPK]["+channelName+"]["+channelNumber+"]Response: "+str(GETresponse.content))
                            logger.error("[ERROR][DASH][BRPK]["+channelName+"]["+channelNumber+"]URL: "+DASH_K_url)
                            logger.error("[ERROR][DASH][BRPK]["+channelName+"]["+channelNumber+"]Response reason: "+str(GETresponse.reason))
                            logger.error("[ERROR][DASH][BRPK]["+channelName+"]["+channelNumber+"]Response status code: "+str(get_responsecode))
                            logger.error("[ERROR][DASH][BRPK]["+channelName+"]["+channelNumber+"]Elapsed time: "+str(DASH_B_elapsed)) 
                            DASH_B_exit_msg = "ERROR"
                            DASH_B_payload = "--BRPK not get Manifest. (wrong URL?) Reason: "+str(GETresponse.reason)+" Status code: "+str(get_responsecode) 
                    else:
                        logger.error("[ERROR][DASH][BRPK]["+channelName+"]["+channelNumber+"] GET REQUEST TIMEOUT (8s)")
                        logger.error("[ERROR][DASH][BRPK]["+channelName+"]["+channelNumber+"] URL: "+DASH_K_url)
                        DASH_B_elapsed = 'NaN'
                        DASH_B_exit_msg = 'ERROR'
                        DASH_B_payload = 'GET REQUEST TIMEOUT (8s)'

                else:
                    logger.error("[ERROR][DASH][BRPK]["+channelName+"]["+channelNumber+"] KALT not returned any URL")
                    DASH_B_exit_msg = "ERROR"
                    DASH_B_payload = "--KALT not returned any URL"
                    DASH_B_elapsed = 'NaN'
            else:
                logger.error("[ERROR][DASH][KALT]["+channelName+"]["+channelNumber+"] SKIPED. NO RESPONSE ...POST TIMEOUT (5s)")
                #RelapsedDASH, DASH_K_BE_execTime, DASH_K_exit_msg, DASH_B_elapsed, DASH_B_exit_msg, DASH_K_payload, DASH_B_payload
                RelapsedDASH = 'NaN'
                DASH_K_BE_execTime = 'NaN'
                DASH_K_exit_msg = "ERROR"
                DASH_B_elapsed = 'NaN'
                DASH_B_exit_msg = "ERROR"
                DASH_K_payload = "DASH SKIPED. NO RESPONSE ...POST TIMEOUT (5s)"
                DASH_B_payload = "--KALT not returned any URL"

        ############################################################################################################################################  
        #analyzeHLS: -KALT
            logger.debug("--> Start analyze HLS")
            if responseHLS != None:
                responseHLSraw = responseHLS
                responseHLS = responseHLS.json()
                HLS_K_BE_execTime = responseHLS['executionTime']
                try:
                    HLS_K_url = responseHLS['result']['sources'][0]['url']
                    HLS_K_exit_msg = "OK"
                    HLS_K_payload = HLS_K_url
                    logger.debug("[RESULT][HLS][KALT]["+channelName+"]["+channelNumber+"] OK --KALT returned URL")
                    HLS_kalt_reason = True
                except:
                    if responseHLS['result']:
                        logger.error("[ERROR][HLS][KALT]["+channelName+"]["+channelNumber+"] Response" + str(responseHLSraw.content))
                        Etype = responseHLS['result']['actions'][0]['type']
                        Emsg = responseHLS['result']['messages'][0]['message']
                        HLS_K_exit_msg = "ERROR"
                        HLS_K_payload = "--KALT Error type: " + Etype + "; Error reason: " + Emsg
                        logger.error("[ERROR][HLS][KALT]["+channelName+"]["+channelNumber+"] KALT not returned any URL")
                        logger.error("[ERROR][HLS][KALT]["+channelName+"]["+channelNumber+"] Type: " + Etype)
                        logger.error("[ERROR][HLS][KALT]["+channelName+"]["+channelNumber+"] Message: " + Emsg)
                        HLS_kalt_reason = False
                    else:
                        logger.error("[ERROR][HLS][KALT]["+channelName+"]["+channelNumber+"] KALT not result")
                        RelapsedHLS = 'NaN'
                        HLS_K_url = 'NONE'
                        HLS_K_exit_msg = "ERROR"
                        HLS_K_payload = "NONE RESULT"
                        HLS_kalt_reason = False
                        
                #analyzeHLS -BRPK
                if HLS_kalt_reason:
                    TIMEOUT = 0
                    logger.debug("--> CONTINUE TEST FOR HLS -- STAGE BRPR")
                    try: 
                        GETresponse = requests.get(HLS_K_url, headers=headerGET, timeout=8)
                    except requests.exceptions.Timeout: 
                        TIMEOUT = 1
                    
                    if TIMEOUT == 0:
                        get_responsecode = GETresponse.status_code
                        if get_responsecode == 200:
                            HLS_B_elapsed = GETresponse.elapsed.total_seconds()
                            logger.debug("[RESULT][HLS][BRPK]["+channelName+"]["+channelNumber+"]Response reason: "+str(GETresponse.reason))
                            HLS_B_exit_msg = "OK" 
                            HLS_B_payload = "Status code: "+str(get_responsecode) 
                        else:
                            #HLS_B_elapsed = GETresponse.elapsed.microseconds/1000000
                            HLS_B_elapsed = 'NaN'
                            logger.error("[ERROR][HLS][BRPK]["+channelName+"]["+channelNumber+"]Response: "+str(GETresponse.content))
                            logger.error("[ERROR][HLS][BRPK]["+channelName+"]["+channelNumber+"]URL: "+HLS_K_url)
                            logger.error("[ERROR][HLS][BRPK]["+channelName+"]["+channelNumber+"]Response reason: "+str(GETresponse.reason))
                            logger.error("[ERROR][HLS][BRPK]["+channelName+"]["+channelNumber+"]Response status code: "+str(get_responsecode))
                            logger.error("[ERROR][HLS][BRPK]["+channelName+"]["+channelNumber+"]Elapsed time: "+str(HLS_B_elapsed)) 
                            HLS_B_exit_msg = "ERROR"
                            HLS_B_payload = "--BRPK not get Manifest. (wrong URL?) Reason: "+str(GETresponse.reason)+" Status code: "+str(get_responsecode) 
                    else:
                        logger.error("[ERROR][HLS][BRPK]["+channelName+"]["+channelNumber+"] GET REQUEST TIMEOUT (8s)")
                        logger.error("[ERROR][HLS][BRPK]["+channelName+"]["+channelNumber+"] URL: "+HLS_K_url)
                        HLS_B_elapsed = 'NaN'
                        HLS_B_exit_msg = 'ERROR'
                        HLS_B_payload = 'GET REQUEST TIMEOUT (8s)'  
                             
                else:
                    logger.error("[ERROR][HLS][BRPK]["+channelName+"]["+channelNumber+"] KALT not returned any URL")
                    HLS_B_exit_msg = "ERROR"
                    HLS_B_payload = "--KALT not returned any URL"
                    HLS_B_elapsed = 'NaN'

            else:
                logger.error("[ERROR][HLS][KALT]["+channelName+"]["+channelNumber+"] SKIPED. NO RESPONSE ...POST TIMEOUT (5s)")
                #RelapsedHLS, HLS_K_BE_execTime, HLS_K_exit_msg, HLS_B_elapsed, HLS_B_exit_msg, HLS_K_payload, HLS_B_payload
                RelapsedHLS = 'NaN'
                HLS_K_BE_execTime = 'NaN'
                HLS_K_exit_msg = "ERROR"
                HLS_B_elapsed = 'NaN'
                HLS_B_exit_msg = "ERROR"
                HLS_K_payload = "HLS SKIPED. NO RESPONSE ...POST TIMEOUT (5s)"
                HLS_B_payload = "--KALT not returned any URL"

            #date, partnerID, channel_num, channel_name, DASH_KALT, DASH_KALT_BE, DASH_K_exit_msg, DASH_BRPK, DASH_B_exit_msg, HLS_KALT, HLS_KALT_BE, HLS_K_exit_msg, HLS_BRPK, HLS_B_exit_msg, DASH_K_payload, DASH_B_payload, HLS_K_payload, HLS_B_payload
            mycursor = mydb.cursor()
            sql = "INSERT INTO channel_test_upr (date, partnerID, channel_num, channel_name, DASH_KALT, DASH_KALT_BE, DASH_K_exit_msg, DASH_BRPK, DASH_B_exit_msg, HLS_KALT, HLS_KALT_BE, HLS_K_exit_msg, HLS_BRPK, HLS_B_exit_msg, DASH_K_payload, DASH_B_payload, HLS_K_payload, HLS_B_payload) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (RQdate, partnerID, channelNumber, channelName, RelapsedDASH, DASH_K_BE_execTime, DASH_K_exit_msg, DASH_B_elapsed, DASH_B_exit_msg, RelapsedHLS, HLS_K_BE_execTime, HLS_K_exit_msg, HLS_B_elapsed, HLS_B_exit_msg, DASH_K_payload, DASH_B_payload, HLS_K_payload, HLS_B_payload) 
            mycursor.execute(sql, val)
            mydb.commit()
            lastID = mycursor.lastrowid
            logger.debug("1 record inserted, ID:" + str(lastID))
            logger.debug("Values:" + str(val))
            RQdate = ""

    dateX2 =  datetime.datetime.now()
    dateX2a =  dateX2.strftime("%Y-%m-%d %H:%M:%S")
    dateX3 = dateX2 - dateX1
    logger.info(" <- TEST ROUND STOP AT: " + dateX2a + " (lap time: "+ str(dateX3) + ")")

schedule.every(5).seconds.do(func)
  
while True:
    schedule.run_pending()
    time.sleep(1)