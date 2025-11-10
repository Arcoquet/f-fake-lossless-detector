import ffmpeg
import soundfile as sf
from scipy import signal
from scipy.io import wavfile
import numpy as np


def getMaxFrequency(filepath: str) -> float:
    file_SF, samplerate = sf.read(filepath)
    duration: float = file_SF.shape[0] / samplerate

    try:
        leftChannel = [i for i in file_SF[:, 0]]
        rightChannel = [i for i in file_SF[:, 1]]
    except:  # for mono music
        leftChannel = [i for i in file_SF[:]]

    fft_samples = np.abs(np.fft.fft(leftChannel))

    peak_index = np.argmax(fft_samples)  # get indices of the largest amplitude
    max_frequency = peak_index / (len(leftChannel)) * samplerate

    print(f"""Maximum frequency: {str(max_frequency)} Hz""")

    return max_frequency


# python max frequency of a sound
# https://stackoverflow.com/questions/75286292/get-maximum-of-spectrum-from-audio-file-with-python-audacity-like