import requests
import json
import datetime


partnerID = "3201" # partnerID = [("TLRS", "3200"), ("O2CZ", "3201"), ("TLHU", "3204"), ("O2SK", "3206")]
phoenixURL = "https://" + partnerID + ".frp1.ott.kaltura.com/api_v3/service/"
apiVersion = "5.4.0"

if partnerID == "3200":
    username = "monitoring3_rs" 
    password = "#-K_monitoring3_rs" 
    udid = "monitoring3_rs"
    header = {'Content-Type' : 'application/json', 'Host ' : '3200.frp1.ott.kaltura.com', 'Accept' : '*/*',
     'Accept-Encoding' : 'gzip, deflate, br', 'Connection' : 'keep-alive'} 
    idEqual = 354085
    makelogfile = "makelog_tlrs.log"
    csvfile = "opc_tlrs.csv"
    asset_type = 601
elif partnerID == "3201":
    username = "monitoring3_cz" 
    password = "#-K_monitoring3_cz" 
    udid = "monitoring3_cz" 
    header = {'Content-Type' : 'application/json', 'Host ' : '3201.frp1.ott.kaltura.com', 'Accept' : '*/*',
     'Accept-Encoding' : 'gzip, deflate, br', 'Connection' : 'keep-alive'} 
    idEqual = 354336
    makelogfile = "makelog_o2cz.log"
    csvfile = "opc_o2cz.csv"
    asset_type = 607


def sendRequest (servis, data):
    send = phoenixURL + servis
    response = requests.post(send, json.dumps(data), headers=header)
    json_response = response.json()
    return json_response

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
json_response = json.dumps(login_ks, indent=4)
#print(json_response)
#login_ks = login_ks['result']['loginSession']['ks']
print(login_ks)
#print(login_ks['result']['loginSession']['expiry'])

epoch_time = (login_ks['result']['loginSession']['expiry'])
the_datetime = datetime. datetime. fromtimestamp( epoch_time )
print( "EXPIRATION:", the_datetime )
