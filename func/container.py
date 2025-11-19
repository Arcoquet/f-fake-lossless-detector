import ffmpeg
from pprint import pprint


def containerInfo(filepath: str) -> dict:
    # pprint(ffmpeg.probe(filepath)["streams"][0])

    sampleRate: float = float(ffmpeg.probe(filepath)["streams"][0]['sample_rate'])
    bitsPerSample: int = int(ffmpeg.probe(filepath)["streams"][0]['bits_per_sample'])
    codecLongName: str = str(ffmpeg.probe(filepath)["streams"][0]['codec_long_name'])
    bitRate: int = int(ffmpeg.probe(filepath)["streams"][0]['bit_rate'])

    # print(f"sample_rate = {sample_rate}")
    # print(f"bits_per_sample = {bits_per_sample}")
    # print(f"codec_long_name = {codec_long_name}")
    # print(f"bit_rate = {bit_rate}")

    return dict(sampleRate=sampleRate,
                bitsPerSample=bitsPerSample,
                codecLongName=codecLongName,
                bitRate=bitRate
                )


def containerInfoSampleRate(filepath: str) -> int:
    return int(ffmpeg.probe(filepath)["streams"][0]['sample_rate'])


def containerInfoBitRate(filepath: str) -> int:
    """Returns bit rate in kbps (int)"""
    try:
        return int(float(ffmpeg.probe(filepath)["streams"][0]['bit_rate']) * 0.001)
    except:
        return 10000
