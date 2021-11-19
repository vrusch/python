import datetime
import mysql.connector
import schedule
import time
from KALT_config import *
import logging
import logging.handlers as handlers
import csv
import http.client


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
'''
logger = logging.getLogger('my_app')
logger.setLevel(logging.INFO)
logHandler = handlers.RotatingFileHandler('./log/channel_availability_test_upr.log', maxBytes=5242880, backupCount=5)
logHandler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)-0s %(levelname)-0s %(message)s")
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
'''

#stare logovani
httpclient_logger = logging.getLogger("http.client")

def httpclient_logging_patch(level=logging.DEBUG):
    """Enable HTTPConnection debug logging to the logging framework"""

    def httpclient_log(*args):
        httpclient_logger.log(level, " ".join(args))

    # mask the print() built-in in the http.client module to use
    # logging instead
    http.client.print = httpclient_log
    # enable debugging
    http.client.HTTPConnection.debuglevel = 1
httpclient_logging_patch()

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING, filename="./log/channel_availability_test_upr.log", filemode="a+",
                        format="%(asctime)-0s %(levelname)-0s %(message)s")

#kontrola souboru
'''
current_path = os.getcwd()
log_directory = current_path + '\log'
list_dir = os.listdir(log_directory)
if os.path.exists('./log/channel_availability_test_upr.log'):
    print("found")
    for item in list_dir:
        print(str(item))
        if item.endswith(".log"):

            i = os.remove(os.path.join(log_directory, item ) )
            print(str(i))
else:
    logger.info()
#os.path.exists('./'+inputfile)
logger.info("DELETED ALL LOG FILES ...")
'''

#ziskani credentials a API hlavicek, phoenixURL
credentials = user_login(partnerID, 4)
head = headers(partnerID)
headerPOST = head[0]
headerGET = head[1]
phoenixURL = head[2]

#ziskani user ks
ks = KALT_ks(apiVersion, partnerID, credentials[0], credentials[1], credentials[2], phoenixURL, headerPOST)
if ks == 'ERROR':
    logging.info("No login ks returned")
else:
    the_datetime = datetime. datetime. fromtimestamp(ks[3]) 
    logging.warning("[LOGIN]KS EXPIRATION: " + str(the_datetime))
    logging.info("[LOGIN]BE execution Time: "+str(ks[2]))
    logging.info("[LOGIN]Elapsed Time: "+str(ks[1]))
    logging.info("[LOGIN]User KS: " + ks[0])

def func():
    dateX =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.warning("======= THIST ROUND START: " + dateX + " ===============================================")
    #print("ROUND START: " + dateX)
    #otevrit csv a vrati stream
    with open(inputfile, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter = ';')
        for row in csvreader:
            channelNumber = row[2]
            channelName = row[0]
            assetId = row[1]
            logging.info("=============================================================================================")
            logging.warning("[TEST]Start test for channel name: " + channelName + " #" + channelNumber + " with ID: " + assetId)
            r = get_context(assetId, ks[0], headerPOST, phoenixURL)
            responseDASH = r[0].json()
            responseHLS = r[1].json()
            RelapsedDASH = r[2]
            RelapsedHLS = r[3]
            RQdate = r[4]


    #(assetId, codec, response , headerGET)
    #analyzeDASH -KALT
            logging.info("--> Start analyze DASH")
            if responseDASH != None:
                DASH_K_BE_execTime = responseDASH['executionTime']
                try:
                    DASH_K_url = responseDASH['result']['sources'][0]['url']
                    DASH_K_exit_msg = "OK"
                    DASH_K_payload = DASH_K_url
                    logging.info("[RESULT][KALT][DASH]["+channelName+"]["+channelNumber+"]REASON: OK --KALT returned URL")
                    DASH_kalt_reason = True
                except:
                    if responseDASH['result']:
                        Etype = responseDASH['result']['actions'][0]['type']
                        Emsg = responseDASH['result']['messages'][0]['message']
                        DASH_K_exit_msg = "ERROR"
                        DASH_K_payload = "--KALT Error type: " + Etype + "; Error reason: " + Emsg
                        logging.error("[ERROR][KALT][DASH]["+channelName+"]["+channelNumber+"]ERROR: --KALT not returned any URL")
                        logging.error("[ERROR][KALT][DASH]["+channelName+"]["+channelNumber+"]ERROR: type: " + Etype)
                        logging.error("[ERROR][KALT][DASH]["+channelName+"]["+channelNumber+"]ERROR: message: " + Emsg)
                        DASH_kalt_reason = False
                    else:
                        logging.error("[ERROR][KALT][DASH]["+channelName+"]["+channelNumber+"]ERROR: --not result?")
                        DASH_K_url = 'NONE'
                        DASH_K_exit_msg = "ERROR"
                        DASH_K_payload = "NONE RESULT"
                        DASH_kalt_reason = False

                #analyzeDASH -BRPK
                if DASH_kalt_reason:
                    logging.info("--> CONTINUE TEST FOR DASH -- STAGE BRPR")
                    GETresponse = requests.get(DASH_K_url, headers=headerGET, timeout=5)
                    get_responsecode = GETresponse.status_code
                    if get_responsecode == 200:
                        DASH_B_elapsed = GETresponse.elapsed.microseconds/1000000
                        logging.info("[RESULT][BRPK][DASH]["+channelName+"]["+channelNumber+"]Response reason: "+str(GETresponse.reason))
                        DASH_B_exit_msg = "OK" 
                        DASH_B_payload = "Status code: "+str(get_responsecode) 
                    else:
                        DASH_B_elapsed = GETresponse.elapsed.microseconds/1000000
                        logging.warning(str(GETresponse.content))
                        logging.error("[ERROR][BRPK][DASH]["+channelName+"]["+channelNumber+"]Response reason: "+str(GETresponse.reason))
                        logging.error("[ERROR][BRPK][DASH]["+channelName+"]["+channelNumber+"]Response status code: "+str(get_responsecode))
                        logging.error("[ERROR][BRPK][DASH]["+channelName+"]["+channelNumber+"]Elapsed time: "+str(DASH_B_elapsed)) 
                        DASH_B_exit_msg = "ERROR"
                        DASH_B_payload = "--BRPK not get Manifest. (wrong URL?) Reason: "+str(GETresponse.reason)+" Status code: "+str(get_responsecode)         

                else:
                    logging.warning("[RESULT][BRPK][DASH]["+channelName+"]["+channelNumber+"]ERROR: --KALT not returned any URL")
                    DASH_B_exit_msg = "ERROR"
                    DASH_B_payload = "--KALT not returned any URL"
                    DASH_B_elapsed = ""
            else:
                print('None')
                logging.error("[ERROR][DASH]["+channelName+"]["+channelNumber+"] SKIPED. NO RESPONSE?")

    #(assetId, codec, response , headerGET)
    #analyzeHLS: -KALT
            logging.info("--> Start analyze HLS")
            if responseHLS != None:
                HLS_K_BE_execTime = responseHLS['executionTime']
                try:
                    HLS_K_url = responseHLS['result']['sources'][0]['url']
                    HLS_K_exit_msg = "OK"
                    HLS_K_payload = HLS_K_url
                    logging.info("[RESULT][KALT][HLS]["+channelName+"]["+channelNumber+"]REASON: OK --KALT returned URL")
                    HLS_kalt_reason = True
                except:
                    if responseHLS['result']:
                        Etype = responseHLS['result']['actions'][0]['type']
                        Emsg = responseHLS['result']['messages'][0]['message']
                        HLS_K_exit_msg = "ERROR"
                        HLS_K_payload = "--KALT Error type: " + Etype + "; Error reason: " + Emsg
                        logging.error("[ERROR][KALT][HLS]["+channelName+"]["+channelNumber+"]ERROR: --KALT not returned any URL")
                        logging.error("[ERROR][KALT][HLS]["+channelName+"]["+channelNumber+"]ERROR: type: " + Etype)
                        logging.error("[ERROR][KALT][HLS]["+channelName+"]["+channelNumber+"]ERROR: message: " + Emsg)
                        HLS_kalt_reason = False
                    else:
                        logging.error("[ERROR][KALT][HLS]["+channelName+"]["+channelNumber+"]ERROR: --not result?")
                        HLS_K_url = 'NONE'
                        HLS_K_exit_msg = "ERROR"
                        HLS_K_payload = "NONE RESULT"
                        HLS_kalt_reason = False
                        

                #analyzeHLS -BRPK
                if HLS_kalt_reason:
                    logging.info("--> CONTINUE TEST FOR HLS -- STAGE BRPR")
                    GETresponse = requests.get(HLS_K_url, headers=headerGET, timeout=5)
                    get_responsecode = GETresponse.status_code
                    if get_responsecode == 200:
                        HLS_B_elapsed = GETresponse.elapsed.microseconds/1000000
                        logging.info("[RESULT][BRPK][HLS]["+channelName+"]["+channelNumber+"]Response reason: "+str(GETresponse.reason))
                        HLS_B_exit_msg = "OK" 
                        HLS_B_payload = "Status code: "+str(get_responsecode) 
                    else:
                        HLS_B_elapsed = GETresponse.elapsed.microseconds/1000000
                        logging.warning(str(GETresponse.content))
                        logging.error("[ERROR][BRPK][HLS]["+channelName+"]["+channelNumber+"]Response reason: "+str(GETresponse.reason))
                        logging.error("[ERROR][BRPK][HLS]["+channelName+"]["+channelNumber+"]Response status code: "+str(get_responsecode))
                        logging.error("[ERROR][BRPK][HLS]["+channelName+"]["+channelNumber+"]Elapsed time: "+str(HLS_B_elapsed)) 
                        HLS_B_exit_msg = "ERROR"
                        HLS_B_payload = "--BRPK not get Manifest. (wrong URL?) Reason: "+str(GETresponse.reason)+" Status code: "+str(get_responsecode)         
                else:
                    logging.warning("[RESULT][BRPK][HLS]["+channelName+"]["+channelNumber+"]ERROR: --KALT not returned any URL")
                    HLS_B_exit_msg = "ERROR"
                    HLS_B_payload = "--KALT not returned any URL"
                    HLS_B_elapsed = ""

                #date, partnerID, channel_num, channel_name, DASH_KALT, DASH_KALT_BE, DASH_K_exit_msg, DASH_BRPK, DASH_B_exit_msg, HLS_KALT, HLS_KALT_BE, HLS_K_exit_msg, HLS_BRPK, HLS_B_exit_msg, DASH_K_payload, DASH_B_payload, HLS_K_payload, HLS_B_payload
                mycursor = mydb.cursor()
                sql = "INSERT INTO channel_test_upr (date, partnerID, channel_num, channel_name, DASH_KALT, DASH_KALT_BE, DASH_K_exit_msg, DASH_BRPK, DASH_B_exit_msg, HLS_KALT, HLS_KALT_BE, HLS_K_exit_msg, HLS_BRPK, HLS_B_exit_msg, DASH_K_payload, DASH_B_payload, HLS_K_payload, HLS_B_payload) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (RQdate, partnerID, channelNumber, channelName, RelapsedDASH, DASH_K_BE_execTime, DASH_K_exit_msg, DASH_B_elapsed, DASH_B_exit_msg, RelapsedHLS, HLS_K_BE_execTime, HLS_K_exit_msg, HLS_B_elapsed, HLS_B_exit_msg, DASH_K_payload, DASH_B_payload, HLS_K_payload, HLS_B_payload) 
                mycursor.execute(sql, val)
                mydb.commit()
                lastID = mycursor.lastrowid
                logging.info("1 record inserted, ID:" + str(lastID))
                RQdate = ""
            else:
                print('None')
                logging.error("[ERROR][HLS]["+channelName+"]["+channelNumber+"] SKIPED. NO RESPONSE?")

schedule.every(5).minutes.do(func)
  
while True:
    schedule.run_pending()
    time.sleep(1)