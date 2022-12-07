import logging

import nbformat
from nbclient.exceptions import CellExecutionError
from nbconvert.preprocessors import ExecutePreprocessor

from src.Executor.Utils import Utils
from src.Executor.Constants import *


class Notebook:

    def __init__(self, path: str, params: list, kernel_name: str, output_path: str):
        self.path = path
        self.params = params
        self.kernel_name = kernel_name
        self.path_test = ''
        self.output_path = output_path

    def __str__(self):
        return 'path=' + self.path + ', params=' + str(self.params) + ', kernel_name=' + self.kernel_name + \
            ', path_test=' + self.path_test + ', output_path=' + self.output_path

    def run(self) -> None:
        logging.info('Open file: %s', self.path)
        with open(self.path) as f:
            nb = nbformat.read(f, as_version=AS_VERSION)
            name = os.path.basename(self.path)
            self.path_test = self.output_path + os.path.sep + name.replace(NOTEBOOK_EXTENSION, '.py')
            notebook = self.output_path + os.path.sep + name

            self.params.append({NAME: '@PATH@', VALUE: self.output_path, TYPE: CONSTANT})

            logging.info('Notebook: %s version: %s running with kernel %s', name, str(AS_VERSION), self.kernel_name)
            logging.info('Running cells...')

            # Add cell to read env variables file
            # nb.cells.insert(0, Utils.get_cell_read_env())

            # Add cell to init
            nb.cells.insert(0, Utils.start_cell(self.params))

            # Add cell to save env variables
            nb.cells.insert(len(nb.cells) + 1, Utils.end_cell())
            # for n in range(0, len(nb.cells)):
            #     if nb.cells[n].cell_type == 'code' and nb.cells[n].source.startswith('%%writetest'):
            #         print("CELLLL")
            #         nb.cells[n].source = nb.cells[n].source.replace('line.py', 'test_line_' + value_accum + '_' + str(n) + '.py')
            #         print(nb.cells[n].source)
            # => Executing notebook
            ep = ExecutePreprocessor(timeout=TIMEOUT, kernel_name=self.kernel_name, startup_timeout=STARTUP_TIMEOUT)
            try:
                out = ep.preprocess(nb, {})

                # logging.info('NOTEBOOK\n\n %s', out)
                logging.info('Notebook: %s executed successfully', name)
                logging.info('Saving notebook: %s', notebook)

            except CellExecutionError:
                out = None
                logging.error('Error executing the notebook \'%s\'.\n\n See notebook \'%s\' for the traceback.',
                              name, notebook)
                raise
            finally:
                with open(notebook, mode=MODE, encoding=UTF_8) as fnb:
                    nbformat.write(nb, fnb)
