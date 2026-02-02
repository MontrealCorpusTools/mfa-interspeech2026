import os
import sys
sys.path.insert(0, r"C:\Users\micha\Documents\Dev\charsiu\src")
sys.path.insert(0, r"C:\Users\micha\Documents\Dev\CharsiuG2P\src")
from Charsiu import charsiu_forced_aligner

root_dir = r"D:\Data\experiments\interspeech_benchmarking"

corpus_directories = {
    "timit": r"D:\Data\speech\benchmark_datasets\timit\timit_benchmark",
    "buckeye": r"D:\Data\speech\benchmark_datasets\buckeye\buckeye_corpus_lab",
}

if __name__ == "__main__":

    charsiu = charsiu_forced_aligner(aligner='charsiu/en_w2v2_fc_10ms')
    for corpus, root in corpus_directories.items():
        output_directory = os.path.join(root_dir, "alignments", corpus, "charsiu")
        for speaker in os.listdir(root):
            speaker_directory = os.path.join(root, speaker)
            output_speaker_directory = os.path.join(output_directory, speaker)
            os.makedirs(output_speaker_directory, exist_ok=True)
            for f in os.listdir(speaker_directory):
                if not f.endswith(".wav"):
                     continue
                text_path = os.path.join(speaker_directory, f.replace(".wav", ".txt"))
                output_path = os.path.join(output_speaker_directory, f.replace(".wav", ".TextGrid"))
                if os.path.exists(output_path):
                    continue
                if not os.path.exists(text_path):
                    text_path = text_path.replace(".txt", ".lab")
                with open(text_path, encoding='utf8') as inf:
                    text = inf.read()
                try:
                    charsiu.serve(audio=os.path.join(speaker_directory, f),
                                  text=text,
                                  save_to=output_path)
                except Exception:
                    pass