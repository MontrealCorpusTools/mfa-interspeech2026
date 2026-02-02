import requests
import os

root_dir = r"D:\Data\experiments\interspeech_benchmarking"

corpus_directories = {
    "timit": r"D:\Data\speech\benchmark_datasets\timit\timit_benchmark",
    "buckeye": r"D:\Data\speech\benchmark_datasets\buckeye\buckeye_corpus_lab",
}

if __name__ == "__main__":
    for corpus, root in corpus_directories.items():
        output_directory = os.path.join(root_dir, "alignments", corpus, "bournemouth")
        for speaker in os.listdir(root):
            speaker_directory = os.path.join(root, speaker)
            output_speaker_directory = os.path.join(output_directory, speaker)
            os.makedirs(output_speaker_directory, exist_ok=True)
            for f in os.listdir(speaker_directory):
                if not f.endswith(".wav"):
                     continue
