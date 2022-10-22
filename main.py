import json
import os

from src import Scheduler

if __name__ == '__main__':
    print(os.path.dirname(os.path.realpath(__file__)))
    scheduler = Scheduler()
    scheduler.run()
    #print("Params: ", json.dumps(params, indent=2))
