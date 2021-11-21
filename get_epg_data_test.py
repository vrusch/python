import requests
import json
import logging
import datetime
import csv
import logging.handlers as handlers

logger = logging.getLogger('my_app')
logger.setLevel(logging.INFO)
logHandler = handlers.RotatingFileHandler('./log/epg_data_test.log', maxBytes=50500500, backupCount=4)
logHandler.setLevel(logging.ERROR)
formatter = logging.Formatter("%(asctime)-0s %(levelname)-0s %(message)s")
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)



partnerID = "3200" 
phoenixURL = "https://3200.frp1.ott.kaltura.com/api_v3/service/"
apiVersion = "5.4.0"
clientTag = "0.13.0-PC"
language = "eng"
udid = "monitoring3_rs" 
username = "monitoring3_rs" 
password = "#-K_monitoring3_rs" 
header = {'Content-Type' : 'application/json', 'Host ' : '3200.frp1.ott.kaltura.com', 'Accept' : '*/*', 'Accept-Encoding' : 'gzip, deflate, br', 'Connection' : 'keep-alive'} 

def http_log(response):
    #logger.debug(http.client.responses)
    logger.debug(response.request.path_url)
    logger.debug(response.request.headers)
    logger.debug(response.request.body)
    logger.debug(response.reason)
    logger.debug(response.status_code)
    logger.debug(response.headers)
    logger.debug(response.content)

#login ks
servis = "OTTUser/action/login"
data = {   
	    "apiVersion": apiVersion,
        "partnerId": partnerID,
        "username": username,
        "password": password,
        "udid": udid,
    }
send = phoenixURL + servis
response = requests.post(send, json.dumps(data), headers=header)
http_log(response)
logger.info("Try get User KS with: ")
logger.info("apiVersion: "+ apiVersion)
logger.info("partnerId: "+ partnerID)
logger.info("username: "+ username)
logger.info("udid: "+ udid)
json_response = response.json()
login_ks = json_response['result']['loginSession']['ks']
logger.info("User KS: "+ login_ks)

inputfile = "opc_tlrs.csv"
assetId = ""
channelName = ""
channelNumber = ""
chyby = {}
chyby_pod = {}
chyby_poc = 0
pod_chyby_poc = 0

#date +- 7 days
d1 = ((datetime.datetime.now() - datetime.timedelta(days=7)).date())
d2 = ((datetime.datetime.now() + datetime.timedelta(days=7)).date())

myformat = "%Y-%m-%d"

mydt_ago = datetime.datetime.strptime(str(d1), myformat)
mydt_next = datetime.datetime.strptime(str(d2), myformat)
ago7_epoch = round(mydt_ago.timestamp())
next7_epoch = round(mydt_next.timestamp())

#print(mydt_ago)
#print(mydt_next)
#print(ago7_epoch)
#print(next7_epoch)

# reading csv file
with open(inputfile, 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile, delimiter = ';')
    logger.info("CSV: " + inputfile + " opened")
    # extracting each data row one by one
    for row in csvreader:
        channelNumber = row[2]
        channelName = row[0]
        assetId = row[1]
        logger.info("")
        logger.info("***** START NEW TEST ***** at: "+str(datetime.datetime.now())+ "*****")
        logger.info("")
        logger.info("[TEST_NAME] TEST EPG FOR: " +channelName+ " Channel number: "+channelNumber+ " with assetID: "+assetId)
        logger.info("[TEST_NAME] TEST EPG period from: " +str(mydt_ago)+ " to: "+str(mydt_next))
        servis = "/asset/action/list"
        data = {
            "language": language,
            "ks": login_ks,
            "filter": {
                "objectType": "KalturaSearchAssetFilter",
                "kSql": "(and linear_media_id:'"+assetId+"' (or ( and end_date >= '"+str(ago7_epoch)+"') ( and start_date  <= '"+str(next7_epoch)+"')) asset_type='epg' auto_fill= true)",
                "orderBy": "START_DATE_ASC",
            },
            "pager": {
                "objectType": "KalturaFilterPager",
                "pageSize": 200,
                "pageIndex": 1
            },
            "clientTag": clientTag,
            "apiVersion": apiVersion
        }
        send = phoenixURL + servis
        response = requests.post(send, json.dumps(data), headers=header)
        json_response = response.json()
        executionTime = json_response['executionTime']
        
        try:
            totalCount = json_response['result']['totalCount']
            objects = json_response['result']['objects']
            logger.info("executionTime: "+str(executionTime))
            logger.info("totalCount: "+str(totalCount))
        except:
            logger.error("[RESULT][KALT]["+channelName+"]["+channelNumber+"]ERROR: --KALT returned error answer")
            logger.error("[RESULT][KALT]["+str(json_response))

        if int(totalCount) <= 10 :
            pod_chyby_poc = pod_chyby_poc +1
            print(" ++> less than 10 items")
            logger.error(" ++> less than 10 items")
            
            chyby_pod[pod_chyby_poc] = channelName
        
            
                    


        oedate = ""
        oetime_stamp = ""
        for object in objects:
            stime_stamp = object['startDate']
            etime_stamp = object['endDate']
            sdate = datetime.datetime.fromtimestamp(object['startDate']).strftime('%Y-%m-%d %H:%M:%S')
            edate = datetime.datetime.fromtimestamp(object['endDate']).strftime('%Y-%m-%d %H:%M:%S')

            pname = object['name']
            print("===================================")
            print(object['name'])
            print(oedate)
            print(sdate)
            print(edate)
        
            logger.debug("Name: "+pname)
            logger.debug("previous end: "+oedate+" : "+str(oetime_stamp))
            logger.debug("START: ==> "+sdate+" : "+str(stime_stamp))
            logger.debug("END: <== "+edate+" : "+str(etime_stamp))
            if oedate == sdate:
                print("STATUS OK")
                logger.info("STATUS OK")
            elif oedate == "":
                print("<==>")
                logger.debug("just starting its ok")
            else:
                print("error")
                logger.error("ERROR ==== wrong items")
                logger.error("Name: "+pname)
                logger.error("previous end: "+oedate+" : "+str(oetime_stamp))
                logger.error("START: ==> "+sdate+" : "+str(stime_stamp))
                logger.error("END: <== "+edate+" : "+str(etime_stamp))
                chyby_poc = chyby_poc + 1
                if channelName not in chyby:
                    chyby[channelName] = {}

                if pname not in chyby[channelName]:
                    chyby[channelName][pname] = {}

                chyby[channelName][pname] = "previous end: "+oedate, oetime_stamp, "beginning of another: "+sdate, stime_stamp
                        
            oedate = edate
            opname = pname
            ostime_stamp = stime_stamp
            oetime_stamp = etime_stamp


print("=== END ====")
print("suspicious EPG (less than 10 items): "+str(pod_chyby_poc))
print (chyby_pod)
print("´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´")
print("gaps or overlaps in the EPG: "+str(chyby_poc))
print (json.dumps(chyby, indent=4))

logger.error("=== END ====")
logger.error(json.dumps(chyby, indent=4))
logger.error("suspicious EPG (less than 10 items): "+str(pod_chyby_poc))
logger.error (chyby_pod)
logger.error("+++++++++++++++++++++++++++++++++++++++++++++++++++")
logger.error("gaps or overlaps in the EPG: "+str(chyby_poc))
