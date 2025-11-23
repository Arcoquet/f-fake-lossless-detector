import sys
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
import glob
from func.container import *
from func.freq import *
from func.diff import *
from main import *




lossyFormatStats: dict[str, list[float]] = {
    "ac3": [],
    "mp3": [],
    "opus": [],
    "wma": [],
    "aac": []
}


root: str = "test/Weeknd_flac"
filesPath: list[str] = []
filesPath += glob.glob(root + '/**/*.m4a', recursive=True)
filesPath += glob.glob(root + '/**/*.flac', recursive=True)
filesPath += glob.glob(root + '/**/*.wav', recursive=True)

lst_signalDifferencePourcentage: list[float] = []
lst_entropy: list[float] = []
compt: int = 0
for filePath in filesPath:
    compt += 1
    print(f"Progression: {compt:4}/{len(filesPath)}")
    fileAnalysis(filePath, quiet=False)
