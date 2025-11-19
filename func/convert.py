import os
import shutil
import ffmpeg
import soundfile as sf

losslessFormat: list[str] = ["flac", "m4a", "wav"]

# List of lossy compression formats supported by ffmpeg
# lossyFormat: dict[str, str]  = {
#     "ac3": "ac3",
#     "mp3": "libmp3lame",
#     "opus": "libopus",
#     "wma": "wmav2",
#     "aac": "aac"
# }

# TODO Armand see filePathToAudioArray()
lossyFormat: dict[str, str] = {
    "mp3": "libmp3lame",
    "opus": "libopus",
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
            .output(outputPath, acodec=codec, vn=None)
            .run(capture_stdout=True, capture_stderr=True, overwrite_output=True)
        )


def removeAllConvertedFile(filePath: str) -> None:
    shutil.rmtree("processing")
    os.mkdir("processing")


def filePathToAudioArray(filePath: str):
    # TODO Armand if format not supported by SF, use another lib
    audioData, sampleRate = sf.read(filePath)
    return audioData, sampleRate
