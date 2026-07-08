"""
Uses environment_files/julius_environment.yaml
"""
import shutil

import soundfile as sf
import os
import sys

from pyjuliusalign import alignFromTextgrid

if sys.platform == 'win32':
    root_dir = r"D:\Data\experiments\interspeech_benchmarking"
    temp_dir = r"D:\Data\experiments\interspeech_benchmarking\temp"

    corpus_directories = {
        "csj": r"D:\Data\speech\benchmark_datasets\csj\csj_lab",
    }
    juliusScriptPath = r"/home/micha/downloads/segmentation-kit/segment_julius.pl"
    soxPath = "sox"
    cabochaPath = "cabocha"
    perlPath = "perl"
else:
    root_dir = r"/mnt/d/Data/experiments/interspeech_benchmarking"
    temp_dir = r"/mnt/d/Data/experiments/interspeech_benchmarking/temp"

    corpus_directories = {
        "csj": r"/mnt/d/Data/speech/benchmark_datasets/csj/csj_lab",
    }
    juliusScriptPath = "/home/micha/downloads/segmentation-kit/segment_julius.pl"
    soxPath = "sox"
    cabochaPath = "cabocha"
    perlPath = "perl"

cabochaEncoding = "utf-8"  # "utf-8" is nice if possible


if __name__ == "__main__":

    for corpus, root in corpus_directories.items():
        output_directory = os.path.join(root_dir, "alignments", corpus, "julius")
        for speaker in os.listdir(root):
            speaker_directory = os.path.join(root, speaker)
            output_speaker_directory = os.path.join(output_directory, speaker)
            os.makedirs(output_speaker_directory, exist_ok=True)
            speaker_temp = os.path.join(temp_dir, speaker)
            os.makedirs(speaker_temp, exist_ok=True)
            cabochaOutput = os.path.join(speaker_temp, "cabocha_output")
            for f in os.listdir(speaker_directory):
                if not f.endswith(".wav"):
                     continue
                audio_path = os.path.join(speaker_directory, f)
                text_path = os.path.join(speaker_directory, f.replace(".wav", ".txt"))
                output_path = os.path.join(output_speaker_directory, f.replace(".wav", ".TextGrid"))
                if not os.path.exists(text_path):
                    text_path = text_path.replace(".txt", ".lab")
                temp_wav_path = os.path.join(speaker_temp, f)
                if not os.path.exists(temp_wav_path):
                    shutil.copyfile(audio_path, temp_wav_path)
                temp_text_path = os.path.join(speaker_temp, f.replace(".wav", ".txt"))
                if not os.path.exists(temp_text_path):
                    info = sf.info(audio_path)
                    with open(text_path, encoding='utf8') as inf:
                        text = inf.read().strip()
                    with open(temp_text_path, 'w', encoding='utf8') as outf:
                        outf.write(f"0.0,{info.duration},{text}")

            alignFromTextgrid.convertCorpusToKanaAndRomaji(
                inputPath=speaker_temp,
                outputPath=cabochaOutput,
                cabochaEncoding=cabochaEncoding,
                cabochaPath=cabochaPath,
                encoding="utf-8",
            )

            alignFromTextgrid.forceAlignCorpus(
                wavPath=speaker_temp,
                txtPath=cabochaOutput,
                outputPath=output_speaker_directory,
                juliusScriptPath=juliusScriptPath,
                soxPath=soxPath,
                perlPath=perlPath,
            )

