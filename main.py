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

from container import containerInfo, containerInfoSampleRate
from freq import *
from convert import *

# To use color in print()
colorama_init()

if len(sys.argv) < 2:
    print("Usage: python3 main.py /path/to/music.flac")
    sys.exit(1)

orgFile_Path = sys.argv[1]
# orgFile_SF, samplerate = sf.read(orgFile_Path)
# print(data[samplerate*60]) = 60s'sample

maxFrequency: float = findMaxFrequency(orgFile_Path)
# print(f"Maximum frequency found: {maxFrequency * 0.001:.1f} kHz")
if (maxFrequency < 20050.0):
    print(f"{Fore.RED}The maximum frequency is too low to be lossless{Style.RESET_ALL}")

if (containerInfoSampleRate(orgFile_Path) * 0.5 > maxFrequency * 2):
    # print(f"\tmaxFrequency={maxFrequency}")
    # print(f"\tcontainer sample rate={containerInfoSampleRate(orgFile_Path) * 0.5}")
    print(f"{Fore.RED}Container sampling rate is far too high for the signal{Style.RESET_ALL}")

# diff % between input and mp3 convert file

# return a score of probably fake lossless
