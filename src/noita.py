import os
import winreg

def noitaAppDataPath():
    roaming = os.getenv("APPDATA")
    return "\\".join(roaming.split("\\")[:-1]) + "\\LocalLow\\Nolla_Games_Noita"

def noitaSteamPath():
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

    
    ...