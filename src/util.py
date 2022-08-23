import os
import shutil
import json
import subprocess
import re
from types import FunctionType
from typing import Any

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PIL import Image


def safeReadJson(path: str, con: FunctionType) -> dict:
    data = None
    if (os.path.exists(path)):
        with open(path, "r") as f:
            customdecoder = json.JSONDecoder(object_pairs_hook=con)

            return customdecoder.decode(f.read())
    else:
        with open(path, "w") as f:
            return con()
    
def safeDelete(path: str):
    if (os.path.exists(path)):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

def getUniqueColor(arg: Any) -> list[int]:
    res = [0, 0, 0]
    if (isinstance(arg, str)):
        total = 0
        p = 31
        m = 1e9 + 9
        pow = 1

        for i in arg:
            total = (total + (ord(i) - ord("a") + 1) * pow) % m
            pow = (pow * p) % m

        total %= 16581375
        
        rgb = int(total)

        res = [rgb & 255, (rgb >> 8) & 255, (rgb >> 16) & 255]
        
        return res

def setTextGeo(but: QPushButton, font: QFontMetrics, x: float, y: float):
    textSize = font.size(0, but.text())
    but.setGeometry(x, y, textSize.width(), textSize.height())

    return but.geometry()


def safeCopyFileFolder(path: str, out: str) -> bool:
    if (os.path.exists(path)):
        if (os.path.isdir(path)):
            shutil.copytree(path, out)
        else:
            shutil.copyfile(path, out)

        return True
    
    return False

def getProcessesRunning() -> list[dict]:
    tasks = str(subprocess.check_output(['tasklist'])).split("\\r\\n")
    p = []
    for task in tasks:
        m = re.match("(.+?) +(\d+) (.+?) +(\d+) +(\d+.* K).*",task)
        if m is not None:
            p.append({"image":m.group(1),
                        "pid":m.group(2),
                        "session_name":m.group(3),
                        "session_num":m.group(4),
                        "mem_usage":m.group(5)
                        })
    return p

def clamp(n: int | float, smallest: int | float, largest: int | float) -> int | float : return max(smallest, min(n, largest))

def get_concat_h(im1, im2):
    dst = Image.new('RGBA', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

def get_concat_v(im1, im2):
    dst = Image.new('RGBA', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst
