import os
import logging
import sys
from datetime import datetime

from src import Scheduler, LOG_FILE_EXTENSION, LOG_FILE_NAME, FORMAT_DATE


def log_config():
    if not os.path.exists('logs'):
        os.makedirs('logs')
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s',
                        handlers=[
                            logging.FileHandler(LOG_FILE_NAME + '_' + datetime.now().strftime(FORMAT_DATE) +
                                                LOG_FILE_EXTENSION),
                            logging.StreamHandler(sys.stdout)
                        ])


if __name__ == '__main__':
    log_config()
    logging.info(os.path.dirname(os.path.realpath(__file__)))
    scheduler = Scheduler()
    scheduler.run()
    #print("Params: ", json.dumps(params, indent=2))
