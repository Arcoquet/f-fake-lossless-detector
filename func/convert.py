import os
import shutil
import ffmpeg

# List of lossy compression formats supported by ffmpeg
# lossyFormat = {
#     "ac3": "ac3",
#     "mp3": "libmp3lame",
#     "opus": "libopus",
#     "wma": "wmav2",
#     "aac": "aac"
# }

# TODO in diff.py, after this, can re-add ac3, aac and wma
lossyFormat = {
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
