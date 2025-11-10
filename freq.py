import ffmpeg
import soundfile as sf


def getMaxFrequency(filepath: str) -> float:
    file_SF, samplerate = sf.read(filepath)

    leftChannel = [i for i in file_SF[:, 0]]
    rightChannel = [i for i in file_SF[:, 1]]

    return 0.0
