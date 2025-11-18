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

# TODO
# Usage: python3 main.py /path/to/music.flac
# Usage: python3 main.py -d /path/to/musicDir --> will call recursively

if len(sys.argv) < 2:
    print("Usage: python3 main.py /path/to/music.flac")
    sys.exit(1)

colorama_init()
orgFile_Path = sys.argv[1]
orgAudioData, _ = sf.read(orgFile_Path)
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

# Clipping p111
if ((np.array(orgAudioData)).max() > 1.00):
    print(f"{Fore.RED}Some values are greater than 0 dB{Style.RESET_ALL}")
    red_flag_nb += 1

print(f"Red flag number: {Fore.RED}{red_flag_nb}{Style.RESET_ALL}")

# reprendre lecture p114
# diff % between input and mp3 convert file
# calculate information on file, Entropy_flac > Entropy_mp3
