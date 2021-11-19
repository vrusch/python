
import requests
import json
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template




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


servis = "/asset/action/getPlaybackContext"
dataDASH = {
            "assetId": '800398',
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

response = ''
try:
    response = requests.post(sendDASH, json.dumps(dataDASH), timeout= 2, headers=headerPOST)
    responseDASH = response.json()
    print(responseDASH)
    RelapsedDASH =  (responseDASH.elapsed.microseconds)/1000000
except:
    print('exe')

help(dcc.Dropdown)
