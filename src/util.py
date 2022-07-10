import os
import shutil
import json

def safeReadJson(path: str, con):
    data = None
    if (os.path.exists(path)):
        with open(path, "r") as f:
            return json.load(f)
    else:
        with open(path, "w") as f:
            return con()
    
def safeDelete(path: str):
    if (os.path.exists(path)):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
