import os
import logging
import sys
from datetime import datetime

from src import Scheduler, LOG_FILE_EXTENSION, LOG_FILE_NAME, FORMAT_DATE


def log_config():
    if not os.path.exists('logs'):
        os.makedirs('logs')
    fh = logging.FileHandler(LOG_FILE_NAME + '_' + datetime.now().strftime(FORMAT_DATE) + LOG_FILE_EXTENSION)
    fh.setLevel(logging.INFO)
    sh = logging.StreamHandler(sys.stdout)
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s', handlers=[fh, sh])


if __name__ == '__main__':
    log_config()
    logging.info(os.path.dirname(os.path.realpath(__file__)))
    scheduler = Scheduler()
    scheduler.run()
