import json
import os


class Utils:
    @staticmethod
    def read_config_file(file_path):
        try:
            file = open(file_path)
            return json.load(file)
        except FileNotFoundError:
            return None

    @staticmethod
    def read_env_file(file_path):
        try:
            file = open(file_path)
            args = dict()
            for line in file:
                key, value = line.split('=')
                args[key] = value.replace('\n', '')
            return args
        except FileNotFoundError:
            return None

    @staticmethod
    def get_env():
        return os.environ.copy()

    @staticmethod
    def set_env(env):
        os.environ.update(env)

    @staticmethod
    def clean_env():
        os.environ.clear()

