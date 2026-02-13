"""Based on https://pytorch.org/audio/stable/tutorials/ctc_forced_alignment_api_tutorial.html"""
import csv
import os
import re
import sys
import typing
import torch
import subprocess
import json
from kalpy.gmm.data import CtmInterval, HierarchicalCtm, WordCtmInterval
from praatio import textgrid as tgio

if sys.platform == 'win32':
    root_dir = r"D:\Data\experiments\interspeech_benchmarking\word_alignments"
    nemo_tools_path = r"C:\Users\micha\Documents\Dev\NeMo\tools"
    nemo_align = os.path.join(nemo_tools_path, "nemo_forced_aligner", "align.py")

    corpus_directories = {
        #"timit": r"D:\Data\speech\benchmark_datasets\timit\timit_benchmark",
        "buckeye": r"D:\Data\speech\benchmark_datasets\buckeye\buckeye_corpus_lab",
        #"csj": r"D:\Data\speech\benchmark_datasets\csj\csj_lab",
        #"seoul_corpus": r"D:\Data\speech\benchmark_datasets\seoul_corpus\seoul_corpus_lab",
    }

    reference_directories = {
        "timit": r"D:\Data\speech\benchmark_datasets\timit\timit_reference",
        "buckeye": r"D:\Data\speech\benchmark_datasets\buckeye\buckeye_corpus_lab_reference",
        "csj": r"D:\Data\speech\benchmark_datasets\csj\csj_lab_reference",
        "seoul_corpus": r"D:\Data\speech\benchmark_datasets\seoul_corpus\seoul_corpus_lab_reference",
    }
else:
    root_dir = r"/mnt/d/Data/experiments/interspeech_benchmarking/word_alignments"
    nemo_tools_path = r"/home/micha/downloads/NeMo/tools"
    nemo_align = os.path.join(nemo_tools_path, "nemo_forced_aligner", "align.py")

    corpus_directories = {
        #"timit": r"/mnt/d/Data/speech/benchmark_datasets/timit/timit_benchmark",
        "buckeye": r"/mnt/d/Data/speech/benchmark_datasets/buckeye/buckeye_corpus_lab",
        #"csj": r"/mnt/d/Data/speech/benchmark_datasets/csj/csj_lab",
        #"seoul_corpus": r"/mnt/d/Data/speech/benchmark_datasets/seoul_corpus/seoul_corpus_lab",
    }

    reference_directories = {
        "timit": r"/mnt/d/Data/speech/benchmark_datasets/timit/timit_reference",
        "buckeye": r"/mnt/d/Data/speech/benchmark_datasets/buckeye/buckeye_corpus_lab_reference",
        "csj": r"/mnt/d/Data/speech/benchmark_datasets/csj/csj_lab_reference",
        "seoul_corpus": r"/mnt/d/Data/speech/benchmark_datasets/seoul_corpus/seoul_corpus_lab_reference",
    }


def align_words(
    ref: typing.List[CtmInterval],
    test: typing.List[CtmInterval],
):
    try:
        assert len(ref) == len(test)
    except AssertionError:
        new_test = []
        offset = 1
        try:
            for t in test:
                if len(new_test) and ref[len(new_test) - 1][2].startswith(new_test[-1][2] + t[2]):
                    new_test[-1][2] += t[2]
                    new_test[-1][1] = t[1]
                    offset += 1
                elif len(new_test) and ref[len(new_test) - 1][2].startswith(new_test[-1][2] + '-' + t[2]):
                    new_test[-1][2] += '-' + t[2]
                    new_test[-1][1] = t[1]
                    offset += 1
                else:
                    new_test.append(t)
            test = new_test
            assert len(ref) == len(test)
        except Exception:
            print(ref)
            print(test)
            print(new_test)
            print(len(new_test))
            print(len(new_test) + offset)
            print(offset)
            print(len(ref), len(new_test))
            print(ref[len(new_test) - 1])
            raise

    error_sum = 0.0
    boundary_count = 0
    boundary_errors = []
    for i, r in enumerate(ref):
        t = test[i]
        # assert r.label == t.label
        error_sum += abs(r[0] - t[0])
        error_sum += abs(r[1] - t[1])
        boundary_count += 2
        if i != 0:
            prev_ref, prev_test =ref[i - 1], test[i-1]
            boundary_errors.append(
                {
                    "following_word": r[2],
                    "previous_word": prev_ref[2],
                    "boundary_error": round(r[0] - t[0], 3),
                    "reference_boundary": round(r[0], 3),
                    "test_boundary": round(t[0], 3),
                }
            )
        else:
            boundary_errors.append(
                {
                    "following_word": r[2],
                    "previous_word": "silence",
                    "boundary_error": round(r[0] - t[0], 3),
                    "reference_boundary": round(r[0], 3),
                    "test_boundary": round(t[0], 3),
                }
            )
    boundary_errors.append(
        {
            "following_word": "silence",
            "previous_word": r[2],
            "boundary_error": round(r[1] - t[1], 3),
            "reference_boundary": round(r[1], 3),
            "test_boundary": round(t[1], 3),
        }
    )
    return error_sum / boundary_count, boundary_errors


def parse_aligned_textgrid(path: str, exclude_unknowns=True) -> typing.List[CtmInterval]:
    """
    Load a TextGrid as a dictionary of speaker's phone tiers

    Parameters
    ----------
    path: :class:`~pathlib.Path`
        TextGrid file to parse

    Returns
    -------
    dict[str, list[:class:`~montreal_forced_aligner.data.CtmInterval`]]
        Parsed phone tier
    """
    tg = tgio.openTextgrid(path, includeEmptyIntervals=False, reportingMode="silence")
    data = []
    for tier_name in tg.tierNames:
        ti = tg._tierDict[tier_name]
        if not isinstance(ti, tgio.IntervalTier):
            continue
        if "words" not in tier_name:
            continue
        for begin, end, text in ti.entries:
            text = text.lower().strip().replace("?", "")
            if exclude_unknowns and re.match(r"^[\[(<].*", text):
                continue
            if not text:
                continue
            begin, end = round(begin, 4), round(end, 4)
            # if end - begin < 0.01:
            #    continue
            #interval = CtmInterval(begin, end, text)
            data.append([begin, end, text])
    return data


if __name__ == "__main__":
    csv_header = [
        "file",
        "begin",
        "end",
        "speaker",
        "duration",
        "normalized_text",
        "filtered_text",
        "alignment_score",
        "alignment_likelihood",
        "word_count",
        "frames_per_second",
        "words_per_second",
    ]
    boundary_csv_header = [
        "file",
        "speaker",
        "previous_word",
        "following_word",
        "boundary_error",
        "reference_boundary",
        "test_boundary",
    ]
    sys.path.append(nemo_tools_path)
    sys.path.insert(0, os.path.join(nemo_tools_path, "nemo_forced_aligner"))



    with torch.inference_mode():
        for c, corpus_directory in corpus_directories.items():
            output_directory = os.path.join(root_dir, "alignments", c, "nemo_script")
            #if os.path.exists(output_directory):
            #    continue
            os.makedirs(output_directory, exist_ok=True)
            csv_path = os.path.join(output_directory, "word_alignment.csv")
            boundary_csv_path = os.path.join(output_directory, "word_alignment_boundaries.csv")
            with (
                open(csv_path, "w", newline="") as f,
                open(boundary_csv_path, "w", newline='') as boundary_f,
            ):
                writer = csv.DictWriter(f, fieldnames=csv_header)
                writer.writeheader()
                boundary_writer = csv.DictWriter(boundary_f, fieldnames=boundary_csv_header)
                boundary_writer.writeheader()
                for speaker in os.listdir(corpus_directory):
                    speaker_directory = os.path.join(corpus_directory, speaker)
                    output_speaker_directory = os.path.join(output_directory, speaker)
                    ctm_dir = os.path.join(output_speaker_directory, "nfa_output", "ctm", "words")
                    if os.path.exists(ctm_dir):
                        continue
                    os.makedirs(output_speaker_directory, exist_ok=True)
                    manifest_data = []
                    for file in os.listdir(speaker_directory):
                        if not file.endswith('.wav'):
                            continue
                        audio_path = os.path.join(speaker_directory, file)
                        text_path = os.path.join(speaker_directory, file.replace('.wav', '.txt'))
                        with open(text_path, 'r', encoding='utf8') as tf:
                            text = tf.read().strip()
                        manifest_data.append({
                            "audio_filepath": audio_path,
                            "text": text
                        })
                    manifest_filepath = os.path.join(output_speaker_directory, 'manifest.json')
                    with open(manifest_filepath, 'w') as outf:
                        for d in manifest_data:
                            line = json.dumps(d)
                            outf.write(f"{line}\n")
                    subprocess.call([
                        "python",
                        nemo_align,
                        'pretrained_name="stt_en_fastconformer_hybrid_large_pc"',
                        f'manifest_filepath={manifest_filepath}',
                        f"output_dir={output_speaker_directory}/nfa_output/",
                    ])
                    if not os.path.exists(ctm_dir):
                        continue
                    for file_name in os.listdir(ctm_dir):
                        with open(os.path.join(ctm_dir, file_name), 'r') as ctm_f:
                            word_intervals = []
                            for line in ctm_f:
                                line = line.strip()
                                if not line:
                                    continue
                                line = line.split()
                                word, begin, duration = line[4], float(line[2]), float(line[3])
                                end = begin + duration
                                word_intervals.append([begin, end, word])
                        reference_path = os.path.join(reference_directories[c], speaker, file_name.replace(".ctm", '.TextGrid'))
                        reference_intervals = parse_aligned_textgrid(reference_path)
                        alignment_score, b_data = align_words(reference_intervals, word_intervals)
                        for b in b_data:
                            b.update(
                                {
                                    "file": file_name.replace(".ctm", ''),
                                    "speaker": speaker,
                                }
                            )
                            boundary_writer.writerow(b)


