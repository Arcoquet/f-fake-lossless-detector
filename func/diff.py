from func.convert import *
import numpy as np
from scipy.signal import stft


def signalDifferencePourcentage(orgAudioData: list[float], convertedAudioData: list[float]) -> float:
    """Takes two audio array, calculates the difference between two arrays.
    :return float: difference between two arrays"""

    orgAudioData = np.array(orgAudioData)
    convertedAudioData = np.array(convertedAudioData)

    # Mono conversion
    if orgAudioData.ndim > 1:
        orgAudioData = np.mean(orgAudioData, axis=1)
    if convertedAudioData.ndim > 1:
        convertedAudioData = np.mean(convertedAudioData, axis=1)

    min_len = min(len(orgAudioData), len(convertedAudioData))
    orgAudioData = orgAudioData[:min_len]
    convertedAudioData = convertedAudioData[:min_len]

    # Normalisation due to lossy codec being above 0 dB
    orgAudioData = orgAudioData / np.max(np.abs(orgAudioData))
    convertedAudioData = convertedAudioData / np.max(np.abs(convertedAudioData))

    diff = np.abs(orgAudioData - convertedAudioData)

    percent = np.mean(diff)
    return percent


def soundEntropy(audioData: list[float],
                 sampleRate: int,
                 nFft: int = 2048,
                 hop: int = 512,
                 window: str = 'hann',
                 base: float = 2.0,
                 eps: float = 1e-12) -> float:
    """
    Compute mean spectral entropy (bits by default) of an audio file.

    Parameters:
      audioData: audio data list float
      sampleRate: audio sample rate
      nFft: FFT size (frame length)
      hop: hop length (nFft - noverlap)
      window: window type for STFT
      base: log base (2 for bits)
      eps: small constant to avoid log(0)

    Returns:
      mean spectral entropy across frames
    """
    audioData = np.array(audioData)
    if audioData.ndim > 1:
        audioData = audioData.mean(axis=1)
    f, t, Z = stft(audioData,
                   fs=sampleRate, window=window,
                   nperseg=nFft, noverlap=nFft - hop, padded=False,
                   boundary=None)
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


def isASimilarCodec(orgFilePath: str, orgAudioData: list[float]) -> bool:
    listPath = orgFilePath.split("/")
    getFname = str("".join(listPath[-1]))[::-1].split(".", 1)[1][::-1]

    for ext, codec in lossyFormat.items():
        convertedPath = os.path.join("processing", f"{getFname}.{ext}")
        convertedAudioData, _ = filePathToAudioArray(convertedPath)

        print(signalDifferencePourcentage(orgAudioData, convertedAudioData))
        if signalDifferencePourcentage(orgAudioData, convertedAudioData) > lossyFormatStats[ext][0]:  # TODO
            return True
    return False


def isASimilarInformation(orgFilePath: str, orgAudioData: list[float], orgSampleRate: int) -> bool:
    # information = entropy
    listPath = orgFilePath.split("/")
    getFname = str("".join(listPath[-1]))[::-1].split(".", 1)[1][::-1]

    for ext, codec in lossyFormat.items():
        convertedPath = os.path.join("processing", f"{getFname}.{ext}")
        convertedAudioData, convertedSampleRate = filePathToAudioArray(convertedPath)

        print(soundEntropy(orgAudioData, orgSampleRate) - soundEntropy(convertedAudioData, convertedSampleRate))

        if not (soundEntropy(orgAudioData, orgSampleRate) -
                soundEntropy(convertedAudioData, convertedSampleRate) > lossyFormatStats[ext][1]):  # TODO
            return False

    return True
