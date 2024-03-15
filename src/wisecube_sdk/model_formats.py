from enum import Enum
import pandas as pd


class WisecubeModel(Enum):
    BBB = "BBB"
    LOGS = "logS"
    CYP2CI9I = "CYP2CI9i"
    LOGD7 = "LogD7"
    PGPI = "PGPi"
    PGPS = "PGPs"
    HIA = "HIA"
    F20 = "F20"
    F30 = "F30"
    PPB = "PPB"
    VD = "VD"
    CYPIA2I = "CYPIA2i"
    CYPIA2S = "CYPIA2s"
    CYP3A4I = "CYP3A4i"
    CYP3A4S = "CYP3A4s"
    CYP2C9I = "CYP2C9i"
    CYP2C9S = "CYP2C9s"
    CYP2C19S = "CYP2C19s"
    CYP2D6I = "CYP2D6i"
    CYP2D6S = "CYP2D6s"
    CL = "CL"
    AMES = "Ames"
    DILI = "DILI"
    SKINS = "SkinS"
    CACO2 = "Caco2"
    THALF = "THALF"
    HERG = "hERG"
    HHT = "HHT"


class OutputFormat(Enum):
    JSON = "JSON"
    PANDAS = "PANDAS"
