from func.convert import *
from scipy.stats import entropy
import soundfile as sf
import numpy as np
import soundfile as sf
from scipy.signal import stft


def signalDifferencePourcentage(filePathOrg: str, filePathConverted: str) -> float:
    """Takes two filepath (relative or absolute), reads both, put it into 2 arrays (sf.read())
    Then calculates the pourcentage of difference between two arrays.
    :return float: pourcentage of difference between two arrays"""

    # TODO /Doc/diff().jpeg
    # TODO Armand

    return 0.0


def soundEntropy(filePath: str,
                 nFft: int = 2048,
                 hop: int = 512,
                 window: str = 'hann',
                 base: float = 2.0,
                 eps: float = 1e-12) -> float:
    """
    Compute mean spectral entropy (bits by default) of an audio file.

    Parameters:
      filePath: path to audio file
      nFft: FFT size (frame length)
      hop: hop length (nFft - noverlap)
      window: window type for STFT
      base: log base (2 for bits)
      eps: small constant to avoid log(0)

    Returns:
      mean spectral entropy across frames
    """
    x, sr = sf.read(filePath)
    if x.ndim > 1:
        x = x.mean(axis=1)
    f, t, Z = stft(x, fs=sr, window=window, nperseg=nFft, noverlap=nFft - hop, padded=False, boundary=None)
    S = np.abs(Z)  # magnitude spectrogram (freq bins x frames)

    # sum per frame
    frameEnergy = S.sum(axis=0)
    valid = frameEnergy > eps
    if not np.any(valid):
        return 0.0

    # normalize to probability distribution per frame
    P = S[:, valid] / (frameEnergy[valid] + eps)

    # compute entropy per frame
    HFrames = -np.sum(P * np.log(P + eps), axis=0) / np.log(base)

    # return mean entropy (you can return median or per-frame array instead)
    return float(np.mean(HFrames))


# print(soundEntropy(
#     "/Volumes/ExtSSD/Users/Vallevert/Desktop/fake-lossless-detector/test/03 Barbie Girl.flac") / soundEntropy(
#     "/Volumes/ExtSSD/Users/Vallevert/Desktop/fake-lossless-detector/test/03 Barbie Girl.mp3"))


def isASimilarCodec(filePathOrg: str) -> bool:
    # TODO Armand if extenxion=ac3, sf can't read it, use another lib
    listPath = filePathOrg.split("/")
    getFname = str("".join(listPath[-1]))[::-1].split(".", 1)[1][::-1]

    for ext, codec in lossyFormat.items():
        outputPath = os.path.join("processing", f"{getFname}.{ext}")
        if (signalDifferencePourcentage(filePathOrg, outputPath) > 0.98):  # TODO Armand find this constant
            return True

    return False


def isASimilarInformation(filePathOrg: str) -> bool:
    # information = entropy
    listPath = filePathOrg.split("/")
    getFname = str("".join(listPath[-1]))[::-1].split(".", 1)[1][::-1]

    for ext, codec in lossyFormat.items():
        outputPath = os.path.join("processing", f"{getFname}.{ext}")

        if (not (soundEntropy(filePathOrg) > soundEntropy(outputPath) * 1.015)):
            return False

    return True
