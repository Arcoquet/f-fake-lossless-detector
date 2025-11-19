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

if len(sys.argv) < 2:
    print("Usage: python3 main.py /path/to/music.flac")
    sys.exit(1)
orgFilePath = sys.argv[1]

colorama_init()
orgAudioData, _ = sf.read(orgFilePath)
redFlagNb: int = 0

# Detects MP3 20.5kHz cut-off
maxFrequency: float = findMaxFrequency(orgFilePath)
if (maxFrequency < 20550.0):
    print(f"{Fore.RED}The maximum frequency is too low{Style.RESET_ALL}")
    redFlagNb += 1

# Detects if max encoded frequency is far less than max container capability (20.5 kHz Mp3 to 96 kHz Flac)
if (containerInfoSampleRate(orgFilePath) * 0.5 > maxFrequency * 2):
    print(f"{Fore.RED}Container sampling rate is far too high for the signal{Style.RESET_ALL}")
    redFlagNb += 1

# Detects if bit rate is too low for lossless
if (containerInfoBitRate(orgFilePath) < 330):
    print(f"{Fore.RED}Bit rate is too low{Style.RESET_ALL}")
    redFlagNb += 1

# Detects saturated values
if ((np.array(orgAudioData)).max() > 1.00):
    print(f"{Fore.RED}Some values are greater than 0 dB{Style.RESET_ALL}")
    redFlagNb += 1

# Detects if another codec is near
convert(orgFilePath)
if (isASimilarCodec(orgFilePath)):
    print(f"{Fore.RED}Another lossy codec is near{Style.RESET_ALL}")
    redFlagNb += 1

# Detects if information is greater than other codecs
if (not isASimilarInformation(orgFilePath)):
    print(f"{Fore.RED}No quality loss found in others converted codecs{Style.RESET_ALL}")
    redFlagNb += 1

# Clean up files
removeAllConvertedFile(orgFilePath)

# Print result
if redFlagNb > 0:
    print(f"File: {orgFilePath}\n"
          f"Red flag number: {Fore.RED}{redFlagNb}{Style.RESET_ALL}")
print("Red flag number should be 6 for MP3, and 0 for FLAC")
