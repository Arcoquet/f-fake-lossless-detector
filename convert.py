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
    list_path = filepath.split("/")
    get_fname = str("".join(list_path[-1]))[::-1].split(".", 1)[1]
    get_fname = get_fname[::-1]
    # print(get_fname)

    for ext, codec in lossy_format.items():
        output_path = os.path.join("processing", f"{get_fname}.{ext}")
        # print(output_path)
        # print(f"output_path={output_path}")
        (
            ffmpeg.input(filepath).output(output_path, acodec=codec, vn=None).run(capture_stdout=True,
                                                                                  capture_stderr=True,
                                                                                  overwrite_output=True)
        )

# convert("test/ext.rait-arist.ochat-devenir-un-cat.wav")
# convert("/Users/vallevert/Desktop/fake-lossless-detector/test/01 Bitch. Lasagna.flac")
# convert("test/01 Bitch. Lasagna.flac")
