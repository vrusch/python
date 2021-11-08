import requests
import json
import logging
import http.client
import csv
import datetime


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="get_manifest_test.log", filemode="a+",
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
inputfile = "opc_tlrs.csv"


def http_log(response):
    #logging.info(http.client.responses)
    logging.debug(response.request.path_url)
    logging.debug(response.request.headers)
    logging.debug(response.request.body)
    logging.debug(response.reason)
    logging.debug(response.status_code)
    logging.debug(response.headers)
    logging.debug(response.content)


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
logging.debug(http.client.responses)
elapsed = (response.elapsed.microseconds)/1000000
#print(response.request.body)
json_response = response.json()
executionTime = json_response['executionTime']
login_ks = json_response['result']['loginSession']['ks']
print("Elapsed time: " +str(elapsed))
print("BE execution Time: "+str(executionTime))
logging.info("[LOGIN]USER KS: " + login_ks)
logging.info("[LOGIN]BE execution Time: "+str(executionTime))
logging.info("[LOGIN]Elapsed Time: "+str(elapsed))


#getPlaybackContext
assetId = ""
channelName = ""
channelNumber = ""
rows = []
chyby = {}
poc = 0
# reading csv file
with open(inputfile, 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile, delimiter = ';')
    logging.info("CSV: " + inputfile + " opened")

    # extracting each data row one by one
    for row in csvreader:
        url = ""
        data = ""
        poc = poc +1
        rows.append(row) 
        channelNumber = row[2]
        channelName = row[0]
        assetId = row[1]
        logging.info("")
        print("")
        logging.info("")
        print("")
        logging.info("#######################################################################################")
        logging.info("[TEST_NAME] TEST FOR: " +channelName+ " Channel number: "+channelNumber+ " with assetID: "+assetId)
        logging.info("#######################################################################################")

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
        print("--> STRART TEST FOR DASH -- STAGE KALT")
        logging.info("--> STRART TEST FOR DASH -- STAGE KALT")
        send = phoenixURL + servis
        response = requests.post(send, json.dumps(data), headers=header)
        elapsed = (response.elapsed.microseconds)/1000000
        #print(response.request.body)
        json_response = response.json()
        try:
            executionTime = json_response['executionTime']
            url = json_response['result']['sources'][0]['url']
            print("Channel name: "+channelName)
            print("Channel #: "+channelNumber)
            print("assetId: "+assetId)
            print("Time backend: "+str(executionTime))
            print("Time request: "+str(elapsed))
            print("REASON OK: --KALT returned URL, OK")
            #print("[RESULT][KALT][DASH]["+channelName+"]["+channelNumber+"]URL: "+url)
            logging.info("[RESULT][KALT][DASH]["+channelName+"]["+channelNumber+"]REASON: OK --KALT returned URL")
            logging.info("[RESULT][KALT][DASH]["+channelName+"]["+channelNumber+"]BE Elapsed: "+str(executionTime))
            logging.info("[RESULT][KALT][DASH]["+channelName+"]["+channelNumber+"]Request eleapsed: "+str(elapsed))
            logging.info("[RESULT][KALT][DASH]["+channelName+"]["+channelNumber+"]URL: "+url)
            exit_msg = "OK: --KALT returned URL"
            payl = url
            DASH_kalt_reason = True
        
        except:
            executionTime = json_response['executionTime']
            object = json_response['result']['actions'][0]['objectType']
            object1 = json_response['result']['actions'][0]['type']
            messages = json_response['result']['messages'][0]['objectType']
            messages1 = json_response['result']['messages'][0]['message']
            messages2 = json_response['result']['messages'][0]['code']
            print("Channel name: "+channelName)
            print("Channel #: "+channelNumber)
            print("assetId: "+assetId)
            print("Time backend: "+str(executionTime))
            print("Time request: "+str(elapsed))
            print("Kaltura error type: "+object1)
            print("Kaltura error message: "+messages1)
            print("KALT REASON ERROR: --KALT not returned any URL")
            #print("[RESULT][KALT][DASH]["+channelName+"]["+channelNumber+"]URL: "+url)
            logging.error("[RESULT][KALT][DASH]["+channelName+"]["+channelNumber+"]ERROR: --KALT not returned any URL")
            logging.error("[RESULT][KALT][DASH]["+channelName+"]["+channelNumber+"]ERROR: type: "+object1)
            logging.error("[RESULT][KALT][DASH]["+channelName+"]["+channelNumber+"]ERROR: message: "+messages1)
            logging.error("[RESULT][KALT][DASH]["+channelName+"]["+channelNumber+"]ERROR: BE Elapsed: "+str(executionTime))
            logging.error("[RESULT][KALT][DASH]["+channelName+"]["+channelNumber+"]ERROR: Request eleapsed: "+str(elapsed))
            exit_msg = "ERROR: --KALT not returned any URL"
            payl = "ERROR type: "+object1+" Error reason: "+messages1
            if channelName not in chyby:
                chyby[channelName] = {}
            if 'DASH' not in chyby[channelName]:
                chyby[channelName]['DASH'] = {}
            chyby[channelName]['DASH']['KALT'] = 'ERROR'

            #print("CSV row: " + str(poc))   
            DASH_kalt_reason = False
        finally:
            #partnerID, channel#, name, date, codec, stage ,Relapsed, BEelapsed, exit_msg, payload
            #---------------------------------------------------------
            # zapsat do DB
            now =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sentense = partnerID+","+channelNumber+","+channelName+","+now+",DASH,KALT,"+str(elapsed)+","+str(executionTime)+","+exit_msg+","+payl+"\n"
            f = open('output.csv', "a")
            f.write(sentense)
            f.close()
        

        # get URL - manifest  DASH, BRPK
        response = ""
        if DASH_kalt_reason:
            print("--> CONTINUE TEST FOR DASH -- STAGE BRPR")
            logging.info("--> CONTINUE TEST FOR DASH -- STAGE BRPR")
            response = requests.get(url, headers=header)
            url = ""
            get_responsecode = response.status_code
            if get_responsecode == 200:
                print("Response reason: "+str(response.reason))
                print("Response status code: "+str(response.status_code))
                print("Elapsed time: "+str(response.elapsed.microseconds/1000000))
                e1 = response.elapsed.microseconds/1000000
                e2 = elapsed
                JointE = round(e1 + e2, 6)
                print("Joint elapsed time: "+str(JointE))
                logging.info("[RESULT][BRPK][DASH]["+channelName+"]["+channelNumber+"]Response reason: "+str(response.reason))
                logging.info("[RESULT][BRPK][DASH]["+channelName+"]["+channelNumber+"]Response status code: "+str(response.status_code))
                logging.info("[RESULT][BRPK][DASH]["+channelName+"]["+channelNumber+"]Elapsed time: "+str(response.elapsed.microseconds/1000000))
                logging.info("[RESULT][BRPK][DASH]["+channelName+"]["+channelNumber+"]Joint elapsed time: "+str(JointE)) 

                exit_msg = "OK: --BRPK returned Manifest" 
                payl = "Reason: "+str(response.reason)+" Status code: "+str(get_responsecode)
                e1 = e1 
            else:
                print("Response reason: "+str(response.reason))
                print("Response status code: "+str(response.status_code))
                print("Elapsed time: "+str(response.elapsed.microseconds/1000000))
                e1 = response.elapsed.microseconds/1000000
                e2 = elapsed
                JointE = round(e1 + e2, 6)
                print("Joint elapsed time: "+str(JointE))
                logging.error("[RESULT][BRPK][DASH]["+channelName+"]["+channelNumber+"]Response reason: "+str(response.reason))
                logging.error("[RESULT][BRPK][DASH]["+channelName+"]["+channelNumber+"]Response status code: "+str(response.status_code))
                logging.error("[RESULT][BRPK][DASH]["+channelName+"]["+channelNumber+"]Elapsed time: "+str(response.elapsed.microseconds/1000000))
                logging.error("[RESULT][BRPK][DASH]["+channelName+"]["+channelNumber+"]Joint elapsed time: "+str(JointE)) 

                exit_msg = "ERROR: --BRPK not get Manifest. (wrong URL?)"
                payl = payl = "Reason: "+str(response.reason)+" Status code: "+str(get_responsecode)
                e1 = e1   

                if channelName not in chyby:
                    chyby[channelName] = {}
                if 'DASH' not in chyby[channelName]:
                    chyby[channelName]['DASH'] = {}
                chyby[channelName]['DASH']['BRPK'] = 'ERROR'       

                DASH_brpk_reason = True
                data = ""
                url = ""
                response = ""
        else:
            print(("BRPK REASON ERROR: --KALT not returned any URL"))
            logging.warn("[RESULT][BRPK][DASH]["+channelName+"]["+channelNumber+"]ERROR: --KALT not returned any URL")
            logging.warn("[RESULT][BRPK][DASH]["+channelName+"]["+channelNumber+"]ERROR: Response status code: NONE")
            logging.warn("[RESULT][BRPK][DASH]["+channelName+"]["+channelNumber+"]ERROR: Elapsed time: NONE")

            if channelName not in chyby:
                chyby[channelName] = {}
            if 'DASH' not in chyby[channelName]:
                chyby[channelName]['DASH'] = {}
            chyby[channelName]['DASH']['BRPK'] = 'ERROR'

            exit_msg = "ERROR: --KALT not returned any URL"
            payl = ""
            e1 = ""

            DASH_brpk_reason = False
            data = ""
            url = ""
            response = ""

        #partnerID, channel#, name, date, codec, stage ,Relapsed, BEelapsed, exit_msg, payload
        #---------------------------------------------------------
        # zapsat do DB
        now =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sentense = partnerID+","+channelNumber+","+channelName+","+now+",DASH,BRPK,"+str(e1)+",NaN,"+exit_msg+","+payl+"\n"
        f = open('output.csv', "a")
        f.write(sentense)
        f.close()
        



        # HLS
        data = ""
        url = ""
        response = ""
        
        servis = "/asset/action/getPlaybackContext"
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
        print("--> STRART TEST FOR HLS -- STAGE KALT")
        logging.info("--> STRART TEST FOR HLS -- STAGE KALT")
        send = phoenixURL + servis
        response = requests.post(send, json.dumps(data), headers=header)
        elapsed = (response.elapsed.microseconds)/1000000
        #print(response.request.body)
        json_response = response.json()
        try:
            executionTime = json_response['executionTime']
            url = json_response['result']['sources'][0]['url']
            print("Channel name: "+channelName)
            print("Channel #: "+channelNumber)
            print("assetId: "+assetId)
            print("Time backend: "+str(executionTime))
            print("Time request: "+str(elapsed))
            print("REASON OK: --KALT returned URL, OK")
            #print("[RESULT][KALT][DASH]["+channelName+"]["+channelNumber+"]URL: "+url)
            logging.info("[RESULT][HLS][DASH]["+channelName+"]["+channelNumber+"]REASON: OK --KALT returned URL")
            logging.info("[RESULT][HLS][DASH]["+channelName+"]["+channelNumber+"]BE Elapsed: "+str(executionTime))
            logging.info("[RESULT][HLS][DASH]["+channelName+"]["+channelNumber+"]Request eleapsed: "+str(elapsed))
            logging.info("[RESULT][HLS][DASH]["+channelName+"]["+channelNumber+"]URL: "+url)
            exit_msg = "OK: --KALT returned URL"
            payl = url
            DASH_kalt_reason = True
        
        except:
            executionTime = json_response['executionTime']
            object = json_response['result']['actions'][0]['objectType']
            object1 = json_response['result']['actions'][0]['type']
            messages = json_response['result']['messages'][0]['objectType']
            messages1 = json_response['result']['messages'][0]['message']
            messages2 = json_response['result']['messages'][0]['code']
            print("Channel name: "+channelName)
            print("Channel #: "+channelNumber)
            print("assetId: "+assetId)
            print("Time backend: "+str(executionTime))
            print("Time request: "+str(elapsed))
            print("Kaltura error type: "+object1)
            print("Kaltura error message: "+messages1)
            print("KALT REASON ERROR: --KALT not returned any URL")
            #print("[RESULT][KALT][DASH]["+channelName+"]["+channelNumber+"]URL: "+url)
            logging.error("[RESULT][KALT][DASH]["+channelName+"]["+channelNumber+"]ERROR: --KALT not returned any URL")
            logging.error("[RESULT][KALT][DASH]["+channelName+"]["+channelNumber+"]ERROR: type: "+object1)
            logging.error("[RESULT][KALT][DASH]["+channelName+"]["+channelNumber+"]ERROR: message: "+messages1)
            logging.error("[RESULT][KALT][DASH]["+channelName+"]["+channelNumber+"]ERROR: BE Elapsed: "+str(executionTime))
            logging.error("[RESULT][KALT][DASH]["+channelName+"]["+channelNumber+"]ERROR: Request eleapsed: "+str(elapsed))
            exit_msg = "ERROR: --KALT not returned any URL"
            payl = "ERROR type: "+object1+" Error reason: "+messages1
            if channelName not in chyby:
                chyby[channelName] = {}
            if 'HLS' not in chyby[channelName]:
                chyby[channelName]['HLS'] = {}
            chyby[channelName]['HLS']['KALT'] = 'ERROR'

            #print("CSV row: " + str(poc))   
            DASH_kalt_reason = False
        finally:
            #partnerID, channel#, name, date, codec, stage ,Relapsed, BEelapsed, exit_msg, payload
            #---------------------------------------------------------
            # zapsat do DB
            now =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sentense = partnerID+","+channelNumber+","+channelName+","+now+",HLS,KALT,"+str(elapsed)+","+str(executionTime)+","+exit_msg+","+payl+"\n"
            f = open('output.csv', "a")
            f.write(sentense)
            f.close()
        

        # get URL - manifest  DASH, BRPK
        response = ""
        if DASH_kalt_reason:
            print("--> CONTINUE TEST FOR HLS -- STAGE BRPR")
            logging.info("--> CONTINUE TEST FOR HLS -- STAGE BRPR")
            response = requests.get(url, headers=header)
            url = ""
            get_responsecode = response.status_code
            if get_responsecode == 200:
                print("Response reason: "+str(response.reason))
                print("Response status code: "+str(response.status_code))
                print("Elapsed time: "+str(response.elapsed.microseconds/1000000))
                e1 = response.elapsed.microseconds/1000000
                e2 = elapsed
                JointE = round(e1 + e2, 6)
                print("Joint elapsed time: "+str(JointE))
                logging.info("[RESULT][BRPK][HLS]["+channelName+"]["+channelNumber+"]Response reason: "+str(response.reason))
                logging.info("[RESULT][BRPK][HLS]["+channelName+"]["+channelNumber+"]Response status code: "+str(response.status_code))
                logging.info("[RESULT][BRPK][HLS]["+channelName+"]["+channelNumber+"]Elapsed time: "+str(response.elapsed.microseconds/1000000))
                logging.info("[RESULT][BRPK][HLS]["+channelName+"]["+channelNumber+"]Joint elapsed time: "+str(JointE)) 

                exit_msg = "OK: --BRPK returned Manifest" 
                payl = "Reason: "+str(response.reason)+" Status code: "+str(get_responsecode)
                e1 = e1 
            else:
                print("Response reason: "+str(response.reason))
                print("Response status code: "+str(response.status_code))
                print("Elapsed time: "+str(response.elapsed.microseconds/1000000))
                e1 = response.elapsed.microseconds/1000000
                e2 = elapsed
                JointE = round(e1 + e2, 6)
                print("Joint elapsed time: "+str(JointE))
                logging.error("[RESULT][BRPK][DASH]["+channelName+"]["+channelNumber+"]Response reason: "+str(response.reason))
                logging.error("[RESULT][BRPK][DASH]["+channelName+"]["+channelNumber+"]Response status code: "+str(response.status_code))
                logging.error("[RESULT][BRPK][DASH]["+channelName+"]["+channelNumber+"]Elapsed time: "+str(response.elapsed.microseconds/1000000))
                logging.error("[RESULT][BRPK][DASH]["+channelName+"]["+channelNumber+"]Joint elapsed time: "+str(JointE)) 

                exit_msg = "ERROR: --BRPK not get Manifest. (wrong URL?)"
                payl = payl = "Reason: "+str(response.reason)+" Status code: "+str(get_responsecode)
                e1 = e1

                if channelName not in chyby:
                    chyby[channelName] = {}
                if 'HLS' not in chyby[channelName]:
                    chyby[channelName]['HLS'] = {}
                chyby[channelName]['HLS']['BRPK'] = 'ERROR'          

                DASH_brpk_reason = True
                data = ""
                url = ""
                response = ""
        else:
            print(("BRPK REASON ERROR: --KALT not returned any URL"))
            logging.warn("[RESULT][BRPK][HLS]["+channelName+"]["+channelNumber+"]ERROR: --KALT not returned any URL")
            logging.warn("[RESULT][BRPK][HLS]["+channelName+"]["+channelNumber+"]ERROR: Response status code: NONE")
            logging.warn("[RESULT][BRPK][HLS]["+channelName+"]["+channelNumber+"]ERROR: Elapsed time: NONE")

            if channelName not in chyby:
                chyby[channelName] = {}
            if 'HLS' not in chyby[channelName]:
                chyby[channelName]['HLS'] = {}
            chyby[channelName]['HLS']['BRPK'] = 'ERROR'

            exit_msg = "ERROR: --KALT not returned any URL"
            payl = ""
            e1 = ""

            DASH_brpk_reason = False
            data = ""
            url = ""
            response = ""

        #partnerID, channel#, name, date, codec, stage ,Relapsed, BEelapsed, exit_msg, payload
        #---------------------------------------------------------
        # zapsat do DB
        now =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sentense = partnerID+","+channelNumber+","+channelName+","+now+",HLS,BRPK,"+str(e1)+",NaN,"+exit_msg+","+payl+"\n"
        f = open('output.csv', "a")
        f.write(sentense)
        f.close()

        url = ""
        HLS_brpk_reason = False
        data = ""
        url = ""
        response = ""

    
    #print(chyby)
    print(json.dumps(chyby, indent=4))
    

