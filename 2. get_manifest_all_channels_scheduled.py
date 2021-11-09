import datetime
from KALT_config import *
import logging
import logging.handlers as handlers

#logovani a rotovani logu
logger = logging.getLogger('my_app')
logger.setLevel(logging.INFO)
logHandler = handlers.RotatingFileHandler('app.log', maxBytes=30000500, backupCount=5)
logHandler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)-0s %(levelname)-0s %(message)s")
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

#specificke promenne pro test
partnerID = '3200'
inputfile = "opc_tlrs.csv"

#ziskani credentials a API hlavicek, phoenixURL
credentials = user_login(partnerID, 3)
head = headers(partnerID)
headerPOST = head[0]
phoenixURL = head[2]

#ziskani user ks
ks = KALT_ks(apiVersion, partnerID, credentials[0], credentials[1], credentials[2], phoenixURL, headerPOST)
if ks == 'ERROR':
    logger.info("No login ks returned")
else:
    logger.info("[LOGIN]BE execution Time: "+str(ks[2]))
    logger.info("[LOGIN]Elapsed Time: "+str(ks[1]))
    logger.info("[LOGIN]User KS: " + ks[0])

#otevrit csv a vrati stream
with open(inputfile, 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter = ';')
    for row in csvreader:
        channelNumber = row[2]
        channelName = row[0]
        assetId = row[1]
        logger.info("[TEST]Start test for channel name: " + channelName + " #" + channelNumber + " with ID: " + assetId)
        r = get_manifest_test(assetId, ks[0], headerPOST, phoenixURL)
        responseDASH = r[0].json()
        responseHLS = r[1].json()


        #analyzeDASH
        logger.info("[TEST]Start analyze DASH")
        KALT_Relapsed = r[2]
        KALT_executionTime = responseDASH['executionTime']
        try:
            urlDASH = responseDASH['result']['sources'][0]['url']
            exit_msg = "OK: --KALT returned URL"
            payload = urlDASH
            logger.info("[RESULT][KALT][DASH]["+channelName+"]["+channelNumber+"]REASON: OK --KALT returned URL")
            DASH_kalt_reason = True
        except:
            Etype = responseDASH['result']['actions'][0]['type']
            Emsg = responseDASH['result']['messages'][0]['message']
            exit_msg = "ERROR: --KALT not returned any URL"
            payload = "ERROR type: " + Etype + "; Error reason: " + Emsg
            logger.error("[RESULT][KALT][DASH]["+channelName+"]["+channelNumber+"]ERROR: --KALT not returned any URL")
            logger.error("[RESULT][KALT][DASH]["+channelName+"]["+channelNumber+"]ERROR: type: " + Etype)
            logger.error("[RESULT][KALT][DASH]["+channelName+"]["+channelNumber+"]ERROR: message: " + Emsg)
            DASH_kalt_reason = False
        finally:
            #partnerID, channel#, name, date, codec, stage ,Relapsed, BEelapsed, exit_msg, payload
            date =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql = "INSERT INTO channel_test (partnerID, channel_number, channel_name, date, stage, Relapsed, BEelapsed, exit_msg, payload) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (partnerID, channelNumber, channelName, date, 'DASH', KALT_Relapsed, KALT_executionTime, exit_msg, payload)
            print(val)
            #zapis do db vrat ID