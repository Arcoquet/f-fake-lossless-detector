import os

import ffmpeg

# List of lossy compression formats supported by ffmpeg
# lossyFormat = {
#     "ac3": "ac3",
#     "mp3": "libmp3lame",
#     "opus": "libopus",
#     "wma": "wmav2",
#     "aac": "aac"
# }
# TODO in diff.py, after this, can re-add ac3
lossyFormat = {
    "mp3": "libmp3lame",
    "opus": "libopus",
    "wma": "wmav2",
    "aac": "aac"
}


def convert(filePath: str):
    listPath = filePath.split("/")
    getFname = str("".join(listPath[-1]))[::-1].split(".", 1)[1][::-1]

    for ext, codec in lossyFormat.items():
        outputPath = os.path.join("processing", f"{getFname}.{ext}")
        (
            ffmpeg.input(filePath).output(outputPath, acodec=codec, vn=None).run(capture_stdout=True,
                                                                                 capture_stderr=True,
                                                                                 overwrite_output=True)
        )


def removeAllConvertedFile(filePath: str) -> None:
    # TODO Armand, BE CAREFULL
    pass

# convert("test/ext.rait-arist.ochat-devenir-un-cat.wav")
# convert("/Users/vallevert/Desktop/fake-lossless-detector/test/01 Bitch. Lasagna.flac")
# convert("test/01 Bitch. Lasagna.flac")
