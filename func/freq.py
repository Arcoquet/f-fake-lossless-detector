import numpy as np
import soundfile as sf
from scipy.fft import fft, fftfreq


def findMaxFrequency(filepath: str, threshold_db: float = -90.0) -> float:
    audio, sr = sf.read(filepath)

    # Convert to mono if stereo
    if audio.ndim > 1:
        audio = audio.mean(axis=1)

    # Use a few seconds only (faster and enough)
    audio = audio[: sr * 3]

    N = len(audio)

    # Hann window
    window = audio * np.hanning(N)

    # FFT
    spectrum = np.abs(fft(window))
    freqs = fftfreq(N, 1 / sr)

    # Positive frequencies only
    mask = freqs >= 0
    freqs = freqs[mask]
    spectrum = spectrum[mask]

    # Convert magnitude to dB
    spectrum_db = 20 * np.log10(spectrum / np.max(spectrum))

    # Find frequencies above threshold (e.g., -40 dB)
    valid = np.where(spectrum_db > threshold_db)[0]

    if len(valid) == 0:
        return 0.0

    max_freq = freqs[valid[-1]]

    return float(max_freq)
