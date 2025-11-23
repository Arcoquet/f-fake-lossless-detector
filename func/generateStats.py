import glob
from func.diff import *
from func.convert import *


def generateStats() -> None:
    root: str = "/Volumes/ExtSSD/Users/Vallevert/Desktop/fake-lossless-detector/test/Weeknd_flac"
    filesPath: list[str] = []
    filesPath += glob.glob(root + '/**/*.m4a', recursive=True)
    filesPath += glob.glob(root + '/**/*.flac', recursive=True)
    filesPath += glob.glob(root + '/**/*.wav', recursive=True)
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

            # stats_diff[ext].append(signalDifferencePourcentage(orgAudioData, convertedAudioData))
            stats_entropy[ext].append(
                soundEntropy(orgAudioData, orgSampleRate) - soundEntropy(convertedAudioData, convertedSampleRate))

    print("\n" * 25)

    for ext, codec in lossyFormat.items():
        stats_diff[ext] = np.array(stats_diff[ext])

        print(f"signalDifferencePourcentage: {ext}")
        print(f"\tmean={stats_diff[ext].mean()}")
        print(f"\tstd={stats_diff[ext].std()}")
        print(f"\tmedian={np.median(stats_diff[ext])}")
        print(f"\tmin={stats_diff[ext].min()}")
        print(f"\tmax={stats_diff[ext].max()}")

    for ext, codec in lossyFormat.items():
        stats_entropy[ext] = np.array(stats_entropy[ext])
        stats_entropy[ext][1] = abs(stats_entropy[ext][1])

        print(f"soundEntropy: {ext}")
        print(f"\tmean={stats_entropy[ext].mean()}")
        print(f"\tstd={stats_entropy[ext].std()}")
        print(f"\tmedian={np.median(stats_entropy[ext])}")
        print(f"\tmin={stats_entropy[ext].min()}")
        print(f"\tmax={stats_entropy[ext].max()}")


generateStats()
