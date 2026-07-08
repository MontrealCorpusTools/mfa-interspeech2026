"""
Uses environment_files/mfa_environment.yaml
"""
import csv
import os
import re
import typing
from kalpy.gmm.data import CtmInterval, WordCtmInterval
from montreal_forced_aligner.exceptions import TextGridParseError
from montreal_forced_aligner.helper import mfa_open
from praatio import textgrid as tgio

root_alignment_dir = r"D:\Data\experiments\interspeech_benchmarking\alignments"
root_dir = r"D:\Data\experiments\interspeech_benchmarking\word_alignments"

corpus_directories = {
    "timit": r"D:\Data\speech\benchmark_datasets\timit\timit_benchmark",
    "buckeye": r"D:\Data\speech\benchmark_datasets\buckeye\buckeye_corpus_lab",
}

reference_directories = {
    "timit": r"D:\Data\speech\benchmark_datasets\timit\timit_reference",
    "buckeye": r"D:\Data\speech\benchmark_datasets\buckeye\buckeye_corpus_lab_reference",
}


def align_words(
    ref: typing.List[CtmInterval],
    test: typing.List[CtmInterval],
):
    test = [x for x in test if x.label not in {'sil', '#'}]
    try:
        assert len(ref) == len(test)
    except AssertionError:
        print("ORIGINAL")
        print(ref)
        print(test)
        print("--------")
        new_test = []
        try:
            for t in test:
                if len(new_test) and ref[len(new_test) - 1].label.startswith(new_test[-1].label + t.label):
                    new_test[-1].label += t.label
                    new_test[-1].end = t.end
                elif len(new_test) and ref[len(new_test) - 1].label.startswith(new_test[-1].label + '-' + t.label):
                    new_test[-1].label += '-' + t.label
                    new_test[-1].end = t.end
                elif len(new_test) and ref[len(new_test) - 1].label.startswith(new_test[-1].label + "'" + t.label):
                    new_test[-1].label += "'" + t.label
                    new_test[-1].end = t.end
                elif len(new_test) and ref[len(new_test) - 1].label == t.label == new_test[-1].label and len(ref) >= len(new_test) and ref[len(new_test)].label != t.label:
                    new_test[-1].end = t.end
                else:
                    new_test.append(t)
            if len(ref) != len(new_test):
                print(ref)
                print(test)
                print(new_test)
                print(len(new_test))
                print(len(ref), len(new_test))
                print(ref[len(new_test) - 1])
                return None, None
            test = new_test
            assert len(ref) == len(test)
        except Exception:
            print(ref)
            print(test)
            print(new_test)
            print(len(new_test))
            print(len(ref), len(new_test))
            print(ref[len(new_test) - 1])
            raise

    error_sum = 0.0
    boundary_count = 0
    boundary_errors = []
    for i, r in enumerate(ref):
        t = test[i]
        # assert r.label == t.label
        error_sum += abs(r.begin - t.begin)
        error_sum += abs(r.end - t.end)
        boundary_count += 2
        if i != 0:
            prev_ref, prev_test =ref[i - 1], test[i-1]
            boundary_errors.append(
                {
                    "following_word": r.label,
                    "previous_word": prev_ref.label,
                    "boundary_error": round(r.begin - t.begin, 3),
                    "reference_boundary": round(r.begin, 3),
                    "test_boundary": round(t.begin, 3),
                }
            )
        else:
            boundary_errors.append(
                {
                    "following_word": r.label,
                    "previous_word": "silence",
                    "boundary_error": round(r.begin - t.begin, 3),
                    "reference_boundary": round(r.begin, 3),
                    "test_boundary": round(t.begin, 3),
                }
            )
    boundary_errors.append(
        {
            "following_word": "silence",
            "previous_word": r.label,
            "boundary_error": round(r.end - t.end, 3),
            "reference_boundary": round(r.end, 3),
            "test_boundary": round(t.end, 3),
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
    num_tiers = len(tg.tiers)
    if num_tiers == 0:
        raise TextGridParseError(path, "Number of tiers parsed was zero")
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
            interval = CtmInterval(begin, end, text)
            data.append(interval)
    return data, tg.maxTimestamp


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
    for corpus, root in corpus_directories.items():
        for condition in os.listdir(os.path.join(root_alignment_dir, corpus)):
            aligned_directory = os.path.join(root_alignment_dir, corpus, condition)
            output_directory = os.path.join(root_dir, "alignments", corpus, condition)
            csv_path = os.path.join(output_directory, "word_alignment.csv")
            boundary_csv_path = os.path.join(output_directory, "word_alignment_boundaries.csv")
            if os.path.exists(boundary_csv_path):
                continue
            os.makedirs(output_directory, exist_ok=True)
            with (
                mfa_open(csv_path, "w") as f,
                mfa_open(boundary_csv_path, "w") as boundary_f,
            ):
                writer = csv.DictWriter(f, fieldnames=csv_header)
                writer.writeheader()
                boundary_writer = csv.DictWriter(boundary_f, fieldnames=boundary_csv_header)
                boundary_writer.writeheader()
                for speaker in os.listdir(aligned_directory):
                    speaker_directory = os.path.join(aligned_directory, speaker)
                    if not os.path.isdir(speaker_directory):
                        continue
                    for file_name in os.listdir(speaker_directory):

                        print(file_name)
                        word_intervals, _ = parse_aligned_textgrid(os.path.join(speaker_directory, file_name))
                        reference, file_duration = parse_aligned_textgrid(os.path.join(reference_directories[corpus], speaker, file_name))
                        word_index = 0
                        alignment_score, b_data = align_words(reference, word_intervals)
                        if alignment_score is None:
                            continue
                        words_per_second = len(reference) / file_duration
                        data = {
                            "file": file_name.replace(".TextGrid", ""),
                            "begin": 0.0,
                            "end": file_duration,
                            "duration": file_duration,
                            "speaker": speaker,
                            "normalized_text": [x.label for x in reference],
                            "filtered_text": " ".join(x.label for x in word_intervals),
                            "alignment_score": alignment_score,
                            "alignment_likelihood": 0.0,
                            "word_count": len(word_intervals),
                            "frames_per_second": 100,
                            "words_per_second": words_per_second,
                        }
                        writer.writerow(data)
                        for b in b_data:
                            b.update(
                                {
                                    "file": file_name.replace(".TextGrid", ""),
                                    "speaker": speaker,
                                }
                            )
                            boundary_writer.writerow(b)