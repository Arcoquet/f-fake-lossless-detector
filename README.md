# fake-lossless-detector

## First install libraries

### <b>Python 3.12 only.</b>

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

# Limitations

This project contains some limitations:

- only `flac`, `m4a` and `wav` are available as input file format
- only `mp3`, `ac3`, `opus`, `wma` and `aac` are available in audio codec conversion comparaison
- Why ? Other files formats are rare nowadays, and I don't care about them
- No way to pass an argument `-q --quiet` to display or remove red flag details
- no Windows, but who care ?