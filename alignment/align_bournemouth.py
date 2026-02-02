import re
import time
import json
import sudachipy
import os
from praatio import textgrid as tgio
from praatio.utilities.constants import Interval as PraatInterval
from bournemouth_aligner import PhonemeTimestampAligner
import sys
if sys.platform == 'win32':
    root_dir = r"D:\Data\experiments\interspeech_benchmarking"

    corpus_directories = {
        "timit": r"D:\Data\speech\benchmark_datasets\timit\timit_benchmark",
        "buckeye": r"D:\Data\speech\benchmark_datasets\buckeye\buckeye_corpus_lab",
        "csj": r"D:\Data\speech\benchmark_datasets\csj\csj_lab",
        "seoul_corpus": r"D:\Data\speech\benchmark_datasets\seoul_corpus\seoul_corpus_lab",
    }
else:
    root_dir = r"/mnt/d/Data/experiments/interspeech_benchmarking"

    corpus_directories = {
        #"timit": r"/mnt/d/Data/speech/benchmark_datasets/timit/timit_benchmark",
        #"buckeye": r"/mnt/d/Data/speech/benchmark_datasets/buckeye/buckeye_corpus_lab",
        "csj": r"/mnt/d/Data/speech/benchmark_datasets/csj/csj_lab",
        #"seoul_corpus": r"/mnt/d/Data/speech/benchmark_datasets/seoul_corpus/seoul_corpus_lab",
    }


if __name__ == "__main__":

    # Initialize aligner using language preset (recommended)
    for corpus, root in corpus_directories.items():
        if corpus == 'csj':
            lang = 'ja'
        elif corpus == 'seoul_corpus':
            lang = 'ko'
        else:
            lang = "en-us"
        if lang == 'en-us':
            extractor = PhonemeTimestampAligner(
                preset=lang,  # Automatically selects best English model
                duration_max=10,
                device='cuda',
                boost_targets=True,
                enforce_all_targets=True,
                ignore_noise=True,
            )
        else:
            if lang == 'ja':
                config_path = r'/mnt/c/Users/micha/Documents/Dev/Montreal-Forced-Aligner/montreal_forced_aligner/tokenization/resources/japanese/sudachi_config.json'
                tokenizer = sudachipy.Dictionary(dict="full", config_path=config_path).create(
                    mode=sudachipy.SplitMode.B
                )
                morphemes = tokenizer.tokenize("")
            extractor = PhonemeTimestampAligner(
                lang=lang,
                model_name="large_multi_mswc38_ua02g_e03_val_GER=0.5133.ckpt",
                duration_max=10,
                device='cuda',
                boost_targets=True,
                enforce_all_targets=True,
                ignore_noise=True,
            )
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
                    text = inf.read().strip()
                    if lang == 'ja':
                        tokenizer.tokenize(text, out=morphemes)
                        pronunciations = []
                        for morph in morphemes:
                            normalized = morph.surface()
                            pronunciation = ""
                            if morph.part_of_speech()[0] != "補助記号":
                                pronunciation = morph.reading_form()
                            pronunciations.append(pronunciation)
                        text = "".join(pronunciations).replace("ー", '')
                    if re.match(r'^.*\w$', text) is not None and lang != 'ja':
                        text += '.'
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
                    debug=False
                )
                t1 = time.time()
                phone_intervals = []
                word_intervals = []
                file_duration = None
                for s in timestamps["segments"]:
                    file_duration = s['end']
                    for i, pi in enumerate(s["phoneme_ts"]):
                        begin = pi["start_ms"] / 1000
                        end = pi["end_ms"] / 1000
                        if i != len(s["phoneme_ts"]) - 1:
                            end = s["phoneme_ts"][i+1]["start_ms"] / 1000
                        phone = pi["phoneme_label"]
                        if phone == "SIL":
                            continue
                        phone_intervals.append(PraatInterval(begin,end, phone))
                    for i, pi in enumerate(s["words_ts"]):
                        begin = pi["start_ms"] / 1000
                        end = pi["end_ms"] / 1000
                        if i != len(s["words_ts"]) - 1:
                            end = s["words_ts"][i+1]["start_ms"] / 1000
                        word = pi["word"]
                        if word == "<sil>":
                            continue
                        word_intervals.append(PraatInterval(begin,end, word))
                try:
                    tg = tgio.Textgrid(minTimestamp=0, maxTimestamp=file_duration)
                    tg.addTier(tgio.IntervalTier(f"{speaker} - words", word_intervals, 0,file_duration))
                    tg.addTier(tgio.IntervalTier(f"{speaker} - phones", phone_intervals, 0,file_duration))
                    tg.save(output_path, "short_textgrid", True)
                except Exception:
                    print(f)
                    raise