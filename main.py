# python 3.12 only
# code in english only


import sys

# python3 main.py /path/to/music.flac
if len(sys.argv) < 2:
    print("Usage: python3 main.py </path/to/music.flac>")
    sys.exit(1)

arg = sys.argv[1]
print("Argument:", arg)
