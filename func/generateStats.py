import sys
import glob
from func.container import *
from func.freq import *
from func.diff import *
from func.convert import *

root: str = "/Volumes/ExtSSD/Users/Vallevert/Desktop/fake-lossless-detector/test/Weeknd_flac"
filesPath: list[str] = []
filesPath += glob.glob(root + '/**/*.m4a', recursive=True)
filesPath += glob.glob(root + '/**/*.flac', recursive=True)
filesPath += glob.glob(root + '/**/*.wav', recursive=True)

lst_signalDifferencePourcentage: list[float] = []
lst_entropy: list[float] = []
compt: int = 0

stats_diff: dict[str, list[float]] = {
    "ac3": [],
    "mp3": [],
    "opus": [],
    "wma": [],
    "aac": []
}

stats_entropy: dict[str, list[float]] = {
    "ac3": [],
    "mp3": [],
    "opus": [],
    "wma": [],
    "aac": []
}

# Convert
for filePath in filesPath:
    compt += 1
    print(f"Progression: {compt:4}/{len(filesPath)}")
    orgAudioData, orgSampleRate = filePathToAudioArray(filePath)
    # fileAnalysis(filePath, quiet=False)
    # convert(filePath)

    for ext, codec in lossyFormat.items():
        listPath = filePath.split("/")
        getFname = str("".join(listPath[-1]))[::-1].split(".", 1)[1][::-1]
        convertedPath = os.path.join("processing", f"{getFname}.{ext}")
        convertedAudioData, convertedSampleRate = filePathToAudioArray(convertedPath)

        print(f"{ext}: signalDifferencePourcentage={signalDifferencePourcentage(orgAudioData, convertedAudioData)}")

    # lst_signalDifferencePourcentage.append(signalDifferencePourcentage(orgAudioData, convAudioData))
    # lst_entropy.append(soundEntropy(orgAudioData, sr1) - soundEntropy(convAudioData, sr2))

# lst_signalDifferencePourcentage = np.array(lst_signalDifferencePourcentage)
# print(lst_signalDifferencePourcentage.mean(axis=0))  #  0.002513323
# print(lst_signalDifferencePourcentage.std(axis=0))  #   0.0025298814
# print(lst_signalDifferencePourcentage.min())  #         0.00067599147
# print(lst_signalDifferencePourcentage.max())  #         0.012584871
# print(np.median(lst_signalDifferencePourcentage))  #    0.0018073984

# lst_entropy = np.array(lst_entropy)
# print(lst_entropy.mean(axis=0))  #  0.01683380437552589
# print(lst_entropy.std(axis=0))  #   0.008066497593942346
# print(lst_entropy.min())  #         0.00038740892301536434
# print(lst_entropy.max())  #         0.04890216027699257
# print(np.median(lst_entropy))  #    0.01564887940118087
