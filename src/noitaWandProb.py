from pprint import pprint
from noitaRandom import NoitaRandom


def createGunProbs():
    gunProbs = {}
        
    gunProbs[ "deck_capacity" ] = {
        "prob": 0,
        "probs": [
            {
                "prob": 1,
                "min": 3,
                "max": 10,
                "mean": 6,
                "sharpness": 2,
            },
            {
                "prob": 0.1,
                "min": 2,
                "max": 7,
                "mean": 4,
                "sharpness": 4,
                "extra": lambda gunData: (gunData["prob_unshuffle"] + .8)
            },
            {
                "prob": 0.05,
                "min": 1,
                "max": 5,
                "mean": 3,
                "sharpness": 4,
                "extra": lambda gunData: (gunData["prob_unshuffle"] + .8)
            },
            {
                "prob": 0.15,
                "min": 5,
                "max": 11,
                "mean": 8,
                "sharpness": 2,
            },
            {
                "prob": 0.12,
                "min": 2,
                "max": 20,
                "mean": 8,
                "sharpness": 4,
            },
            {
                "prob": 0.15,
                "min": 3,
                "max": 12,
                "mean": 6,
                "sharpness": 6,
                "extra": lambda gunData: (gunData["prob_unshuffle"] + .8)
            },
            {
                "prob": 1,
                "min": 1,
                "max": 20,
                "mean": 6,
                "sharpness": 0,
            }
        ]
    }

    gunProbs[ "reload_time" ] = {
        "prob": 0,
        "probs": [
            {
                "prob": 1,
                "min": 5,
                "max": 60,
                "mean": 30,
                "sharpness": 2,
            },
            {
                "prob": 0.5,
                "min": 1,
                "max": 100,
                "mean": 40,
                "sharpness": 2,
            },
            {
                "prob": 0.02,
                "min": 1,
                "max": 100,
                "mean": 40,
                "sharpness": 0,
            },
            {
                "prob": 0.35,
                "min": 1,
                "max": 240,
                "mean": 40,
                "sharpness": 0,
                "extra": lambda gunData: gunData["prob_unshuffle"] + 0.5
            }
        ]
    }


    gunProbs[ "fire_rate_wait" ] = {
        "prob": 0,
        "probs": [
            {
                "prob": 1,
                "min": 1,
                "max": 30,
                "mean": 5,
                "sharpness": 2,
            },
            {
                "prob": 0.1,
                "min": 1,
                "max": 50,
                "mean": 15,
                "sharpness": 3,
            },
            {
                "prob": 0.1,
                "min": -15,
                "max": 15,
                "mean": 0,
                "sharpness": 3,
            },
            {
                "prob": 0.45,
                "min": 0,
                "max": 35,
                "mean": 12,
                "sharpness": 0,
            }
        ]
    }


    gunProbs[ "spread_degrees" ] = {
        "prob": 0,
        "probs": [ 
            {
                "prob": 1,
                "min": -5,
                "max": 10,
                "mean": 0,
                "sharpness": 3,
            },
            {
                "prob": 0.02,
                "min": 1,
                "max": 10,
                "mean": 3,
                "sharpness": 3,
            },
            {
                "prob": 0.02,
                "min": 1,
                "max": 11,
                "mean": 5,
                "sharpness": 3,
            },
            {
                "prob": 0.02,
                "min": -35,
                "max": 0,
                "mean": -10,
                "sharpness": 2,
            },
            {
                "prob": 0.1,
                "min": -35,
                "max": 35,
                "mean": 0,
                "sharpness": 0,
            }
        ]
    }

    gunProbs[ "speed_multiplier" ] = {
        "prob": 0,
        "probs": [
            {
                "prob": 1,
                "min": 0.8,
                "max": 1.2,
                "mean": 1,
                "sharpness": 6,
            },
            {
                "prob": 0.05,
                "min": 1,
                "max": 2,
                "mean": 1.1,
                "sharpness": 3,
            },
            {
                "prob": 0.05,
                "min": 0.5,
                "max": 1,
                "mean": 0.9,
                "sharpness": 3,
            },
            {
                "prob": 1,
                "min": 0.8,
                "max": 1.2,
                "mean": 1,
                "sharpness": 0,
            },
            {
                "prob": 0.001,
                "min": 1,
                "max": 10,
                "mean": 5,
                "sharpness": 2,
            }
        ]
    }


    gunProbs[ "actions_per_round" ] = {
        "prob": 0,
        "probs": [
            {
                "prob": 1,
                "min": 1,
                "max": 3,
                "mean": 1,
                "sharpness": 3,
            },
            {
                "prob": 0.2,
                "min": 2,
                "max": 4,
                "mean": 2,
                "sharpness": 8,
            },
            {
                "prob": 0.05,
                "min": 1,
                "max": 5,
                "mean": 2,
                "sharpness": 2,
            },
            {
                "prob": 1,
                "min": 1,
                "max": 5,
                "mean": 2,
                "sharpness": 0,
            }
        ]
    }

    return gunProbs

def initTotalProb(value):
    value["prob"] = 0
    for v in value["probs"]:
        if ("prob" in v):
            value["prob"] += v["prob"]

def initGunProbs(probs):
    for k in probs:
        initTotalProb(probs[k])  

def getGunProbs(var, rand: NoitaRandom):
    probs = createGunProbs()
    initGunProbs(probs)

    if (var not in probs):
        return None

    r = rand.Randomfn() * probs[var]["prob"]
    
    for v in probs[var]["probs"]:
        if ("prob" in v):
            if (r <= v["prob"]):
                return v

            r -= v["prob"]

    return None