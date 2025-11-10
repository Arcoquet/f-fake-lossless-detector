# python 3.12 only
# code in english only


import sys
import soundfile as sf

# python3 main.py /path/to/music.flac
if len(sys.argv) < 2:
    print("Usage: python3 main.py </path/to/music.flac>")
    sys.exit(1)

orgFilePath = sys.argv[1]

# if freq max =16kHz = sus because mp3 max is near
# if freq is 96 but max freq is 21khz, sus
# convert to mp3, acc, and so on and check if same file
# diff % beween input and mp3 convert file