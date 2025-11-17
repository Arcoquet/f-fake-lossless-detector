import os
import ffmpeg

# List of lossy compression formats supported by ffmpeg
lossy_format = {
    "ac3": "ac3",
    "mp3": "libmp3lame",
    "opus": "libopus",
    "wma": "wmav2",
    "aac": "aac"
}


def convert(filepath: str):
    # filepath = /user/truc/desktop/ma musique. de fou.mp3
    list_path = filepath.split("/")
    get_fname = str("".join(list_path[-1].split(".")[:-1]))
    print(get_fname)
    # bonjour.truc.flac

    # Tour of extensions and codecs
    for ext, codec in lossy_format.items():
        output_path = os.path.join("processing", f"{get_fname}.{ext}")
        print(output_path)
        (
            ffmpeg.input(filepath).output(output_path, acodec=codec, vn=None).run()
        )


# convert("test/01 Bohemian Rhapsody (Remastered 2011).flac")
# convert("/Users/vallevert/Desktop/fake-lossless-detector/test/01 Bitch. Lasagna.flac")
