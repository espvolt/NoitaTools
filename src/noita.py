import base64
from copy import copy
import io
from itertools import count
import math
from operator import truediv
import os
from pprint import pprint
from re import S
from turtle import end_fill
from types import NoneType
from typing import Any, OrderedDict
from warnings import filters
import winreg
import shutil
import PyQt5.QtWidgets, PyQt5.QtGui

import ctypes
import pymem
import pymem.process

import collections
import util
import noitaWandProb

from noitaRandom import NoitaRandom

from PIL import Image, ImageQt

# lib = ctypes.cdll.LoadLibrary("./assets/noita_random.dll")

# lib.SetRandomSeed.restype = ctypes.c_double
# lib.Random.restype = ctypes.c_int
# lib.Randomf.restype = ctypes.c_double
# lib.Randomfn.restype = ctypes.c_double
# lib.ProceduralRandomf.restype = ctypes.c_double
# lib.ProceduralRandomfn.restype = ctypes.c_double
# lib.ProceduralRandomi.restype = ctypes.c_int

# lib.SetRandomSeed.argtypes = [ctypes.c_uint64, ctypes.c_double, ctypes.c_double]
# lib.Random.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
# lib.Randomf.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
# lib.Randomfn.argtypes = [ctypes.POINTER(ctypes.c_double)]
# lib.ProceduralRandomfn.argtypes = [ctypes.c_uint64, ctypes.c_double, ctypes.c_double]
# lib.ProceduralRandomf.argtypes = [ctypes.c_uint64, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int]
# lib.ProceduralRandomi.argtypes = [ctypes.c_uint64, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int]


def noitaAppDataPath() -> str:
    roaming = os.getenv("APPDATA")
    return "\\".join(roaming.split("\\")[:-1]) + "\\LocalLow\\Nolla_Games_Noita"


def noitaSteamPath() -> str | None:
    hkey = None
    steamPath = None
    try:
        hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\WOW6432Node\Valve\Steam")
    except:
        return None

    try:
        steamPath = winreg.QueryValueEx(hkey, "InstallPath")
    except:
        return None
        
    return steamPath[0] + "\\steamapps\\common\\Noita"

def noitaSteamWorkshopPath() -> str | None:
    hkey = None
    steamPath = None
    try:
        hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\WOW6432Node\Valve\Steam")
    except:
        return None

    try:
        steamPath = winreg.QueryValueEx(hkey, "InstallPath")
    except:
        return None

    return steamPath[0] + "\\steamapps\\workshop\\content\\881100"


def isNoitaOpen() -> bool:
    for i in util.getProcessesRunning():
        if (i["image"] == "noita.exe" or i["image"] == "noita_dev.exe"):
            return True

    return False

def getNoitaType() -> str | None:
    for i in util.getProcessesRunning():
        if (i["image"] == "noita.exe" or i["image"] == "noita_dev.exe"):
            return i["image"]

    return None
def getCurrentNoitaSeed() -> int:
    addresses = {
        "noita.exe": 0xBEE850,
        "noita_dev.exe": 0xCEB0D4
    }
    addr = 0xBEE850

    t = getNoitaType()
    pm = pymem.Pymem(t)
    offset = pymem.process.module_from_name(pm.process_handle, t).lpBaseOfDll

    return pm.read_int(offset + addresses[t])


def installUtilMod(gamePath: str): # this is really bad :(
    if ((os.path.exists(gamePath + "\\mods\\__noitatoolhelper") and os.path.isdir(gamePath + "\\mods\\__noitatoolhelper"))):
        shutil.rmtree(gamePath + "\\mods\\__noitatoolhelper")

    shutil.unpack_archive("./assets/noitamod.zip", gamePath + "\\mods\\__noitatoolhelper", "zip")
    for i in os.listdir(gamePath + "\\mods\\__noitatoolhelper\\noitamod"):
        shutil.move(gamePath + "\\mods\\__noitatoolhelper\\noitamod\\" + i, gamePath + "\\mods\\__noitatoolhelper")
    
    os.rmdir(gamePath + "\\mods\\__noitatoolhelper\\noitamod")

    initData = ""

    with open(gamePath + "\\mods\\__noitatoolhelper\\init.lua", "r") as f:
        initData = f.read()

    with open(gamePath + "\\mods\\__noitatoolhelper\\init.lua", "w") as f:
        f.write("noitaToolsDir = \"" + os.getcwd().replace("\\", "/") + "\"\n" + initData)


def copyModsList(names: list[str], gamePath: str, workshopPath: str = None, progressLabel: PyQt5.QtWidgets.QLabel = None):
    if (os.path.exists(gamePath + "/mods")):
        for i in os.listdir(gamePath + "/mods"):
            if (not os.path.isdir(gamePath + "/mods/" + i)):
                continue

            if (i in names):
                names.remove(i)

                if (progressLabel is not None):
                    progressLabel.setText("Copying " + i)

                shutil.copytree(gamePath + "/mods/" + i, "assets/mods/" + i)

    if (workshopPath is None):
        return

    for i in os.listdir(workshopPath):
        current = workshopPath + "/" + i

        if (not os.path.exists(current + "/mod_id.txt")):
            continue

        else:
            text = None
            
            with open(current + "/mod_id.txt", "r") as f:
                text = f.read()

            if (text in names):
                names.remove(text)

                if (progressLabel is not None):
                    progressLabel.setText("Copying " + text + "(" + i + ")")

                shutil.copytree(current, "assets/mods/" + text)

data = util.safeReadJson("./data.json", collections.OrderedDict)["spellAssets"]
wandData = util.safeReadJson("./assets/wand.json", collections.OrderedDict)

def filterSpellData(data: dict):
    filtered = [] 
    for spell in data:
        copied = copy(spell)

        if (isinstance(spell["spawnProbability"], str)):        
            probs = [float(i) for i in copied["spawnProbability"].split(",")]
            levels = [int(i) for i in copied["spawnLevel"].split(",")]
            copied["spawnProbability"] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            
            for i, v in enumerate(levels):
                copied["spawnProbability"][v] = probs[i]

        else:
            copied["spawnProbability"] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        filtered.append(copied)

    return filtered
    ...
    
def shuffleList(l: list, rand: NoitaRandom): # NOITA
    its = len(l)

    for i in range(its, 1, -1):
        j = rand.Random(1, i)
        l[i - 1], l[j - 1] = l[j - 1], l[i - 1]


def getPerkList(worldSeed: int, data: list[dict], ignore: list[str], state: Any) -> list[str]: # Needs a bit more 
    rand = NoitaRandom(worldSeed)
    rand.SetRandomSeed(1, 2)

    pool = []

    minDist = 4
    defaultMax = 128


    stackableDists = {}
    stackableCounts = {}

    for i, data in enumerate(data):
        if (data["id"] not in ignore and data["default"]):
            name = data["id"]
            times = 1

            stackableDists[name] = -1
            stackableCounts[name] = -1

            if (data["stackable"]):
                maxPerks = rand.Random(1, 2)

                if (data["maxInPerkPool"]):
                    maxPerks = rand.Random(1, data["maxInPerkPool"])

                if (data["stackableMax"]):
                    stackableCounts[name] = data["stackableMax"]
                else:
                    stackableCounts[name] = defaultMax

                if (data["stackableRare"]):
                    maxPerks = 1

                stackableDists[name] = data["stackableReappearRate"] if data["stackableReappearRate"] else minDist

                times = rand.Random(1, maxPerks)

            for i in range(times):
                pool.append(data["id"])

    shuffleList(pool, rand)

    for i in range(len(pool) - 1, -1, -1): # -1 :)
        perk = pool[i]

        if (stackableDists[perk] != -1):
            minDist = stackableDists[perk]
            remove = False

            for j in range(i - minDist, i - 1, 1):
                if (j >= 0 and pool[j] == perk):
                    remove = True
                    break

            if remove:
                pool.pop(i)

    return pool

def perkReroll(worldSeed: int, data: list, numPerks: int=3, rerollCount: int=0, rerollIndex: int=-1) -> dict[str, list | int]:
    res = {
        "perks": []
    }

    perks = getPerkList(worldSeed, data, [], None)

    if (rerollIndex == -1):
        rerollIndex = len(perks) - 1

    for _ in range(numPerks):
        perk = perks[rerollIndex]
        rerollIndex -= 1
        if (rerollIndex < 0):
            rerollIndex = len(data) - 1

        res["perks"].append(perk)
        
    res["rerollIndex"] = rerollIndex

    return res


def getPerkLucky(worldSeed: int, chance: float=100, extraLevel: int=0, index: int=0) -> list[bool]:
    res = []
    rand = NoitaRandom(worldSeed)

    defaultStart = [-22, -24, -26, -27, -28, -28]
    specialStart = [2570, 2568, 2566, 2565, 2564, 2564] # The laboratory hm

    defaultSteps = [[20, 20], # Weird
                    [14, 16, 14],
                    [12, 12, 12, 12],
                    [10, 10, 10, 10, 10],
                    [9, 8, 9, 9, 8, 9],
                    [7, 8, 7, 8, 7, 8, 7]]

    yLevels = [1410, 2936, 4994, 6530, 8578, 10626, 13181]

    index = min(index, len(yLevels) - 1)
    extraLevel = min(extraLevel, len(defaultStart) - 1)
    
    start: int = None
    step: int = defaultSteps[extraLevel]
    yLevel = yLevels[index]

    numPerks = 3 + extraLevel

    if (index == len(yLevels) - 1):
        start = specialStart[extraLevel]
    else:
        start = defaultStart[extraLevel]
    
    current = start

    for i in range(numPerks):
        rand.SetRandomSeed(current, yLevel)

        if (rand.Random(1, 100) > chance):
            res.append(True)
        else:
            res.append(False)

        if (i <= len(step) - 1):
            current += step[i]

    return res

def addLuckyIcon(dir1: str, dir2: str, resize: tuple[int, int]) -> PyQt5.QtGui.QPixmap:
    im = Image.open(dir1)
    im = im.resize(resize)
    im2 = Image.open(dir2)

    im.paste(im2, (0, 0))


    return PyQt5.QtGui.QPixmap.fromImage(ImageQt.ImageQt(im))

class ActionType:
    PROJECTILE	      = 0
    STATIC_PROJECTILE = 1
    MODIFIER	      = 2
    DRAW_MANY	      = 3
    MATERIAL	      = 4
    OTHER		      = 5
    UTILITY		      = 6
    PASSIVE		      = 7

def getRandomAction(spellData: list[dict], worldSeed: int, x: float, y: float, level: int, offset: int=0, type: ActionType=None) -> dict:
    s = 0
    
    for spell in spellData:
        if (type is not None):
            if (spell["type"] == type):
                s += spell["spawnProbability"][level]
        else:
            s += spell["spawnProbability"][level]
    
    prng = NoitaRandom(worldSeed + offset)
    prng.SetRandomSeed(ctypes.c_double(ctypes.c_float(x).value), ctypes.c_double(ctypes.c_float(y).value))
    multipl = prng.Randomfn()
    accumulated = s * multipl

 
    for spell in spellData:
        probability = spell["spawnProbability"][level]
    
        if (type is not None):
            if (spell["type"] != type):
                continue

        if (probability == 0):
            continue
          
        if (probability >= accumulated):
            return spell

        accumulated -= probability

    return spellData[0]

wandData = util.safeReadJson("./assets/wand.json", dict)

def generateShopItem(rand: NoitaRandom, spellData: list[dict], worldSeed: int, x: float, y: float, cheap: bool) -> dict:
    biomes = {1: 0, 2: 0, 3: 0,
		      4: 1, 5: 1, 6: 1,
		      7: 2, 8: 2, 9: 2, 10: 2, 11: 2, 12: 2,
	    	  13: 3, 14: 3, 15: 3, 16: 3,
              17: 4, 18: 4, 19: 4, 20: 4,
              21: 5, 22: 5, 23: 5, 24: 5,
              25: 6, 26: 6, 27: 6, 28: 6, 29: 6, 30: 6, 31: 6, 32: 6, 33: 6}

    biomep = math.floor(y / 512)

    biomeid = 0 if biomep not in biomes else biomes[biomep]

    if (biomep > 35):
        biomeid = 7

    action = getRandomAction(spellData, worldSeed, x, y, biomeid, 0)
    price = max(math.floor((action["price"] * .3 + (70 * (biomeid ** 2))) / 10) * 10, 10)
    
    return action, int(price * .5) if cheap else price

def generateShopWand(rand: NoitaRandom, spellData: list[dict], worldSeed: int, x: float, y: float, cheap: bool) -> dict:
    rand.SetRandomSeed(x, y)
    
    biomes = {1: 0, 2: 0, 3: 0,
		      4: 1, 5: 1, 6: 1,
		      7: 2, 8: 2, 9: 2, 10: 2, 11: 2, 12: 2,
	    	  13: 3, 14: 3, 15: 3, 16: 3,
              17: 4, 18: 4, 19: 4, 20: 4,
              21: 5, 22: 5, 23: 5, 24: 5,
              25: 6, 26: 6, 27: 6, 28: 6, 29: 6, 30: 6, 31: 6, 32: 6, 33: 6}

    biomep = math.floor(y / 512)

    biomeid = 0 if biomep not in biomes else biomes[biomep]

    biomeid = util.clamp(biomeid, 1, 6)
    
    x = round(x) # Wacky
    y = round(y)

    unshuffleWandArgs = {
        1: [worldSeed, spellData, x, y, 30, 1, False],
        2: [worldSeed, spellData, x, y, 40, 2, False],
        3: [worldSeed, spellData, x, y, 60, 3, False],
        4: [worldSeed, spellData, x, y, 80, 4, False],
        5: [worldSeed, spellData, x, y, 100, 5, False],
        6: [worldSeed, spellData, x, y, 120, 6, False]
    }

    shuffleWandArgs = {
        1: [worldSeed, spellData, x, y, 25, 1, True],
        2: [worldSeed, spellData, x, y, 40, 2, True],
        3: [worldSeed, spellData, x, y, 60, 3, True],
        4: [worldSeed, spellData, x, y, 80, 4, True],
        5: [worldSeed, spellData, x, y, 100, 5, True],
        6: [worldSeed, spellData, x, y, 120, 6, True]
    }

    wand = None

    r = rand.Random(0, 100)

    if (r <= 50):
        wand = generateGun(*unshuffleWandArgs[biomeid])
    else:
        wand = generateGun(*shuffleWandArgs[biomeid])
    
    biomeid = (.5 * biomeid) + (.5 * biomeid * biomeid)

    wandCost = (50 + biomeid * 210) + (rand.Random(-15, 15) * 10)

    if (cheap):
        wandCost *= .5

    return wand, wandCost

# I NEED TO REDO THE WAND STUFF BUT I GIVE UP FOR NOW

def applyRandomVariable(rand: NoitaRandom, gun: dict[str], variable: str):
    cost = gun["cost"]
    probs = noitaWandProb.getGunProbs(variable, rand)

    if (variable == "reload_time"):
        min = util.clamp(60 - (cost * 5), 1, 240)
        max = 1024

        gun[variable] = util.clamp(rand.RandomDistribution(int(probs["min"]), int(probs["max"]), int(probs["mean"]), probs["sharpness"]), min, max)
        gun["cost"] -= ((60 - gun[variable]) / 5)
        return

    if (variable == "fire_rate_wait"):
        min = util.clamp(16 - cost, -50, 50)
        max = 50

        gun[variable] = util.clamp(rand.RandomDistribution(int(probs["min"]), int(probs["max"]), int(probs["mean"]), probs["sharpness"]), min, max)
        gun["cost"] -= 16 - gun[variable]
        return

    if (variable == "spread_degrees"):
        min = util.clamp(cost / -1.5, -35, 35)
        max = 35 

        gun[variable] = util.clamp(rand.RandomDistribution(int(probs["min"]), int(probs["max"]), int(probs["mean"]), probs["sharpness"]), min, max)
        gun["cost"] -= 16 - gun[variable]
        return

    if (variable == "speed_multiplier"):
        gun[variable] = rand.RandomDistributionf(probs["min"], probs["max"], probs["mean"], probs["sharpness"])    
        return

    if (variable == "deck_capacity"):
        min = 1
        max = util.clamp((cost / 5) + 6, 1, 20)

        if (gun["force_unshuffle"]):
            min = 1
            max = ((cost - 15) / 5)

            if (max > 6):
                max = 6 + ((cost - (15 + 6 * 5)) / 10)

        max = util.clamp(max, 1, 20)

        gun[variable] = util.clamp(rand.RandomDistribution(int(probs["min"]), int(probs["max"]), int(probs["mean"]), probs["sharpness"]), min, max)
        gun["cost"] -= ((gun[variable] - 6) * 5)
        return

    deck_capacity = gun["deck_capacity"]

    if (variable == "shuffle_deck_when_empty"):
        r = rand.Random(0, 1)

        if (gun["force_unshuffle"]):
            r = 1
            if (cost < (15 + deck_capacity * 5)):
                print("DEBUG: " + str(cost))
                print("This shouldn't happen.")

        if (r and cost >= (15 + deck_capacity * 5) and deck_capacity <= 9):
            gun[variable] = False
            gun["cost"] -= (15 + deck_capacity * 5)
        
        return

    if (variable == "actions_per_round"):
        action_costs = [
            0,
            5 + (deck_capacity * 2),
            15 + (deck_capacity * 3.5),
            35 + (deck_capacity * 5),
            45 + (deck_capacity ** 2),
        ]

        min = 1
        max = 1

        for i, action_cost in enumerate(action_costs):
            if (action_cost <= cost):
                max = i + 1

        max = util.clamp(max, 1, deck_capacity)

        gun[variable] = math.floor(util.clamp(rand.RandomDistribution(int(probs["min"]), int(probs["max"]), int(probs["mean"]), probs["sharpness"]), min, max))
        temp_cost = action_costs[util.clamp(gun[variable] - 1, 0, len(action_costs) - 1)]

        gun["cost"] -= temp_cost

def getGunData(rand: NoitaRandom, cost: int, level: int, force_unshuffle: bool) -> dict:
    gun = OrderedDict()

    if (level == 1):
        if (rand.Random(0, 100) < 50):
            cost += 5

    cost += rand.Random(-3, 3)

    gun["deck_capacity"] = 0
    gun["reload_time"] = 0
    gun["mana_charge_speed"] = 50 * level + rand.Random(-5, 5 * level)
    gun["is_rare"] = False
    gun["force_unshuffle"] = False
    gun["speed_multiplier"] = 0
    gun["shuffle_deck_when_empty"] = True
    gun["mana_max"] = 50 + (150 * level) + (rand.Random(-5, 5) * 10)
    gun["actions_per_round"] = 0
    gun["prob_draw_many"] = 0.15
    gun["prob_unshuffle"] = 0.1
    gun["fire_rate_wait"] = 0
    gun["spread_degrees"] = 0
    gun["cost"] = cost

    p = rand.Random(0, 100)

    if (p < 20):
        gun["mana_charge_speed"] = (50 * level + rand.Random(-5, 5 * level)) / 5
        gun["mana_max"] = (50 + (150 * level) + (rand.Random(-5, 5) * 10)) * 3

    p = rand.Random(0, 100)
    if (p < 15):
        gun["mana_charge_speed"] = (50 * level + rand.Random(-5, 5 * level)) * 5
        gun["mana_max"] = (50 + (150 * level) + (rand.Random(-5, 5) * 10)) / 3
        
    if (gun["mana_max"] < 50):
        gun["mana_max"] = 50

    if (gun["mana_charge_speed"] < 10):
        gun["mana_charge_speed"] = 10

    p = rand.Random(0, 100)
    if (p < 15 + level * 6):
        gun["force_unshuffle"] = True


    p = rand.Random(0, 100)
    if (p < 5):
        gun["is_rare"] = True
        gun["cost"] += 65

    vars1 = ["reload_time", "fire_rate_wait", "spread_degrees", "speed_multiplier"]
    vars2 = ["deck_capacity"]
    vars3 = ["shuffle_deck_when_empty", "actions_per_round"]

    shuffleList(vars1, rand)

    if (not gun["force_unshuffle"]): shuffleList(vars3, rand)

    for i in vars1:
        applyRandomVariable(rand, gun, i)
    
    for i in vars2:
        applyRandomVariable(rand, gun, i)

    for i in vars3:
        applyRandomVariable(rand, gun, i)


    if (gun["cost"] > 5 and rand.Random(0, 1000) < 995):
        if (gun["shuffle_deck_when_empty"]):
            gun["deck_capacity"] += (gun["cost"] / 5)
            gun["cost"] = 0

        else:
            gun["deck_capacity"] += (gun["cost"] / 10)
            gun["cost"] = 0

    if (force_unshuffle):
        gun["shuffle_deck_when_empty"] = False

    if (rand.Random(0, 10000) <= 9999):
        gun["deck_capacity"] = util.clamp(gun["deck_capacity"], 2, 26)
    
    if (gun["deck_capacity"] <= 1):
        gun["deck_capacity"] = 2

    if (gun["reload_time"] >= 60):
        def random_add_actions_per_round():
            gun["actions_per_round"] += 1

            if (rand.Random(0, 100) < 70):
                random_add_actions_per_round()

        random_add_actions_per_round()

        if (rand.Random(0, 100) < 50):
            new_actions_per_round = gun["deck_capacity"]

            for i in range(6):
                temp_actions_per_round = rand.Random(int(gun["actions_per_round"]), int(gun["deck_capacity"]))

                if (temp_actions_per_round < new_actions_per_round):
                    new_actions_per_round = temp_actions_per_round

            gun["actions_per_round"] = new_actions_per_round

    gun["actions_per_round"] = util.clamp(gun["actions_per_round"], 1, gun["deck_capacity"])
    
    # debug
    # print(vars1)
    # print(vars3)
    # print(gun)

    # print("bruh", rand.Random(0, 100))

    return gun

def wandDiff(gun: dict, wand: dict) -> float: # TODO
    score = 0.0

    score += abs(gun["fire_rate_wait"] - wand["fire_rate_wait"])
    score += abs(gun["actions_per_round"] - wand["actions_per_round"])
    score += abs(gun["shuffle_deck_when_empty"] - wand["shuffle_deck_when_empty"])
    score += abs(gun["deck_capacity"] - wand["deck_capacity"])
    score += abs(gun["spread_degrees"] - wand["spread_degrees"])
    score += abs(gun["reload_time"] - wand["reload_time"])
    return score

def inbetween(gun: dict, rand: NoitaRandom):
    best_wand: dict | None = None
    best_score = 1000
    gun_ = {}

    gun_["fire_rate_wait"] = util.clamp(gun["fire_rate_wait"] + 5 / 7 - 1, 0, 4)
    gun_["actions_per_round"] = util.clamp(gun["actions_per_round"] - 1, 0, 2)
    gun_["shuffle_deck_when_empty"] = util.clamp(gun["shuffle_deck_when_empty"], 0, 1)
    gun_["deck_capacity"] = util.clamp((gun["deck_capacity"] - 3) / 3, 0, 7)
    gun_["spread_degrees"] = util.clamp((gun["spread_degrees"] + 5) / 5 - 1, 0, 2)
    gun_["reload_time"] = util.clamp((gun["reload_time"] + 5) / 25 - 1, 0, 2)

    for wand in wandData:
        score = wandDiff(wand, gun_)

        if (score <= best_score):
            best_wand = wand
            best_score = score

            if (score == 0 and rand.Random(0, 100) < 33):
                return best_wand

    return best_wand

def getWandCards(rand: NoitaRandom, spellData: list[dict], gun: dict[str, Any], x: float, y: float, level: int):
    # NOTE This should be correct, but i just need the random seed to be correct.

    res_cards: dict[str, list | Any] = {
        "cards": [],
        "always": None
    }

    is_rare = gun["is_rare"]

    good_cards = 5

    if (rand.Random(0, 100) < 7): good_cards = rand.Random(20, 50)
    if (is_rare): good_cards *= 2
    if (level is None): level = 1

    orig_level = level
    level -= 1
    deck_capacity = gun["deck_capacity"]
    actions_per_round = gun["actions_per_round"]
    card_count = rand.Random(1, 3)
    bullet_card = getRandomAction(spellData, rand.worldSeed, x, y, level, 0, ActionType.PROJECTILE)
    card = None
    random_bullets = 0
    good_card_count = 0

    # REDO IF FAILS HERE   

    if (rand.Random(0, 100) < 50 and card_count < 3): card_count += 1
    if (rand.Random(0, 100) < 10 or is_rare): card_count += rand.Random(1, 2)

    good_cards = rand.Random(5, 45)
    card_count = int(util.clamp(rand.Random(round(.51 * deck_capacity), round(deck_capacity)), 1, deck_capacity - 1))
    
    if (rand.Random(0, 100) < (orig_level * 10) - 5): random_bullets = 1

    if (rand.Random(0, 100) < 4 or is_rare):
        p = rand.Random(0, 100)
        if (p < 77):
            card = getRandomAction(spellData, rand.worldSeed, x, y, level + 1, 666, ActionType.MODIFIER)
        elif (p < 85):
            card = getRandomAction(spellData, rand.worldSeed, x, y, level + 1, 666, ActionType.MODIFIER)
            good_card_count += 1
        elif (p < 93):
            card = getRandomAction(spellData, rand.worldSeed, x, y, level + 1, 666, ActionType.STATIC_PROJECTILE)
        else:
            card = getRandomAction(spellData, rand.worldSeed, x, y, level + 1, 666, ActionType.PROJECTILE)
        
        res_cards["always"] = card

    if (rand.Random(0, 100) < 50):
        extra_level = level

        while (rand.Random(1, 10) == 10):
            extra_level += 1
            bullet_card = getRandomAction(spellData, rand.worldSeed, x, y, extra_level, 0, ActionType.PROJECTILE)

        if (card_count < 3):
            if (card_count > 1 and rand.Random(0, 100) < 20):
                card = getRandomAction(spellData, rand.worldSeed, x, y, level, 2, ActionType.MODIFIER)
                res_cards["cards"].append(card)
                card_count -= 1

            for _ in range(card_count):
                res_cards["cards"].append(bullet_card)
        else:
            if (rand.Random(0, 100) < 40):
                card = getRandomAction(spellData, rand.worldSeed, x, y, level, 1, ActionType.DRAW_MANY)
                res_cards["cards"].append(card)
                card_count -= 1
            
            if (card_count > 3 and rand.Random(0, 100) < 40):
                card = getRandomAction(spellData, rand.worldSeed, x, y, level, 1, ActionType.DRAW_MANY)
                res_cards["cards"].append(card)
                card_count -= 1

            if (rand.Random(0, 100) < 80):
                card = getRandomAction(spellData, rand.worldSeed, x, y, level, 2, ActionType.MODIFIER)
                res_cards["cards"].append(card)
                card_count -= 1

            for _ in range(card_count):
                res_cards["cards"].append(bullet_card)

    else:        
        for i in range(card_count):
            if (rand.Random(0, 100) < good_cards and card_count + 1 > 2):
                if (good_card_count == 0 and actions_per_round == 1):
                    card = getRandomAction(spellData, rand.worldSeed, x, y, level, i + 1, ActionType.DRAW_MANY)
                    good_card_count += 1

                else:
                    if (rand.Random(0, 100) < 83):
                        card = getRandomAction(spellData, rand.worldSeed, x, y, level, i + 1, ActionType.MODIFIER)

                    else:
                        card = getRandomAction(spellData, rand.worldSeed, x, y, level, i + 1, ActionType.DRAW_MANY)
                        
                        
                res_cards["cards"].append(card)
            else:
                res_cards["cards"].append(bullet_card)

                if (random_bullets == 1):
                    bullet_card = getRandomAction(spellData, rand.worldSeed, x, y, level, i + 1, ActionType.PROJECTILE)
    
    gun["cards"] = res_cards

def generateGun(worldSeed: int, spellData: dict, x: float, y: float, cost: int, level: int, force_unshuffle: bool) -> dict:
    rand = NoitaRandom(worldSeed)
    rand.SetRandomSeed(x, y)

    gun = getGunData(rand, cost, level, force_unshuffle)
    wa = inbetween(gun, rand)
    getWandCards(rand, spellData, gun, x, y, level)

    return gun, wa["file"][len("data:image/png;base64,"):]

def getShop(spellData: list[dict], worldSeed: int, level: int, itemCount: int=5) -> dict:
    rand = NoitaRandom(worldSeed)

    locations = [[-331, 1395],
                 [-331, 2931],
                 [-331, 4979],
                 [-331, 6515],
                 [-331, 8563],
                 [-331, 10611],
                 [2261, 13166]]

    x, y = locations[level]

    rand.SetRandomSeed(x, y)

    width = 132
    itemWidth = width / itemCount
    saleItem = rand.Random(1, itemCount) - 1

    if (rand.Random(0, 100) <= 50):
        spells = [[], []]

        for i in range(itemCount):
            if (i == saleItem):
                spells[1].append(generateShopItem(rand, spellData, worldSeed, x + itemWidth * i, y, True))
            else:
                spells[1].append(generateShopItem(rand, spellData, worldSeed, x + itemWidth * i, y, False))
            
            spells[0].append(generateShopItem(rand, spellData, worldSeed, x + i * itemWidth, y - 30, False))

        return spells, 1

    else:
        wands = []

        for i in range(itemCount):
            if (i == saleItem):
                wands.append(generateShopWand(rand, spellData, worldSeed, x + i * itemWidth, y, True))
            else:
                wands.append(generateShopWand(rand, spellData, worldSeed, x + i * itemWidth, y, False))
                
        return wands, 2
