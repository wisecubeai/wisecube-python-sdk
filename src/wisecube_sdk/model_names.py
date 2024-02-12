from enum import Enum


class WisecubeModel(Enum):
    BBB = "BBB"  # ok
    LOGS = "logS" # ok
    CYP2CI9I = "CYP2CI9i" # ok
    LOGD7 = "LogD7" # ok
    CACO2 = "Caco2" #  error
    PGPI = "PGPi" # ok
    PGPS = "PGPs" #ok
    HIA = "HIA" #ok
    F20 = "F20" #ok
    F30 = "F30" #ok
    PPB = "PPB" #ok
    VD = "VD" #ok
    CYPIA2I = "CYPIA2i" #ok
    CYPIA2S = "CYPIA2s" #ok
    CYP3A4I = "CYP3A4i" #ok
    CYP3A4S = "CYP3A4s" #ok
    CYP2C9I = "CYP2C9i" #ok
    CYP2C9S = "CYP2C9s" #ok
    CYP2C19S = "CYP2C19s" #ok
    CYP2D6I = "CYP2D6i" #ok
    CYP2D6S = "CYP2D6s" #ok
    CL = "CL" #ok
    THALF = "THALF" # error
    HERG = "hERG" # error
    HHT = "HHT" # error
    AMES = "Ames" #ok
    DILI = "DILI" # #ok
    SKINS = "SkinS" #ok


