import logging
import requests
import json
import datetime
import time

from requests.models import HTTPError

apiVersion = "5.4.0"
clientTag = "0.13.0-PC"
language = "eng"


def user_login(partnerID, user):
    if partnerID == "3200":
        if user == 1:
            udid = "monitoring1_rs" 
            username = "monitoring1_rs" 
            password = "#-K_monitoring1_rs" 
        elif user == 2:
            udid = "monitoring2_rs" 
            username = "monitoring2_rs" 
            password = "#-K_monitoring2_rs"
        elif user == 3:
            udid = "monitoring3_rs" 
            username = "monitoring3_rs" 
            password = "#-K_monitoring3_rs"
        elif user == 4:
            udid = "monitoring4_rs" 
            username = "monitoring4_rs" 
            password = "#-K_monitoring4_rs"
        else:
            udid = "none" 
            username = "none" 
            password = "none" 

    elif partnerID == "3201":
        if user == 1:
            udid = "monitoring1_cz" 
            username = "monitoring1_cz@cetin.cz" 
            password = "#-K_monitoring1_cz"
        elif user == 2:
            udid = "monitoring2_cz" 
            username = "monitoring2_cz@cetin.cz" 
            password = "#-K_monitoring2_cz" 
        elif user == 3:
            udid = "monitoring3_cz" 
            username = "monitoring3_cz@cetin.cz" 
            password = "#-K_monitoring3_cz" 
        elif user == 4:
            udid = "monitoring4_cz" 
            username = "monitoring4_cz@cetin.cz" 
            password = "#-K_monitoring4_cz"
        else:
            udid = "none" 
            username = "none" 
            password = "none"
        
    elif partnerID == "3204":
        if user == 1:
            udid = "monitoring1_hu" 
            username = "monitoring1_hu" 
            password = "#-K_monitoring1_rs" 
        elif user == 2:
            udid = "monitoring2_rs" 
            username = "monitoring2_hu" 
            password = "#-K_monitoring2_hu"
        elif user == 3:
            udid = "monitoring3_hu" 
            username = "monitoring3_hu" 
            password = "#-K_monitoring3_hu"
        elif user == 4:
            udid = "monitoring4_hu" 
            username = "monitoring4_hu" 
            password = "#-K_monitoring4_hu"
        else:
            udid = "none" 
            username = "none" 
            password = "none"

    elif partnerID == "3206":
        if user == 1:
            udid = "monitoring1_sk" 
            username = "monitoring1_sk" 
            password = "#-K_monitoring1_sk" 
        elif user == 2:
            udid = "monitoring2_sk" 
            username = "monitoring2_sk" 
            password = "#-K_monitoring2_sk"
        elif user == 3:
            udid = "monitoring3_sk" 
            username = "monitoring3_sk" 
            password = "#-K_monitoring3_sk"
        elif user == 4:
            udid = "monitoring4_sk" 
            username = "monitoring4_sk" 
            password = "#-K_monitoring4_sk"
        else:
            udid = "none" 
            username = "none" 
            password = "none"
    
    return username, password, udid


def headers(partnerID):
    if partnerID == "3200":
        headerPOST = {'Content-Type' : 'application/json', 'Host ' : '3200.frp1.ott.kaltura.com', 'Accept' : '*/*', 'Accept-Encoding' : 'gzip, deflate, br', 'Connection' : 'keep-alive'} 
        headerGET = {'Host ' : '3200.frp1.ott.kaltura.com', 'Accept' : '*/*', 'Accept-Encoding' : 'gzip, deflate, br', 'Connection' : 'keep-alive'} 
    elif partnerID == "3201":
        headerPOST = {'Content-Type' : 'application/json', 'Host ' : '3201.frp1.ott.kaltura.com', 'Accept' : '*/*', 'Accept-Encoding' : 'gzip, deflate, br', 'Connection' : 'keep-alive'} 
        headerGET = {'Host ' : '3200.frp1.ott.kaltura.com', 'Accept' : '*/*', 'Accept-Encoding' : 'gzip, deflate, br', 'Connection' : 'keep-alive'}
    elif partnerID == "3204":
        headerPOST = {'Content-Type' : 'application/json', 'Host ' : '3201.frp1.ott.kaltura.com', 'Accept' : '*/*', 'Accept-Encoding' : 'gzip, deflate, br', 'Connection' : 'keep-alive'} 
        headerGET = {'Host ' : '3200.frp1.ott.kaltura.com', 'Accept' : '*/*', 'Accept-Encoding' : 'gzip, deflate, br', 'Connection' : 'keep-alive'}
    elif partnerID == "3206":
        headerPOST = {'Content-Type' : 'application/json', 'Host ' : '3201.frp1.ott.kaltura.com', 'Accept' : '*/*', 'Accept-Encoding' : 'gzip, deflate, br', 'Connection' : 'keep-alive'} 
        headerGET = {'Host ' : '3200.frp1.ott.kaltura.com', 'Accept' : '*/*', 'Accept-Encoding' : 'gzip, deflate, br', 'Connection' : 'keep-alive'}
    else:
        headerPOST = {} 
        headerGET = {}
    
    phoenixURL = "https://" + partnerID + ".frp1.ott.kaltura.com/api_v3/service/"

    return headerPOST, headerGET, phoenixURL

def KALT_ks(apiVersion, partnerID, username, password, udid, phoenixURL, header):
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
    try:
        login_ks = json_response['result']['loginSession']['ks']
        Relapsed = (response.elapsed.microseconds)/1000000
        BEexecutionTime = json_response['executionTime']
        epoch = json_response['result']['loginSession']['expiry']
        return login_ks, Relapsed, BEexecutionTime, epoch
    except:
        #doplnit telo error msg a vratit
        return 'ERROR'


def get_context(assetId, login_ks, header, phoenixURL):
    servis = "/asset/action/getPlaybackContext"
    dataDASH = {
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
    sendDASH = phoenixURL + servis
    dateS =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        responseDASH = requests.post(sendDASH, json.dumps(dataDASH), timeout= 7, headers=header)
        RelapsedDASH =  (responseDASH.elapsed.microseconds)/1000000
    except:
        responseDASH = None
        RelapsedDASH = None
        
    

    dataHLS = {
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
    sendHLS = phoenixURL + servis
    try:
        responseHLS = requests.post(sendHLS, json.dumps(dataHLS), timeout= 7, headers=header)
        RelapsedHLS =  (responseHLS.elapsed.microseconds)/1000000
    except:
        responseHLS = None
        RelapsedHLS = None
    
    return responseDASH, responseHLS, RelapsedDASH, RelapsedHLS, dateS
    