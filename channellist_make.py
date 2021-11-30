import requests
import json
import logging
import os


partnerID = "3201" # partnerID = [("TLRS", "3200"), ("O2CZ", "3201"), ("TLHU", "3204"), ("O2SK", "3206")]
phoenixURL = "https://" + partnerID + ".frp1.ott.kaltura.com/api_v3/service/"
apiVersion = "5.4.0"

if partnerID == "3200":
    header = {'Content-Type' : 'application/json', 'Host ' : '3200.frp1.ott.kaltura.com', 'Accept' : '*/*', 
            'Accept-Encoding' : 'gzip, deflate, br', 'Connection' : 'keep-alive'}
    udid = "monitoring4_rs" 
    username = "monitoring4_rs" 
    password = "#-K_monitoring4_rs" 
    idEqual = 354085
    assettype = 601
    outputcsv = "opc_tlrs.csv"
    log="./log/makeTLRS_channel_list.log"
elif partnerID == "3201":
    header = {'Content-Type' : 'application/json', 'Host ' : '3201.frp1.ott.kaltura.com', 'Accept' : '*/*', 
            'Accept-Encoding' : 'gzip, deflate, br', 'Connection' : 'keep-alive'}
    udid = "monitoring2_cz" 
    username = "monitoring2_cz@cetin.cz" 
    password = "#-K_monitoring2_cz" 
    idEqual = 354336
    assettype = 607
    outputcsv = "opc_o2cz.csv"
    log="./log/makeO2cz_channel_list.log"


#send request function
def sendRequest (servis, data):
    send = phoenixURL + servis
    response = requests.post(send, json.dumps(data), headers=header)
    logging.info(response.elapsed)
    logging.info(response.headers)
    logging.info(response.encoding)
    logging.info(response.reason)
    json_response = response.json()
    return json_response


#logging
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, filename=log, filemode="a+",
                        format="%(asctime)-1s %(levelname)-0.5s %(message)s")
logging.info("hello")

if os.path.exists(outputcsv):
  os.remove(outputcsv)
  logging.info("The output file exist removed!")
else:
  logging.info("The output file does not exist")


#login ks
servis = "OTTUser/action/login"
data = {   
	    "apiVersion": apiVersion,
        "partnerId": partnerID,
        "username": username,
        "password": password,
        "udid": udid,
    }
login_ks = sendRequest(servis,data)
login_ks = login_ks['result']['loginSession']['ks']
logging.info("LOGIN KS: " +login_ks)
#print(login_ks)



#get all channels
servis = "/asset/action/list"
data = {
        "clientTag": "KUX",
        "language": "srp",
        "apiVersion": apiVersion,
        "ks": login_ks,
        "filter": {
            "objectType": "KalturaChannelFilter",
            "kSql": "(and (and asset_type="+str(assettype)+"))",
            "idEqual": idEqual
            },
        "pager": {
        "objectType": "KalturaFilterPager",
        "pageSize": 200,
        "pageIndex": 1
         }
        }
all_channels = sendRequest(servis,data)
#print (json.dumps(all_channels, indent=4))
total_count = all_channels['result']['totalCount']
try:
    channels = all_channels['result']['objects']
    poc = 0
    poc_n = 0
    chan_w_noNumber = []
except:
    print(json.dumps(all_channels, indent=4))
    
    

#vyloucit kanaly ktere maji v mene
vyloucit_ch = ("Cetin", "blabla")
vyloucit_poc = 0
chan_out = []

if total_count > 0:
#print (json.dumps(channels, indent=4))
    for channel in channels:
        print("=======================") 
        channel_name = (channel['name'])
        logging.info("")
        logging.info("===================================================")
        logging.info("puvodni jmeno: " +channel_name)
        channel_name = str(channel_name)
        channel_name = channel_name.replace(":", "")
        channel_name = channel_name.replace(".", "")
        channel_name = channel_name.replace("š", "s")
        channel_name = channel_name.replace("Ž", "Z")
        channel_name = channel_name.replace("!", "1")
        channel_name = channel_name.replace("Č", "C")
        channel_name = channel_name.replace("č", "c")
        channel_name = channel_name.replace("Ó", "O")
        channel_name = channel_name.replace("+", "_")
        channel_name = channel_name.replace("ň", "n")
        channel_name = channel_name.replace("Š", "S")
        channel_name = channel_name.replace("á", "a")
        channel_name = channel_name.replace("ž", "z")
        channel_name = ''.join(channel_name.split())
        print(channel_name)
        logging.info("upravene jmeno: " +channel_name)
        channel_id = (channel['id'])
        print(channel_id)
        logging.info("channel ID: " +str(channel_id))
        channel_metas = channel['metas']
        if 'ChannelNumber' in channel_metas:
            channel_number = (channel['metas']['ChannelNumber']['value'])
            channel_number = str(channel_number)
            logging.info("puvodni channel #: " +channel_number)
            if len(channel_number) < 3:
                channel_number = "0" + channel_number
            if len(channel_number) < 3:
                channel_number = "0" + channel_number
            print(channel_number)
            logging.info("upravene channel #: " +channel_number)
            channel_mediafiles = channel['mediaFiles']
            print(len(channel_mediafiles))
            logging.info("channel #: " +channel_number + " " + channel_name +" have "+str(len(channel_mediafiles))+" media files: ")
            for media_file in channel_mediafiles:
                print("--> " +media_file['type'])
                print("-- with URL: " +media_file['url'])
                logging.info("--> " +media_file['type'])
                logging.info("-- with URL: " +media_file['url'])

            if any(x in channel_name for x in vyloucit_ch):
                vyloucit_poc = vyloucit_poc +1 
                chan_out.append((channel_name,channel_number))
                logging.error("channel #: " +channel_number + " " + channel_name +" byl vyhozeny protoze je v mnozine nezadoucich")
            elif channel['status'] == False :
                vyloucit_poc = vyloucit_poc +1 
                chan_out.append((channel_name,channel_number))
                logging.error("channel #: " +channel_number + " " + channel_name +" byl vyhozeny protoze status je FALSE")
            else:
                sentense = channel_name + ";" + str(channel_id) + ";" + str(channel_number) + "\n"
                poc = poc + 1
                f = open(outputcsv, "a")
                f.write(sentense)
                f.close()
                logging.info("channel #: " +channel_number + " " + channel_name +" status: " + str(channel['status']))
                logging.info("channel #: " +channel_number + " " + channel_name +" byl zapsan do csv")
        else:
            print("NONE")
            poc_n = poc_n + 1
            chan_w_noNumber.append({channel_name,channel_number})
            logging.error("channel #: " +channel_number + " " + channel_name +" byl vyhozeny protoze nema cislo kanalu")
        

    print("-----------------------------------------")
    print("Celkovy pocet stahnutych kanalu: "+str(total_count))
    print("Celkovy pocet zapsanych kanalu: "+str(poc))
    print("Pocet kanalu bez cisla: "+str(poc_n))
    print(chan_w_noNumber)
    print("Vyloucenych kanalu: "+str(vyloucit_poc))
    print(chan_out)
    logging.info("-----------------------------------------")
    logging.info("Celkovy pocet stahnutych kanalu: "+str(total_count))
    logging.info("Celkovy pocet zapsanych kanalu: "+str(poc))
    logging.info("Pocet kanalu bez cisla: "+str(poc_n))
    logging.info(chan_w_noNumber)
    logging.info("Vyloucenych kanalu: "+str(vyloucit_poc))
    logging.info(chan_out)


else:
    print("-----------------------------------------")
    print("Celkovy pocet stahnutych kanalu: "+str(total_count))

    
    
    
    

