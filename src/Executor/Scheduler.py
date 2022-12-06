import logging
import sys

import pytest

from src.Executor.Utils import Utils
from src.Executor.Constants import *
from src.Executor.Notebook import Notebook


class Scheduler:
    """
    Constructor
    """
    def __init__(self, config_file: str = CONFIG_FILE):
        """
        :param config_file: path to config file
        """
        self.notebooks = []
        self.time = 1
        self.config = Utils.read_config_file(config_file)
        if self.config is None:
            raise Exception('Exception: Config file not found')
        if NOTEBOOKS not in self.config:
            raise Exception('Exception: Not found notebooks key')

        self.__initializer_notebooks()

        logging.info('Output path: %s', OUTPUT_PATH)

        logging.info('Repeat time: %s', str(self.time))
        logging.info("Notebooks: ")
        for notebook in self.notebooks:
            logging.info(notebook)

    def __initializer_notebooks(self) -> None:
        logging.debug('Initializer notebooks ...')
        if type(self.config[NOTEBOOKS]).__name__ not in ('list', 'tuple'):
            raise Exception('\'Notebooks\' key not is an array')

        for notebook in self.config[NOTEBOOKS]:
            if KERNEL_NAME not in notebook:
                raise Exception('\'Kernel name\' key not found')
            if PATHS not in notebook:
                raise Exception('\'Paths\' key not found')
            if PARAMS in notebook:
                consts_params = list(filter(lambda param: TYPE not in param or VALUE not in param or NAME not in param,
                                            notebook[PARAMS]))
                if len(consts_params) > 0:
                    raise Exception('\'name\', \'value\' or \'type\' key not found in params')
                consts_params = list(filter(lambda param: (param[TYPE] == CONSTANT), notebook[PARAMS]))
                accumulated_params = list(filter(lambda param: (param[TYPE] == ACCUMULATED), notebook[PARAMS]))
                # repeat_params = list(filter(lambda p: (p[TYPE] == REPEAT), notebook[PARAMS]))
                if len(accumulated_params) > 1:
                    raise Exception('Only one accumulated param is allowed')
                self.time = len(accumulated_params[0][VALUE])
                if self.time > 0:
                    for i in range(self.time):
                        param = {
                            NAME: accumulated_params[0][NAME],
                            VALUE: ','.join(str(x) for x in accumulated_params[0][VALUE][:i + 1]),
                            TYPE: accumulated_params[0][TYPE]
                        }
                        for p in range(len(notebook[PATHS])):
                            params = consts_params.copy()
                            params.append(param)
                            print(params)
                            nb = Notebook(path=notebook[PATHS][p], params=params, kernel_name=notebook[KERNEL_NAME])
                            self.notebooks.append(nb)
                else:
                    pass

    def get_notebooks(self) -> list[Notebook]:
        return self.notebooks

    def run(self) -> None:
        logging.info('Running notebooks...')
        self.__run_notebooks()
        logging.info('Done')

    def __run_notebooks(self) -> None:

        for i in range(len(self.notebooks)):
            Utils.set_env(self.notebooks[i].params)
            logging.info('Running notebook number: %s of %s', str(i + 1), str(self.time))
            logging.info('Running notebook: %s', self.notebooks[i].path)
            logging.info('Params: %s', str(self.notebooks[i].params))
            self.notebooks[i].run()

    def __test(self):
        pass
        # test_file = 'output/tests/' + os.path.basename(self.notebooks[i].path_test.replace(NOTEBOOK_EXTENSION, '.py'))
        # logging.info('Run file test: %s', test_file)
        # pytest.main(["-v", test_file])