import requests
import json
import csv
import datetime
import schedule
import time
import logging
import http.client


inputfile = "opc_tlrs.csv"
outputfileDASH = "output_DASH.csv"
outputfileHLS = "output_HLS.csv"
logfile = "get_manifest_test5min.log"


httpclient_logger = logging.getLogger("http.client")

def httpclient_logging_patch(level=logging.INFO):
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
    logging.basicConfig(level=logging.INFO, filename=logfile, filemode="a+",
                        format="%(asctime)-0s %(levelname)-0s %(message)s")

partnerID = "3200" 
phoenixURL = "https://3200.frp1.ott.kaltura.com/api_v3/service/"
apiVersion = "5.4.0"
clientTag = "0.13.0-PC"
language = "eng"
udid = "monitoring4_rs" 
username = "monitoring4_rs" 
password = "#-K_monitoring4_rs" 
header = {'Content-Type' : 'application/json', 'Host ' : '3200.frp1.ott.kaltura.com', 'Accept' : '*/*', 'Accept-Encoding' : 'gzip, deflate, br', 'Connection' : 'keep-alive'} 


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
json_response = response.json()
login_ks = json_response['result']['loginSession']['ks']
logging.info("USER KS: " + login_ks)



def func():
    #getPlaybackContext
    now =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print ("START: "+ now)
    logging.info("START: " + str(now))
    assetId = ""
    channelName = ""

    # reading csv file
    with open(inputfile, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter = ';')
        for row in csvreader:
            url = ""
            data = ""
            channelName = row[0]
            assetId = row[1]
            channelNumber = row[2]

            servis = "/asset/action/getPlaybackContext"
            data = {
                "assetId": assetId,
                "assetType": "media",
                "contextDataParams": {
                    "objectType": "KalturaPlaybackContextOptions",
                    "streamerType": "mpegdash",
                    "context": "PLAYBACK",
                    "urlType": "DIRECT",
                    "mediaProtocol": "https"
                },
                "ks": login_ks,
                "clientTag": clientTag,
                "language": language,
                "apiVersion": apiVersion
            }
            send = phoenixURL + servis
            logging.info("[KALT][DASH] TRY SEND POST REQUEST: etPlaybackContext --with "+channelName + " | " + assetId)
            try:
                response = ""
                response = requests.post(send, json.dumps(data), headers=header)
                elapsed = (response.elapsed.microseconds)/1000000
                json_response = response.json()
                url = json_response['result']['sources'][0]['url']
                DASH_kalt_reason = True
            except:
                object = json_response['result']['actions'][0]['type']
                messages = json_response['result']['messages'][0]['message']
                logging.error("[KALT][DASH] POST RESPONSE BAD: ERROR -- with "+channelName + " | " + assetId) 
                logging.error("[KALT][DASH]["+channelName+"]["+channelNumber+"]ERROR: -- KALT not returned URL")
                logging.error("[KALT][DASH]["+channelName+"]["+channelNumber+"]ERROR: type: "+ object)
                logging.error("[KALT][DASH]["+channelName+"]["+channelNumber+"]ERROR: message: "+ messages)   
                DASH_kalt_reason = False
        
            # get URL - manifest  DASH, BRPK
            logging.info("[BRPK][DASH] TRY SEND GET REQUEST: --with url: " + url)
            if DASH_kalt_reason:
                response = ""
                response = requests.get(url, headers=header)
                url = ""
                e1 = response.elapsed.microseconds/1000000
                e2 = elapsed
                JointE = round(e1 + e2, 6)

                now =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                sentense = channelName+","+now+",DASH,"+str(JointE)+"\n"
                f = open(outputfileDASH, "a")
                f.write(sentense)
                f.close()

            else: 
                logging.error("[BRPK][DASH] GET RESPONSE: ERROR --with url: " + url)
                logging.error("[BRPK][DASH]["+channelName+"]["+channelNumber+"]Response status code: "+str(response.status_code))
                now =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                sentense = channelName+","+now+",DASH,NaN\n"
                f = open(outputfileDASH, "a")
                f.write(sentense)
                f.close()
            


            # HLS
            data = ""
            url = ""
            data = {
                "assetId": assetId,
                "assetType": "media",
                "contextDataParams": {
                    "objectType": "KalturaPlaybackContextOptions",
                    "streamerType": "applehttp",
                    "context": "PLAYBACK",
                    "urlType": "DIRECT",
                    "mediaProtocol": "https"
                },
                "ks": login_ks,
                "clientTag": clientTag,
                "language": language,
                "apiVersion": apiVersion
            }
            send = phoenixURL + servis
            logging.info("[KALT][HLS] TRY SEND POST REQUEST: etPlaybackContext --with "+channelName + " | " + assetId)
            try:
                response = ""
                response = requests.post(send, json.dumps(data), headers=header)
                elapsed = (response.elapsed.microseconds)/1000000
                json_response = response.json()
                url = json_response['result']['sources'][0]['url']
                HLS_kalt_reason = True
            except:  
                object = json_response['result']['actions'][0]['type']
                messages = json_response['result']['messages'][0]['message']
                logging.error("[KALT][HLS] POST RESPONSE BAD: ERROR -- with "+channelName + " | " + assetId) 
                logging.error("[KALT][HLS]["+channelName+"]["+channelNumber+"]ERROR: -- KALT not returned URL")
                logging.error("[KALT][HLS]["+channelName+"]["+channelNumber+"]ERROR: type: "+ object)
                logging.error("[KALT][HLS]["+channelName+"]["+channelNumber+"]ERROR: message: "+ messages)
                HLS_kalt_reason = False
                
            # get URL - manifest HLS, BRPK
            logging.info("[BRPK][HLS] TRY SEND GET REQUEST: --with url: " + url)
            if HLS_kalt_reason == True:
                response = ""
                response = requests.get(url, headers=header)
                url = ""
                e1 = response.elapsed.microseconds/1000000
                e2 = elapsed
                JointE = round(e1 + e2, 6)

                now =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                sentense = channelName+","+now+",HLS,"+str(JointE)+"\n"
                f = open(outputfileHLS, "a")
                f.write(sentense)
                f.close()

            else:
                logging.error("[BRPK][HLS] GET RESPONSE: ERROR --with url: " + url)
                logging.error("[BRPK][DASH]["+channelName+"]["+channelNumber+"]Response status code: "+str(response.status_code))
                now =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                sentense = channelName+","+now+",HLS,NaN\n"
                f = open(outputfileHLS, "a")
                f.write(sentense)
                f.close()
                

now =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print ("START RUN: "+ now)

schedule.every(5).minutes.do(func)
  
while True:
    schedule.run_pending()
    time.sleep(1)
    
    

