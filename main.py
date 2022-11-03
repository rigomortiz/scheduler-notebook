import json
import os
import logging
import sys
from datetime import datetime

from src import Scheduler, FORMAT_DATE, LOG_FILE_EXTENSION, LOG_FILE_NAME, UTF_8

if __name__ == '__main__':
    now = datetime.now()
    current_time = now.strftime(FORMAT_DATE)
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s',
                        handlers=[
                            logging.FileHandler(LOG_FILE_NAME + '_' + current_time + LOG_FILE_EXTENSION),
                            logging.StreamHandler(sys.stdout)
                        ])
    logging.info(os.path.dirname(os.path.realpath(__file__)))
    scheduler = Scheduler(current_time)
    scheduler.run()
    #print("Params: ", json.dumps(params, indent=2))
