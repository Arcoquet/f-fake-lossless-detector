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

from container import *
from freq import *
from convert import *

if len(sys.argv) < 2:
    print("Usage: python3 main.py /path/to/music.flac")
    sys.exit(1)

colorama_init()
orgFile_Path = sys.argv[1]
red_flag_nb: int = 0

maxFrequency: float = findMaxFrequency(orgFile_Path)
if (maxFrequency < 20500.0):
    print(f"{Fore.RED}The maximum frequency is too low{Style.RESET_ALL}")
    red_flag_nb += 1

if (containerInfoSampleRate(orgFile_Path) * 0.5 > maxFrequency * 2):
    print(f"{Fore.RED}Container sampling rate is far too high for the signal{Style.RESET_ALL}")
    red_flag_nb += 1

if (containerInfoBitRate(orgFile_Path) < 330):
    print(f"{Fore.RED}Bit rate is too low{Style.RESET_ALL}")
    red_flag_nb += 1

print(f"Red flag number: {red_flag_nb}")

# diff % between input and mp3 convert file
# calculate information on file, Entropy_flac > Entropy_mp3
