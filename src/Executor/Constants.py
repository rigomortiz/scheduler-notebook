import os

KERNEL_NAME = 'kernel_name'
PARAMS = 'params'
PATHS = 'paths'
NOTEBOOKS = 'notebooks'
NAME = 'name'
TYPE = 'type'
VALUE = 'value'
CONSTANT = 'constant'
REPEAT = 'repeat'
ACCUMULATED = 'accumulated'

UTF_8 = 'utf-8'
INPUT_PATH = './input'
OUTPUT_PATH = './output'
ENV_PATH = OUTPUT_PATH + os.path.sep + 'env'
TMP_PATH = OUTPUT_PATH + os.path.sep + 'tmp'
TMP_TEST_PY = TMP_PATH + os.path.sep + 'test.py'
NOTEBOOKS_PATH = OUTPUT_PATH + os.path.sep + 'notebooks'
TESTS_PATH = OUTPUT_PATH + os.path.sep + 'tests'
CSV_PATH = OUTPUT_PATH + os.path.sep + 'csv'
FORMAT_DATE = '%Y-%m-%d_%H-%M-%S'
NOTEBOOK_EXTENSION = '.ipynb'
CONFIG_FILE = './config.json'
ENV_FILE = '.env'
LOG_FILE_NAME = 'logs/log'
LOG_FILE_EXTENSION = '.log'
TIMEOUT = -1
STARTUP_TIMEOUT = 5000
AS_VERSION = 4
MODE = 'w'
