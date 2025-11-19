from func.convert import *
from scipy.stats import entropy
import soundfile as sf
import numpy as np
from scipy.spatial.distance import cosine
from scipy.signal import stft


def signalDifferencePourcentage(orgAudioData: list[float], convertedAudioData: list[float]) -> float:
    """Takes two filepath (relative or absolute), reads both, put it into 2 arrays (sf.read())
    Then calculates the pourcentage of difference between two arrays.
    :return float: pourcentage of difference between two arrays"""

    # TODO /Doc/diff().jpeg

    data1, sr1 = sf.read(filePathOrg)
    data2, sr2 = sf.read(filePathConverted)

    if sr1 != sr2:
        raise ValueError("Sample rates differ")

    # Mono conversion
    if data1.ndim > 1:
        data1 = np.mean(data1, axis=1)
    if data2.ndim > 1:
        data2 = np.mean(data2, axis=1)

    min_len = min(len(data1), len(data2))
    data1 = data1[:min_len]
    data2 = data2[:min_len]

    data1 = data1 / np.max(np.abs(data1))
    data2 = data2 / np.max(np.abs(data2))

    diff = np.abs(data1 - data2)

    similarity = np.mean(diff) * 100
    
    return similarity

def soundEntropy(filePath: str,
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
        outputPath = os.path.join("processing", f"{getFname}.{ext}")
        if (signalDifferencePourcentage(filePathOrg, outputPath) > 0.9998):  # TODO Constant to find
        covertedPath = os.path.join("processing", f"{getFname}.{ext}")
        convertedAudioData, _ = filePathToAudioArray(covertedPath)

        if signalDifferencePourcentage(orgAudioData, convertedAudioData) > 0.985:  # TODO Armand find this constant.
            return True
    return False


def isASimilarInformation(orgFilePath: str, orgAudioData: list[float], orgSampleRate: int) -> bool:
    # information = entropy
    listPath = orgFilePath.split("/")
    getFname = str("".join(listPath[-1]))[::-1].split(".", 1)[1][::-1]

    for ext, codec in lossyFormat.items():
        covertedPath = os.path.join("processing", f"{getFname}.{ext}")
        convertedAudioData, convertedSampleRate = filePathToAudioArray(covertedPath)

        if not (soundEntropy(orgAudioData, orgSampleRate) >
                soundEntropy(convertedAudioData, convertedSampleRate)
                * 1.015):  # TODO flac2flac=1, flac2mp3=1.015
            return False

    return True
