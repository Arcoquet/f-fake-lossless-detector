import os
import ffmpeg

# List of lossy compression formats supported by ffmpeg
lossy_format = {
    "ac3":  "ac3",
    "mp3":  "libmp3lame",
    "opus": "libopus",
    "wma":  "wmav2",
    "aac":  "aac",
    "m4a":  "aac"
}

def convert(filename):
    fname, _ = os.path.splitext(filename)
    input_path = os.path.join("test", filename)

    # Tour of extensions and codecs
    for ext, codec in lossy_format.items():

        output_path = os.path.join("processing", f"{fname}.{ext}")
        (
            ffmpeg.input(input_path).output(output_path, acodec=codec, vn=None).run()
        )

# convert("01 Bitch Lasagna.flac")
