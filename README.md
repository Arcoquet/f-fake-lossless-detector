# fake-lossless-detector

## First install libraries

### macOS

```bash
pip install ffmpeg-python==0.2.0 numpy colorama soundfile pprint scipy;
```

### Linux-based

```bash
pip install ffmpeg numpy colorama soundfile pprint scipy;
```

## How to run

For a single music file:

```bash
python3 main.py /path/to/music.flac
```

For a folder (recursive):

```bash
python3 main.py -d /path/to/musicDir
```