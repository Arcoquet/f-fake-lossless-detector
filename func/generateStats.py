import glob
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

        # print(f"{ext}: signalDifferencePourcentage={signalDifferencePourcentage(orgAudioData, convertedAudioData)}")
        stats_diff[ext].append(signalDifferencePourcentage(orgAudioData, convertedAudioData))
        # print(soundEntropy(orgAudioData, orgSampleRate) - soundEntropy(convertedAudioData, convertedSampleRate))
        stats_entropy[ext].append(
            soundEntropy(orgAudioData, orgSampleRate) - soundEntropy(convertedAudioData, convertedSampleRate))

for ext, codec in lossyFormat.items():
    stats_diff[ext] = np.array(stats_diff[ext])
    stats_entropy[ext] = np.array(stats_entropy[ext])

    print(f"signalDifferencePourcentage: {ext}")
    print(f"mean={stats_diff[ext].mean()}")
    print(f"std={stats_diff[ext].std()}")
    print(f"min={stats_diff[ext].min()}")
    print(f"max={stats_diff[ext].max()}")
    print(f"median={np.median(stats_diff[ext])}")

for ext, codec in lossyFormat.items():
    print(f"soundEntropy: {ext}")
    print(f"mean={stats_entropy[ext].mean()}")
    print(f"std={stats_entropy[ext].std()}")
    print(f"min={stats_entropy[ext].min()}")
    print(f"max={stats_entropy[ext].max()}")
    print(f"median={np.median(stats_entropy[ext])}")
