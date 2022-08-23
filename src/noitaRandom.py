import ctypes

lib = ctypes.cdll.LoadLibrary("./assets/noita_random.dll")

lib.SetRandomSeed.restype = ctypes.c_double
lib.Random.restype = ctypes.c_int
lib.Randomf.restype = ctypes.c_double
lib.Randomfn.restype = ctypes.c_double
lib.ProceduralRandomf.restype = ctypes.c_double
lib.ProceduralRandomfn.restype = ctypes.c_double
lib.ProceduralRandomi.restype = ctypes.c_int
lib.RandomDistribution.restype = ctypes.c_int
lib.RandomDistributionf.restype = ctypes.c_float


lib.SetRandomSeed.argtypes = [ctypes.c_uint64, ctypes.c_double, ctypes.c_double]
lib.Random.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
lib.Randomf.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double)]
lib.Randomfn.argtypes = [ctypes.POINTER(ctypes.c_double)]
lib.ProceduralRandomfn.argtypes = [ctypes.c_uint64, ctypes.c_double, ctypes.c_double]
lib.ProceduralRandomf.argtypes = [ctypes.c_uint64, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int]
lib.ProceduralRandomi.argtypes = [ctypes.c_uint64, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int]
lib.RandomDistribution.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_float, ctypes.POINTER(ctypes.c_double)]
lib.RandomDistributionf.argtypes = [ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.POINTER(ctypes.c_double)]


class NoitaRandom:
    def __init__(self, worldSeed):
        self.worldSeed = worldSeed
        self.randomSeed = ctypes.c_double(0)

    def SetRandomSeed(self, a: float, b: float):
        self.randomSeed = ctypes.c_double(lib.SetRandomSeed(self.worldSeed, a, b))

    def Random(self, a: int, b: int):
        return lib.Random(a, b, ctypes.byref(self.randomSeed))

    def Randomfn(self):
        return lib.Randomfn(ctypes.byref(self.randomSeed))

    def Randomf(self, a: float, b: float):
        return lib.Randomf(a, b, ctypes.byref(self.randomSeed))

    def RandomDistribution(self, min: int, max: int, mean: int, sharpness: float):
        return lib.RandomDistribution(min, max, mean, sharpness, ctypes.byref(self.randomSeed))

    def RandomDistributionf(self, min: float, max: float, mean: float, sharpness: float):
        return lib.RandomDistributionf(min, max, mean, sharpness, ctypes.byref(self.randomSeed))

class NoitaProceduralRandom: # TODO typehint this later
    def __init__(self, worldSeed, x, y):
        self.worldSeed = worldSeed

        self.x = x
        self.y = y
        
    def ProceduralRandomi(self, a, b):
        res = lib.ProceduralRandomi(self.worldSeed, self.x, self.y, a, b)
        self.y += 1
        return res

    def ProceduralRandomf(self, a, b):
        res = lib.ProceduralRandomf(self.worldSeed, self.x, self.y, a, b)
        self.y += 1
        return res

    def ProceduralRandomfn(self):
        res = lib.ProceduralRandomfn(self.worldSeed, self.x, self.y)
        self.y += 1
        return res