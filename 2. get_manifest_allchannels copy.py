
import csv
import datetime
from KALT_config import *
import logging
import logging.handlers as handlers

#logovani a rotovani logu
logger = logging.getLogger('my_app')
logger.setLevel(logging.INFO)
logHandler = handlers.RotatingFileHandler('app.log', maxBytes=30000500, backupCount=5)
logHandler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)-0s %(levelname)-0s %(message)s")
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

#specificke promenne pro test
partnerID = '3200'
inputfile = "opc_tlrs.csv"

#ziskani credentials a API hlavicek, phoenixURL
credentials = user_login(partnerID, 3)
head = headers(partnerID)
headerPOST = head[0]
phoenixURL = head[2]

#ziskani user ks
ks = KALT_ks(apiVersion, partnerID, credentials[0], credentials[1], credentials[2], phoenixURL, headerPOST)
if ks == 'ERROR':
    logger.info("No login ks returned")
else:
    logger.info("[LOGIN]BE execution Time: "+str(ks[2]))
    logger.info("[LOGIN]Elapsed Time: "+str(ks[1]))
    logger.info("[LOGIN]User KS: " + ks[0])



