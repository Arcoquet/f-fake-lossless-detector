import os
import ffmpeg

def convert(filename, output_name):
    # Construire le chemin complet du fichier de sortie
    input_pat = os.path.join("test", filename)
    output_path = os.path.join("convert", output_name)

    # Conversion du fichier avec ffmpeg
    ffmpeg.input(input_pat).output(output_path).run()

convert("extrait-aristochat-devenir-un-cat.wav", "cat.mp3")