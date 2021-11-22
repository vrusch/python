
import requests
import json




apiVersion = "5.4.0"
clientTag = "0.13.0-PC"
language = "eng"
udid = "monitoring3_rs" 
username = "monitoring3_rs" 
password = "#-K_monitoring3_rs"
partnerID = "3200"
phoenixURL = "https://" + partnerID + ".frp1.ott.kaltura.com/api_v3/service/"
headerPOST = {'Content-Type' : 'application/json', 'Host ' : '3200.frp1.ott.kaltura.com', 'Accept' : '*/*', 'Accept-Encoding' : 'gzip, deflate, br', 'Connection' : 'keep-alive'} 
headerGET = {'Host ' : '3200.frp1.ott.kaltura.com', 'Accept' : '*/*', 'Accept-Encoding' : 'gzip, deflate, br', 'Connection' : 'keep-alive'} 


servis = "OTTUser/action/login"
data = {   
            "apiVersion": apiVersion,
            "partnerId": partnerID,
            "username": username,
            "password": password,
            "udid": udid,
        }
send = phoenixURL + servis
response = requests.post(send, json.dumps(data), headers=headerPOST)
json_response = response.json()
login_ks = json_response['result']['loginSession']['ks']
Relapsed = (response.elapsed.microseconds)/1000000
BEexecutionTime = json_response['executionTime']
epoch = json_response['result']['loginSession']['expiry']


servis = "/asset/action/list"
data = {
        "clientTag": "KUX",
        "language": "srp",
        "apiVersion": apiVersion,
        "ks": login_ks,
        "filter": {
            "objectType": "KalturaChannelFilter",
            "kSql": "(and (and asset_type=601))",
            "idEqual": 354085
            },
        "pager": {
        "objectType": "KalturaFilterPager",
        "pageSize": 200,
        "pageIndex": 1
         }
        }
send = phoenixURL + servis
response = requests.post(send, json.dumps(data), headers=headerPOST)
responsejson = response.json()
print(responsejson)
