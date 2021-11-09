import requests
import hashlib


phoenixURL = "https://3200.frp1.ott.kaltura.com/api_v3/service/"
servis = "OTTUser/action/anonymousLogin"
apiVersion = "5.3.5"
partnerID = "3200"

send = phoenixURL + servis
data = {   
	"apiVersion": apiVersion,
	"partnerId": partnerID
}
response = requests.post(send, data)

json_response = response.json()
#print(response.status_code)
#print(response.headers)
#print(response.content)

ks = json_response['result']['ks']


servis = "appToken/action/startSession"
token_id = "0a2c8d706c694cb199057f8e9b704e7c"
token = "78ec49d3f1924ed8a63575db1c8cde9d"
send = phoenixURL + servis

string = ks + token #anonym + token
encoded = string.encode()
tokenHash = hashlib.sha256(encoded)
tokenHash = tokenHash.hexdigest()

data = {
        "apiVersion" :  apiVersion,
        "ks": ks,
        "id": token_id,
        "tokenHash": tokenHash
}

response2 = requests.post(send, data)
json_response2 = response2.json()
BSS_ks = json_response2['result']['ks']
print (BSS_ks)







