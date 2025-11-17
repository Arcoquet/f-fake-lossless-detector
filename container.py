import ffmpeg
import ffmpeg
import sys
from pprint import pprint  # for printing Python dictionaries in a human-readable way


def containerInfo(filepath: str):
    # pprint(ffmpeg.probe(filepath)["streams"][0])

    sample_rate: float = ffmpeg.probe(filepath)["streams"][0]['sample_rate']
    bits_per_sample = ffmpeg.probe(filepath)["streams"][0]['bits_per_sample']
    codec_long_name = ffmpeg.probe(filepath)["streams"][0]['codec_long_name']
    bit_rate = ffmpeg.probe(filepath)["streams"][0]['bit_rate']
    # print(f"sample_rate = {sample_rate}")
    # print(f"bits_per_sample = {bits_per_sample}")
    # print(f"codec_long_name = {codec_long_name}")
    # print(f"bit_rate = {bit_rate}")

    return dict(sample_rate=sample_rate,
                bits_per_sample=bits_per_sample,
                codec_long_name=codec_long_name,
                bit_rate=float(bit_rate) * 0.001
                )

# containerInfo("test/01 Bitch Lasagna.flac")
# containerInfo("/Users/vallevert/Desktop/fake-lossless-detector/test/son_pure_440_22050_3_1.wav")
