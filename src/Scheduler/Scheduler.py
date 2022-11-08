import os
from datetime import datetime
import nbformat
import logging
from nbclient.exceptions import CellExecutionError
from nbconvert.preprocessors import ExecutePreprocessor

from src.Scheduler.Utils import Utils
from src.Scheduler.Constants import ENV_FILE, NOTEBOOKS_KEY, AS_VERSION, KERNEL_NAME_KEY, TIMEOUT, \
    STARTUP_TIMEOUT, NOTEBOOK_EXTENSION, PARAMS_KEY, CONFIG_FILE, REPEAT_BY_KEY, OUTPUT_PATH, UTF_8, MODE, \
    FORMAT_DATE


class Notebook:

    def __init__(self, num, name, path, params, kernel_name):
        self.num = num
        self.name = name
        self.path = path
        self.params = params
        self.kernel_name = kernel_name
        # self.env = Utils.get_env()

    def __str__(self):
        return 'num=' + str(self.num) + ', name=' + self.name + ', path=' + self.path + ', params=' + str(self.params) \
               + ', kernel_name=' + self.kernel_name

    @staticmethod
    def get_cell_read_env():
        source = '''
import os

file = open('.env')
args = dict()
for line in file:
    key, value = line.split('=')
    args[key] = value.replace('\\n', '')
    os.environ[key] = value.replace('\\n', '')
                    '''
        return nbformat.v4.new_code_cell(source)

    @staticmethod
    def get_cell_write_env(name):
        source = '''
import os
import csv

with open('CSV_NAME', 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['VARIABLE', 'VALUE'])
    csvwriter.writerows([[x.replace('@', ''), os.environ[x]] for x in list(os.environ.copy().keys()) if x[0] == '@' and x[-1] == '@'])
                    '''.replace('CSV_NAME', name)
        return nbformat.v4.new_code_cell(source)

    def run(self):
        logging.info('Open file: %s', self.path)
        with open(self.path) as f:
            nb = nbformat.read(f, as_version=AS_VERSION)
            current_time = datetime.now().strftime(FORMAT_DATE)
            output_name = OUTPUT_PATH + os.path.sep + self.name.replace(NOTEBOOK_EXTENSION, '_' + current_time +
                                                                        NOTEBOOK_EXTENSION)
            logging.info('Notebook: %s version: %s running with kernel %s', output_name, str(AS_VERSION),
                         self.kernel_name)
            logging.info('Running cells...')

            # Add cell to read env variables file
            # nb.cells.insert(0, self.get_cell_read_env())
            # Add cell to save env variables
            nb.cells.append(self.get_cell_write_env(OUTPUT_PATH + os.path.sep + 'data_' + current_time + '.csv'))

            # => Executing notebook
            ep = ExecutePreprocessor(timeout=TIMEOUT, kernel_name=self.kernel_name, startup_timeout=STARTUP_TIMEOUT)
            try:
                out = ep.preprocess(nb, {})

                # logging.info('NOTEBOOK\n\n %s', out)
                logging.info('Notebook: %s executed successfully', output_name)
                logging.info('Saving notebook: %s', output_name)
            except CellExecutionError:
                out = None
                logging.error('Error executing the notebook \'%s\'.\n\n See notebook \'%s\' for the traceback.',
                              self.name, output_name)
                raise
            finally:
                with open(output_name, mode=MODE, encoding=UTF_8) as fnb:
                    nbformat.write(nb, fnb)


class Scheduler:
    def __init__(self, config_file=CONFIG_FILE, env_file=ENV_FILE):
        self.notebooks = []
        self.time = 1
        self.config = Utils.read_config_file(config_file)
        if self.config is None:
            raise Exception('Exception: Config file not found')

        self.params = self.config[PARAMS_KEY]
        # self.args = Utils.read_env_file(env_file)
        # if self.args is None:
        #     print('Warning: Env file not found')
        #     self.args = dict()
        #     if self.config[PARAMS_KEY] is not None:
        #         for param in self.config[PARAMS_KEY]:
        #             self.args[param] = self.config[PARAMS_KEY][param]
        #     else:
        #         print('Warning: Params not found')

        if self.config[REPEAT_BY_KEY] is not None and len(list(self.config[REPEAT_BY_KEY].keys())) == 1:
            key_repeat = list(self.config[REPEAT_BY_KEY].keys())[0]
            self.time = len(self.config[REPEAT_BY_KEY][key_repeat])
            num = 1
            for i in range(0, self.time):
                args_repeat = self.config[PARAMS_KEY]
                args_repeat[key_repeat] = ",".join(str(x) for x in self.config[REPEAT_BY_KEY][key_repeat][:i + 1])
                for n in range(0, len(self.config[NOTEBOOKS_KEY])):
                    notebook = self.config[NOTEBOOKS_KEY][n]
                    current_time = datetime.now().strftime(FORMAT_DATE)
                    self.notebooks.append(Notebook(num, os.path.basename(notebook), notebook, {**args_repeat},
                                          self.config[KERNEL_NAME_KEY]))
                    num += 1
        else:
            self.time = 1
            for notebook in self.config[NOTEBOOKS_KEY]:
                self.notebooks.append(Notebook(1, os.path.basename(notebook), notebook, self.config[PARAMS_KEY],
                                               self.config[KERNEL_NAME_KEY]))

        logging.info('Repeat time: %s', str(self.time))
        logging.info("Notebooks: ")
        for notebook in self.notebooks:
            logging.info(notebook)

        logging.info('Output path: %s', OUTPUT_PATH)
        if not os.path.exists(OUTPUT_PATH):
            os.makedirs(OUTPUT_PATH)

    def get_notebooks(self):
        return self.notebooks

    def run(self):
        logging.info('Running notebooks...')
        self.__run_notebooks()
        logging.info('Done')

    def __run_notebooks(self):
        for notebook in self.notebooks:
            Utils.set_env(notebook.params)
            logging.info('Running notebook number: %s of %s', str(notebook.num), str(self.time))
            logging.info('Running notebook: %s', notebook.name)
            logging.info('Params: %s', str(notebook.params))
            notebook.run()
