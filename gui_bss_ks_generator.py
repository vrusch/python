import tkinter as tk
from tkinter import ttk
from tkinter.constants import END
import requests
import hashlib
import pyperclip

root = tk.Tk()
root.geometry('300x350')
root.resizable(False, False)
root.title('BSS ks generator')


def op_changed(event):
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
    kstext.insert(END, BSS_ks)
    pyperclip.copy(BSS_ks)


# operator
op = ('TLRS', 'TLHU', 'O2CZ', 'O2SK')

label = ttk.Label(text="Please select a operator:")
label.pack(fill='x', padx=5, pady=5)

# create a combobox
selected_op = tk.StringVar()

op_cb = ttk.Combobox(root, textvariable=selected_op)
op_cb['values'] = op
op_cb['state'] = 'readonly'  # normal
op_cb.pack(fill='x', padx=5, pady=5)

op_cb.bind('<<ComboboxSelected>>', op_changed)

kstext = tk.Text(root)
kstext.pack(fill='x', padx=5, pady=5)

root.mainloop()