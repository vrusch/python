import requests
import hashlib

partnerID = "3200" # partnerID = [("TLRS", "3200"), ("O2CZ", "3201"), ("TLHU", "3204"), ("O2SK", "3206")]
apiVersion = "5.3.5"


if partnerID == "3200":
        bu = 'TLRS'
        token_id = "0a2c8d706c694cb199057f8e9b704e7c"
        token = "78ec49d3f1924ed8a63575db1c8cde9d"
elif partnerID == "3201":
        bu = 'O2CZ'
        token_id = "none"
        token = "none"
elif partnerID == "3204":
        bu = 'TLHU'
        token_id = "c2759f4f10494c428399ee36f27650d6"
        token = "ef39b6258189408db31dbab1477740cb"
elif partnerID == "3206":
        bu = 'O2SK'
        token_id = "aed7d414b5cb4638ac74d61d9adf1eab"
        token = "cd89a01cab1d466185fd225d8e901dcb"


phoenixURL = "https://"+partnerID+".frp1.ott.kaltura.com/api_v3/service/"

servis = "OTTUser/action/anonymousLogin"
send = phoenixURL + servis
data = {   
	"apiVersion": apiVersion,
	"partnerId": partnerID
}
response = requests.post(send, data)

json_response = response.json()
ks = json_response['result']['ks']

servis = "appToken/action/startSession"
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
print('')
print ('BSS KS for '+bu+': \n'+BSS_ks)