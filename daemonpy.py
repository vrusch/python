import os, sys
from daemonize import Daemonize
import schedule
import time
import logging

#logging
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, filename="./log/test.log", filemode="a+",
                        format="%(asctime)-1s %(levelname)-0.5s %(message)s")
logging.info("hello")

def main():
      # your code here
      def func():
            logging.info("hello")

      schedule.every(10).seconds.do(func)
  
      while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == '__main__':
      myname=os.path.basename(sys.argv[0])
      pidfile='/tmp/%s' % myname       # any name
      daemon = Daemonize(app=myname,pid=pidfile, action=main)
      daemon.start()