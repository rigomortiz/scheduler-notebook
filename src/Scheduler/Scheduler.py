import os
import nbformat
from nbclient.exceptions import CellExecutionError
from nbconvert.preprocessors import ExecutePreprocessor
from datetime import datetime

from src.Scheduler.Constants import ENV_FILE, NOTEBOOKS_KEY, AS_VERSION, KERNEL_NAME_KEY, TIMEOUT, \
    FORMAT_DATE, EXTENSION, PARAMS_KEY, CONFIG_FILE, REPEAT_BY_KEY, OUTPUT_PATH, INPUT_PATH
from src.Scheduler.Utils import Utils


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

    def run(self):
        print('Open file: ' + self.path)
        with open(self.path) as f:
            nb = nbformat.read(f, as_version=AS_VERSION)
            print('Notebook: ' + self.name + ' version: ' + str(AS_VERSION) + ' running with kernel: '
                  + self.kernel_name)
            print('Running cells...')
            ep = ExecutePreprocessor(timeout=TIMEOUT, kernel_name=self.kernel_name)
            now = datetime.now()
            current_time = now.strftime(FORMAT_DATE)
            filename_out = self.name.replace(EXTENSION, '_' + current_time + '_out' + EXTENSION)
            try:
                out = ep.preprocess(nb)
                print(out)
            except CellExecutionError:
                out = None
                msg = 'Error executing the notebook \'%s\'.\n\n' % self.name
                msg += 'See notebook \'%s\' for the traceback.' % filename_out
                print(msg)
                raise
            finally:
                try:
                    os.mkdir(OUTPUT_PATH)
                except OSError as error:
                    print(error)
                with open(OUTPUT_PATH + os.sep + filename_out, mode='w', encoding='utf-8') as fnb:
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
            for i in range(0, self.time):
                args_repeat = self.config[PARAMS_KEY]
                args_repeat[key_repeat] = ",".join(str(x) for x in self.config[REPEAT_BY_KEY][key_repeat][:i + 1])
                for n in range(0, len(self.config[NOTEBOOKS_KEY])):
                    notebook = self.config[NOTEBOOKS_KEY][n]
                    self.notebooks.append(Notebook(n + 1, os.path.basename(notebook), notebook, {**args_repeat},
                                          self.config[KERNEL_NAME_KEY]))
        else:
            self.time = 1
            for notebook in self.config[NOTEBOOKS_KEY]:
                self.notebooks.append(Notebook(1, os.path.basename(notebook), notebook, self.config[PARAMS_KEY],
                                               self.config[KERNEL_NAME_KEY]))

        print('Repeat time: ' + str(self.time))
        print("Notebooks: ")
        for notebook in self.notebooks:
            print(notebook)

    def get_notebooks(self):
        return self.notebooks

    def write_params_to_notebook(self, params):
        with open(INPUT_PATH + os.sep + ENV_FILE, 'w') as file:
            print('Writing params to file')
            for param in params:
                file.write(param + '\n')

    def run(self):
        print('Running notebooks...')
        self.__run_notebooks()
        print('Done')

    def __run_notebooks(self):
        for notebook in self.notebooks:
            Utils.set_env(notebook.params)
            print('Running notebook number: ' + str(notebook.num) + ' of ' + str(self.time))
            print('Running notebook: ' + notebook.name)
            print('Params: ' + str(notebook.params))
            notebook.run()
