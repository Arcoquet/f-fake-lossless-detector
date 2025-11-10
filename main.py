# python 3.12 only
# code in english only
# UNIX based file system only
import sys
import soundfile as sf
import numpy as np

from freq import *

if len(sys.argv) < 2:
    print("Usage: python3 main.py </path/to/music.flac>")
    sys.exit(1)

orgFile_Path = sys.argv[1]
orgFile_SF, samplerate = sf.read(orgFile_Path)
# print(data[samplerate*60]) = 60s'sample

(getMaxFrequency(orgFile_Path))

# if freq max=16kHz = sus because mp3 max is near
# if freq is 96 but max freq is 21khz, sus
# convert to mp3, acc, and so on and check if same file
# diff % between input and mp3 convert file

# return a score of probably fake lossless
