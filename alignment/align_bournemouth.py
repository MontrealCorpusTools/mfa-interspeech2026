
import time
import json
import os
from bournemouth_aligner import PhonemeTimestampAligner
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

    # Initialize aligner using language preset (recommended)
    extractor = PhonemeTimestampAligner(
        preset="en-us",  # Automatically selects best English model
        duration_max=10,
        device='cpu'
    )
    for corpus, root in corpus_directories.items():
        output_directory = os.path.join(root_dir, "alignments", corpus, "bournemouth")
        for speaker in os.listdir(root):
            speaker_directory = os.path.join(root, speaker)
            output_speaker_directory = os.path.join(output_directory, speaker)
            os.makedirs(output_speaker_directory, exist_ok=True)
            for f in os.listdir(speaker_directory):
                if not f.endswith(".wav"):
                     continue
                audio_path = os.path.join(speaker_directory, f)
                text_path = os.path.join(speaker_directory, f.replace(".wav", ".txt"))
                output_path = os.path.join(output_speaker_directory, f.replace(".wav", ".TextGrid"))
                if os.path.exists(output_path):
                    continue
                if not os.path.exists(text_path):
                    text_path = text_path.replace(".txt", ".lab")
                with open(text_path, encoding='utf8') as inf:
                    text = inf.read()

                # Load and process
                audio_wav = extractor.load_audio(audio_path) # use RMS normalization for preloaded wav `audio_wav = extractor._rms_normalize(audio_wav)`

                t0 = time.time()
                timestamps = extractor.process_sentence(
                    text,
                    audio_wav,
                    ts_out_path=None,
                    extract_embeddings=False,
                    vspt_path=None,
                    do_groups=True,
                    debug=True
                )
                t1 = time.time()
                print("🎯 Timestamps:")
                print(json.dumps(timestamps, indent=4, ensure_ascii=False))
                print(f"⚡ Processing time: {t1 - t0:.2f} seconds")
                error