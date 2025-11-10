import ffmpeg
import soundfile as sf


def getMaxFrequency(filepath: str) -> float:
    file_SF, samplerate = sf.read(filepath)
    duration: float = file_SF.shape[0] / samplerate

    leftChannel = [i for i in file_SF[:, 0]]
    rightChannel = [i for i in file_SF[:, 1]]

    from scipy import signal
    from scipy.io import wavfile
    import numpy as np

    sample_rate, samples = wavfile.read('/Users/vallevert/Desktop/lossy-detector/test/03 Barbie Girl.wav')
    fft_samples = np.abs(np.fft.fft(samples))

    peak_index = np.argmax(fft_samples)  # get indices of the largest amplitude
    max_frequency = peak_index / (len(samples)) * sample_rate

    print(
        f"""
        Frequency index where the maximum is:
        {peak_index}

        Maximum Frequency:
        {str(max_frequency)} Hz

        Frequency Value:
        {fft_samples[peak_index]} 

        Frequency Value once again (should be the same if our calculations were right):
        {np.max(fft_samples)}
        """
    )

    return 0.0
