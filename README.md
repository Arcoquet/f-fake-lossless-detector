# fake-lossless-detector

## First install libraries

### macOS

```bash
pip install ffmpeg-python==0.2.0;
pip install numpy==2.3.5 colorama==0.4.6 soundfile==0.13.1 scipy==1.16.3;
```

### Linux-based

```bash
pip install ffmpeg==1.4;
pip install numpy==2.3.5 colorama==0.4.6 soundfile==0.13.1 scipy==1.16.3;
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