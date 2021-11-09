import logging
import logging.handlers as handlers




logger = logging.getLogger('my_app')
logger.setLevel(logging.INFO)
logHandler = handlers.RotatingFileHandler('app.log', maxBytes=500, backupCount=4)
logHandler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)-0s %(levelname)-0s %(message)s")
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)






for i in range(30):
    logger.info(str(i) +" [KALT][DASH] TRY SEND POST REQUEST: etPlaybackContext --with channelName +  + assetId")


