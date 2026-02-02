import shutil
import subprocess
import os
import sys
if sys.platform == 'win32':
    root_dir = r"D:\Data\experiments\interspeech_benchmarking"

    corpus_directories = {
        "timit": r"D:\Data\speech\benchmark_datasets\timit\timit_benchmark",
        "buckeye": r"D:\Data\speech\benchmark_datasets\buckeye\buckeye_corpus_lab",
    }
else:
    root_dir = r"/mnt/d/Data/experiments/interspeech_benchmarking"

    corpus_directories = {
        "timit": r"/mnt/d/Data/speech/benchmark_datasets/timit/timit_benchmark",
        "buckeye": r"/mnt/d/Data/speech/benchmark_datasets/buckeye/buckeye_corpus_lab",
    }


if __name__ == "__main__":

    for corpus, root in corpus_directories.items():
        output_directory = os.path.join(root_dir, "alignments", corpus, "w2tg")
        for speaker in os.listdir(root):
            speaker_directory = os.path.join(root, speaker)
            output_speaker_directory = os.path.join(output_directory, speaker)
            if os.path.exists(output_speaker_directory):
                continue
            os.makedirs(output_speaker_directory, exist_ok=True)
            for f in os.listdir(speaker_directory):
                if not f.endswith(".wav"):
                     continue
                audio_path = os.path.join(speaker_directory, f)
                text_path = os.path.join(speaker_directory, f.replace(".wav", ".lab"))
                output_path = os.path.join(output_speaker_directory, f.replace(".wav", ".TextGrid"))
                if not os.path.exists(text_path):
                    shutil.copyfile(text_path.replace('.lab', '.txt'), text_path)
            subprocess.call(["w2tg", speaker_directory, speaker_directory, output_speaker_directory])