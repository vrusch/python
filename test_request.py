import requests
import json
import logging
import http.client
import csv

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


partnerID = "3200" 
phoenixURL = "https://3200.frp1.ott.kaltura.com/api_v3/service/"
apiVersion = "5.4.0"
clientTag = "0.13.0-PC"
language = "eng"
udid = "monitoring4_rs" 
username = "monitoring4_rs" 
password = "#-K_monitoring4_rs" 
header = {'Content-Type' : 'application/json', 'Host ' : '3200.frp1.ott.kaltura.com', 'Accept' : '*/*', 'Accept-Encoding' : 'gzip, deflate, br', 'Connection' : 'keep-alive'} 

httpclient_logging_patch()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, filename="test.log", filemode="a+",
                        format="%(asctime)-0s %(levelname)-0s %(message)s")

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
#print(response.request.method)
#print(response.request.url)
#print(response.request.headers)
#print(response.request.body)
json_response = response.json()
login_ks = json_response['result']['loginSession']['ks']
#print(login_ks)

#getEPG data for one program
servis = "/asset/action/list"
data = {
    "language": language,
    "ks": login_ks,
    "filter": {
        "objectType": "KalturaSearchAssetFilter",
        "kSql": "(and linear_media_id:'817432' (or ( and end_date >= '1635285600' end_date  <= '1635371999') ( and start_date >= '1635285600' start_date  <= '1635371999')) asset_type='epg' auto_fill= true)",
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
#print(response.request.method)
#print(response.request.url)
#print(response.request.headers)
#print(response.request.body)
json_response = response.json()
executionTime = json_response['executionTime']
totalCount = json_response['result']['totalCount']
print("---------------------------")
print(executionTime)
print(totalCount)

#get HOME PAGE content
servis = "/asset/action/list"
data = {
    "language": language,
    "ks": login_ks,
    "filter": {
        "objectType": "KalturaSearchAssetFilter",
        "kSql": "(and (or CategoryId = '56864' CategoryId = '56719' CategoryId = '56718' CategoryId = '56711' CategoryId = '56712' CategoryId = '56713' CategoryId = '56714' CategoryId = '56715' CategoryId = '56716' CategoryId = '56717' CategoryId = '56726' CategoryId = '56720' CategoryId = '56721' CategoryId = '56722' CategoryId = '56723' CategoryId = '56724' CategoryId = '56725' CategoryId = '56727' CategoryId = '56734' CategoryId = '56728' CategoryId = '56729' CategoryId = '56730' CategoryId = '56731' CategoryId = '56732' CategoryId = '56733' CategoryId = '56744' CategoryId = '56735' CategoryId = '56736' CategoryId = '56737' CategoryId = '56738' CategoryId = '56739' CategoryId = '56740' CategoryId = '56741' CategoryId = '56743' CategoryId = '56746' CategoryId = '56745' CategoryId = '56747' CategoryId = '56768' CategoryId = '56757' CategoryId = '56754' CategoryId = '56753' CategoryId = '56748' CategoryId = '56749' CategoryId = '56750' CategoryId = '56751' CategoryId = '56752' CategoryId = '56755' CategoryId = '56756' CategoryId = '56758' CategoryId = '56759' CategoryId = '56760' CategoryId = '56761' CategoryId = '56762' CategoryId = '56763' CategoryId = '56764' CategoryId = '56765' CategoryId = '56766' CategoryId = '56767' CategoryId = '56775' CategoryId = '56769' CategoryId = '56770' CategoryId = '56771' CategoryId = '56772' CategoryId = '56773' CategoryId = '56774' CategoryId = '56784' CategoryId = '56783' CategoryId = '56776' CategoryId = '56777' CategoryId = '56778' CategoryId = '56779' CategoryId = '56780' CategoryId = '56781' CategoryId = '56782' CategoryId = '56792' CategoryId = '56785' CategoryId = '56786' CategoryId = '56787' CategoryId = '56788' CategoryId = '56789' CategoryId = '56790' CategoryId = '56791' CategoryId = '56799' CategoryId = '56793' CategoryId = '56794' CategoryId = '56795' CategoryId = '56796' CategoryId = '56797' CategoryId = '56798' CategoryId = '56807' CategoryId = '56800' CategoryId = '56801' CategoryId = '56802' CategoryId = '56803' CategoryId = '56804' CategoryId = '56805' CategoryId = '56806' CategoryId = '56814' CategoryId = '56808' CategoryId = '56809' CategoryId = '56810' CategoryId = '56811' CategoryId = '56812' CategoryId = '56813' CategoryId = '56822' CategoryId = '56815' CategoryId = '56816' CategoryId = '56817' CategoryId = '56818' CategoryId = '56819' CategoryId = '56820' CategoryId = '56821' CategoryId = '56828' CategoryId = '56823' CategoryId = '56824' CategoryId = '56825' CategoryId = '56826' CategoryId = '56827' CategoryId = '56832' CategoryId = '56829' CategoryId = '56830' CategoryId = '56831' CategoryId = '56837' CategoryId = '56833' CategoryId = '56834' CategoryId = '56835' CategoryId = '56836' CategoryId = '56844' CategoryId = '56838' CategoryId = '56839' CategoryId = '56840' CategoryId = '56841' CategoryId = '56842' CategoryId = '56843' CategoryId = '56850' CategoryId = '56845' CategoryId = '56846' CategoryId = '56847' CategoryId = '56848' CategoryId = '56849' CategoryId = '56858' CategoryId = '56851' CategoryId = '56852' CategoryId = '56853' CategoryId = '56854' CategoryId = '56855' CategoryId = '56856' CategoryId = '56857' CategoryId = '56863' CategoryId = '56859' CategoryId = '56860' CategoryId = '56861' CategoryId = '56862' )(or ))"
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
#print(response.request.method)
#print(response.request.url)
#print(response.request.headers)
#print(response.request.body)
json_response = response.json()
executionTime = json_response['executionTime']
totalCount = json_response['result']['totalCount']
print("---------------------------")
print(executionTime)
print(totalCount)