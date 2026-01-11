import os
import shutil

corpus_directory = r'D:\Data\speech\benchmark_datasets\seoul_corpus\seoul_corpus_lab'

batch_output_root = r"D:\Data\experiments\interspeech_benchmarking\temp"

if __name__ == '__main__':
    for speaker in os.listdir(corpus_directory):
        speaker_dir = os.path.join(corpus_directory, speaker)
        count = 0
        batch_num = 0
        for f in sorted(os.listdir(speaker_dir)):
            batch_directory = os.path.join(batch_output_root, speaker, f"batch_{batch_num}")
            os.makedirs(batch_directory, exist_ok=True)
            shutil.copyfile(os.path.join(speaker_dir, f), os.path.join(batch_directory, f))
            count += 1
            if count >= 100:
                batch_num += 1
                count = 0
