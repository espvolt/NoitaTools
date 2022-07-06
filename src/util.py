import os
import json

def safeReadJson(path: str, con):
    data = None
    if (os.path.exists(path)):
        with open(path, "r") as f:
            return json.load(f)
    else:
        with open(path, "w") as f:
            return con()
