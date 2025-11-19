# Python 3.12 only
# Code in english only
# UNIX-based file system only (macOS, Linux, ...)

import sys
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
import glob
from func.container import *
from func.freq import *
from func.diff import *

colorama_init()
blueTab: str = f"{Fore.LIGHTBLUE_EX}|\t{Style.RESET_ALL}"


def fileAnalysis(orgFilePath: str, quiet: bool = True) -> int:
    if not quiet:
        print(f"{Fore.LIGHTBLUE_EX}{orgFilePath}{Style.RESET_ALL}")

    orgAudioData, orgSampleRate = filePathToAudioArray(orgFilePath)
    redFlagNb: int = 0

    # Detection methods ------------------------------------------------------------------------------------------------

    # Detects MP3 20.5kHz cut-off
    maxFrequency: float = findMaxFrequency(orgFilePath)
    if maxFrequency < 20550.0:
        if not quiet:
            print(f"{blueTab + Fore.YELLOW}The maximum frequency is too low{Style.RESET_ALL}")
        redFlagNb += 1

    # Detects if max encoded frequency is far less than max container capability (20.5 kHz Mp3 to 96 kHz Flac)
    if containerInfoSampleRate(orgFilePath) * 0.5 > maxFrequency * 2:
        if not quiet:
            print(f"{blueTab + Fore.YELLOW}Container sampling rate is far too high for the signal{Style.RESET_ALL}")
        redFlagNb += 1

    # Detects if bit rate is too low for lossless
    if containerInfoBitRate(orgFilePath) < 330:
        if not quiet:
            print(f"{blueTab + Fore.YELLOW}Bit rate is too low{Style.RESET_ALL}")
        redFlagNb += 1

    # Detects saturated values
    if (np.array(orgAudioData)).max() > 1.00:
        if not quiet:
            print(f"{blueTab + Fore.YELLOW}Some values are greater than 0 dB{Style.RESET_ALL}")
        redFlagNb += 1

    # Detects if another codec is near
    convert(orgFilePath)
    if isASimilarCodec(orgFilePath, orgAudioData):
        if not quiet:
            print(f"{blueTab + Fore.YELLOW}Another lossy codec is near{Style.RESET_ALL}")
        redFlagNb += 1

    # Detects if information is greater than other codecs
    if not isASimilarInformation(orgFilePath, orgAudioData, orgSampleRate):
        if not quiet:
            print(f"{blueTab + Fore.YELLOW}No quality loss found in others converted codecs{Style.RESET_ALL}")
        redFlagNb += 1

    # Clean up files  --------------------------------------------------------------------------------------------------
    removeAllConvertedFile(orgFilePath)

    # Print info  ------------------------------------------------------------------------------------------------------
    if not quiet:
        print(f"{blueTab}redFlagNb={Fore.YELLOW}{redFlagNb}{Style.RESET_ALL}")

    if redFlagNb >= 2:
        print(
            f"{Fore.RED}⚠️ \033[4m{orgFilePath}{Style.RESET_ALL + Fore.RED} is suspect "
            f"({redFlagNb} reds flags) ⚠️{Style.RESET_ALL}")

    # print("TODO: redFlagNb should be 6 for MP3, and 0 for FLAC")

    return redFlagNb


arg: list[str] = sys.argv[1:]

if len(arg) > 2 or len(arg) < 1:
    print(f"{Fore.RED}Usage: python3 main.py /path/to/music.flac\n"
          f"Usage: python3 main.py -d /path/to/musicDir{Style.RESET_ALL}")
    sys.exit(1)

# One file
if len(arg) == 1:
    fileAnalysis(arg[0], quiet=False)

# Folder: multiple files
if len(arg) == 2:
    root: str = arg[1]
    filesPath: list[str] = []
    filesPath += glob.glob(root + '/**/*.m4a', recursive=True)
    filesPath += glob.glob(root + '/**/*.flac', recursive=True)
    filesPath += glob.glob(root + '/**/*.wav', recursive=True)

    compt: int = 0
    for filePath in filesPath:
        compt += 1
        print(f"Progression: {compt}/{len(filesPath)}")
        fileAnalysis(filePath, quiet=False)
