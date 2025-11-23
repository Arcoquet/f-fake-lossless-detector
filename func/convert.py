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

# [[diff mean, diff std], [entropy mean, entropy std]]
lossyFormatStats: dict[str, list] = {
    "ac3": [[0.2999180555343628, 0.06330308318138123], [2.5645503283655557e-05]],
    "mp3": [[0.0025133229792118073, 0.002529881428927183], [0.00038740892301536434]],
    "opus": [[0.28965553641319275, 0.05666084215044975], [0.09653195264480274]],
    "wma": [[0.27840492129325867, 0.06375496089458466], [0.00011512780879119333]],
    "aac": [[0.2546287775039673, 0.05744258686900139], [0.0067861002225546585]]
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
