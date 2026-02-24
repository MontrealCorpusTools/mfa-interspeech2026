import subprocess
import os
import sys
import random
if sys.platform == 'win32':
    root_dir = r"D:\Data\experiments\interspeech_benchmarking"

    maps_dir = r'C:\Users\micha\Documents\Dev\Tools\MAPS-main'
    corpus_directories = {
        "timit": r"D:\Data\speech\benchmark_datasets\timit\timit_benchmark",
        "buckeye": r"D:\Data\speech\benchmark_datasets\buckeye\buckeye_corpus_lab",
    }
else:
    root_dir = r"/mnt/d/Data/experiments/interspeech_benchmarking"
    maps_dir = r'/home/micha/downloads/MAPS'
    corpus_directories = {
        "timit": r"/mnt/d/Data/speech/benchmark_datasets/timit/timit_benchmark",
        "buckeye": r"/mnt/d/Data/speech/benchmark_datasets/buckeye/buckeye_corpus_lab",
    }
maps_file = os.path.join(maps_dir, "maps.py")
maps_model = os.path.join(maps_dir, "timbuck_eng.tf")
maps_dict = os.path.join(maps_dir, "cmudict-0.7b")
oov_path = os.path.join(maps_dir, "oovs.txt")

def load_dictionary():
    dictionary_words = set()
    lines = []
    with open(maps_dict, 'r', encoding='utf8') as f:
        for line in f:
            line = line.upper()
            lines.append(line)
            word, _ = line.strip().split(maxsplit=1)
            dictionary_words.add(word)
    #with open(maps_dict, 'w', encoding='utf8') as f:
    #    for line in lines:
    #        f.write(line.upper())
    return dictionary_words

if __name__ == "__main__":
    punctuation = [',', "!", "?", '"', "(", ")", ":", ";", '.', ">"]
    conditions = ['maps_variants', 'maps', ]
    existing_words = load_dictionary()
    words_to_g2p = set()
    for condition in conditions:
        for corpus, root in corpus_directories.items():
            output_directory = os.path.join(root_dir, "alignments", corpus, condition)
            for speaker in os.listdir(root):
                speaker_directory = os.path.join(root, speaker)
                output_speaker_directory = os.path.join(output_directory, speaker)
                if os.path.exists(output_speaker_directory):
                    continue
                for f in os.listdir(speaker_directory):
                    if not f.endswith(".wav"):
                         continue
                    audio_path = os.path.join(speaker_directory, f)
                    text_path = os.path.join(speaker_directory, f.replace(".wav", ".txt"))
                    if os.path.exists(text_path):
                        with open(text_path, encoding='utf8') as inf:
                            text = inf.read().strip()

                    else:
                        with open(text_path.replace('.txt', '.lab'), encoding='utf8') as inf:
                            text = inf.read().strip()
                    if text.endswith("."):
                        text = text[:-1]
                    for x in punctuation:
                        text = text.replace(x, '')
                    text = text.replace("-", " ")
                    #words = [x for x in text.upper().split() if x]
                    #oovs = [x.lower() for x in words if x not in existing_words]
                    #if oovs:
                    #    print(text)
                    #    print(text_path)
                    #words_to_g2p.update(oovs)
                    #continue
                    with open(text_path, 'w', encoding='utf8') as outf:
                        outf.write(text)
                #continue
                os.makedirs(output_speaker_directory, exist_ok=True)
                command = [
                    "python",
                    maps_file,
                    "--audio",
                    speaker_directory,
                    "--text",
                    speaker_directory,
                    "--output",
                    output_speaker_directory,
                    "--model",
                    maps_model,
                    "--dict",
                    maps_dict,
                ]
                if "variants" in condition:
                    command += [
                        "--check-variants",
                    "--variant-limit", '1000',
                        "--variant-shuffle",
                        "--variant-seed", "1234"
                    ]
                subprocess.check_call(command)
        #with open(oov_path, 'w', encoding='utf8') as outf:
        #    for w in sorted(words_to_g2p):
        #        outf.write(f"{w}\n")