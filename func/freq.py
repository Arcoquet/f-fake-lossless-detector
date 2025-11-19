import numpy as np
import soundfile as sf
from scipy.fft import fft, fftfreq


def findMaxFrequency(audioData: list[float], sampleRate: int, thresholdDb: float = -90.0) -> float:
    # Convert to mono if stereo
    if audioData.ndim > 1:
        audioData = audioData.mean(axis=1)

    # Use a few seconds only (faster and enough)
    audioData = audioData[: sampleRate * 3]

    N = len(audioData)

    # Hann window
    window = audioData * np.hanning(N)

    # FFT
    spectrum = np.abs(fft(window))
    freqs = fftfreq(N, 1 / sampleRate)

    # Positive frequencies only
    mask = freqs >= 0
    freqs = freqs[mask]
    spectrum = spectrum[mask]

    # Convert magnitude to dB
    spectrum_db = 20 * np.log10(spectrum / np.max(spectrum))

    # Find frequencies above threshold (e.g., -40 dB)
    valid = np.where(spectrum_db > thresholdDb)[0]

    if len(valid) == 0:
        return 0.0

    max_freq = freqs[valid[-1]]

    return float(max_freq)
