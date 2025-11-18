# Python 3.12 only
# Code in english only
# UNIX based file system only (macOS, Linux, ...), but no Windaube !

import sys
import soundfile as sf
import numpy as np
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
from pprint import pprint

from func.container import *
from func.freq import *
from func.convert import *
from func.diff import *

# TODO
# Usage: python3 main.py /path/to/music.flac
# Usage: python3 main.py -d /path/to/musicDir --> will call recursively
# compiled version ?
# .app version ?
# reprendre lecture p117
# calculate information on file, Entropy_flac > Entropy_mp3

if len(sys.argv) < 2:
    print("Usage: python3 main.py /path/to/music.flac")
    sys.exit(1)

colorama_init()
orgFile_Path = sys.argv[1]
orgAudioData, _ = sf.read(orgFile_Path)
redFlagNb: int = 0

maxFrequency: float = findMaxFrequency(orgFile_Path)
if (maxFrequency < 20550.0):
    print(f"{Fore.RED}The maximum frequency is too low{Style.RESET_ALL}")
    redFlagNb += 1

if (containerInfoSampleRate(orgFile_Path) * 0.5 > maxFrequency * 2):
    print(f"{Fore.RED}Container sampling rate is far too high for the signal{Style.RESET_ALL}")
    redFlagNb += 1

if (containerInfoBitRate(orgFile_Path) < 330):
    print(f"{Fore.RED}Bit rate is too low{Style.RESET_ALL}")
    redFlagNb += 1

if ((np.array(orgAudioData)).max() > 1.00):
    print(f"{Fore.RED}Some values are greater than 0 dB{Style.RESET_ALL}")
    redFlagNb += 1

if (isASimilarFormat(orgFile_Path)):
    removeAllConvertedFile(orgFile_Path)
    print(f"{Fore.RED}An other format (codec) is near{Style.RESET_ALL}")
    redFlagNb += 1

if redFlagNb > 0:
    print(f"File: {orgFile_Path}\n"
          f"Red flag number: {Fore.RED}{redFlagNb}{Style.RESET_ALL}")
