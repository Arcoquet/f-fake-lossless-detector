import os
import shutil
import ffmpeg
import numpy as np

losslessFormat: list[str] = ["flac", "m4a", "wav"]

# List of lossy compression formats supported by ffmpeg
lossyFormat: dict[str, str] = {
    "ac3": "ac3",
    "mp3": "libmp3lame",
    "opus": "libopus",
    "wma": "wmav2",
    "aac": "aac"
}

lossyFormatStats: dict[str, list[float]] = {
    "ac3": [0.001, 0.1],
    "mp3": [0.001, 0.1],
    "opus": [0.001, 0.1],
    "wma": [0.001, 0.1],
    "aac": [0.001, 0.1],
}


def convert(filePath: str) -> None:
    try:
        os.mkdir("processing")
    except:
        pass

    listPath = filePath.split("/")
    getFname = str("".join(listPath[-1]))[::-1].split(".", 1)[1][::-1]

    for ext, codec in lossyFormat.items():
        outputPath = os.path.join("processing", f"{getFname}.{ext}")
        (
            ffmpeg.input(filePath)
            .output(outputPath, acodec=codec, vn=None, audio_bitrate="320k", )
            .run(capture_stdout=True, capture_stderr=True, overwrite_output=True)
        )


def removeAllConvertedFile(filePath: str) -> None:
    shutil.rmtree("processing")
    os.mkdir("processing")


def filePathToAudioArray(filePath: str):
    probe = ffmpeg.probe(filePath)
    audioStreams = [s for s in probe["streams"] if s["codec_type"] == "audio"]
    sampleRate = int(audioStreams[0]["sample_rate"])
    channels = int(audioStreams[0]["channels"])

    out, _ = (
        ffmpeg
        .input(filePath)
        .output(
            'pipe:',
            format='s16le',
            acodec='pcm_s16le',
            ac=channels,
            ar=sampleRate
        )
        .run(capture_stdout=True, capture_stderr=True)
    )

    audioData = np.frombuffer(out, dtype=np.int16).astype(np.float32)
    audioData = audioData.reshape(-1, channels)  # re-shape in (samples, channels)
    audioData /= 32768.0

    return audioData, sampleRate
