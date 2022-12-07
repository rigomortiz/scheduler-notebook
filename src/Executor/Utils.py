import json
import numpy as np
import nbformat
from src.Executor.Constants import *


class Utils:
    @staticmethod
    def read_config_file(file_path: str) -> dict or None:
        try:
            file = open(file_path)
            return json.load(file)
        except FileNotFoundError:
            return None

    @staticmethod
    def read_env_file(file_path: str) -> dict or None:
        try:
            file = open(file_path)
            args = dict()
            for line in file:
                key, value = line.split('=')
                args[key] = value.replace('\n', '')
                os.environ[key] = value.replace('\n', '')
            return args
        except FileNotFoundError:
            return None

    @staticmethod
    def write_params_to_notebook(params):
        with open(INPUT_PATH + os.sep + ENV_FILE, MODE) as file:
            for param in params:
                file.write(param + '\n')

    @staticmethod
    def get_env() -> dict:
        return os.environ.copy()

    @staticmethod
    def set_env(params: list) -> None:
        for param in params:
            os.environ[param[NAME]] = param[VALUE]

    @staticmethod
    def clean_env() -> None:
        os.environ.clear()

    @staticmethod
    def create_directories(folder) -> None:
        if not os.path.exists(OUTPUT_PATH):
            os.makedirs(OUTPUT_PATH)
        if not os.path.exists(OUTPUT_PATH + os.sep + folder):
            os.makedirs(OUTPUT_PATH + os.sep + folder)

    @staticmethod
    def get_cell_read_env() -> nbformat.notebooknode.NotebookNode:
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
    def end_cell() -> nbformat.notebooknode.NotebookNode:
        source = '''
import os

os.remove(PATH + os.path.sep + 'test-tmp.py')

with open(PATH + os.path.sep + '.env', 'w') as file:
    print('Saving .env ...')
    vs = [[x.replace('@', ''), os.environ[x]] for x in list(os.environ.copy().keys()) if x[0] == '@' and x[-1] == '@']
    for v in vs:
        file.write(v[0] + '=' + v[1] + "\\n")

    '''

        return nbformat.v4.new_code_cell(source)

    @staticmethod
    def start_cell(params) -> nbformat.notebooknode.NotebookNode:
        ps = ''.join(['%env ' + param[NAME] + ' = ' + param[VALUE] + '\n' for param in params])
        source = '''
from IPython.core.magic import register_line_cell_magic
import pytest
import os


'''

        source += ps + '''
        
PATH = %env @PATH@        
if os.path.exists(PATH + os.path.sep + 'test.py'):
    os.remove(PATH + os.path.sep + 'test.py')

@register_line_cell_magic
def write_test(line, cell):
    print('Running Tests ...')
    if cell is None:
        with open(PATH + os.path.sep + 'test.py', 'a') as f:
            f.write(cell.format(**globals()))
            f.close()
    else:
        with open(PATH + os.path.sep + 'test.py', 'a') as f:
            f.write(cell.format(**globals()))
            f.close()

    with open(PATH + os.path.sep + 'test-tmp.py', 'w') as f:
        f.write(cell.format(**globals()))
        f.close()
    #pytest.main(['-v', PATH + os.path.sep + 'test.py'])
    csv_file = PATH + os.path.sep + 'In[' + str(len(globals()['In']) - 1) + '].csv'
    csv_cols = "--csv-columns 'name,status,message,duration_formatted,function,parameters_as_columns'"
    res = os.system('pytest --csv ' + csv_file + ' ' + PATH + os.path.sep + 'test-tmp.py')
'''

        return nbformat.v4.new_code_cell(source)

    @staticmethod
    def merge_notebooks(paths, path_output):
        cells = []
        for p in paths:
            with open(p, 'r') as file:
                cells.append(json.loads(file.read())['cells'])

        with open(paths[0], 'r') as file:
            new_dict = json.loads(file.read()).copy()
            new_dict['cells'] = list(np.concatenate(cells))

        with open(path_output, 'w') as json_file:
            json.dump(new_dict, json_file)

        return True
