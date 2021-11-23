import os, sys
from daemonize import Daemonize
import schedule
import time



def main():
      # your code here
      def func():
            print('Alive..')

      schedule.every(1).minutes.do(func)
  
      while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == '__main__':
      myname=os.path.basename(sys.argv[0])
      pidfile='/tmp/%s' % myname       # any name
      daemon = Daemonize(app=myname,pid=pidfile, action=main)
      daemon.start()