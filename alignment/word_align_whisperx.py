"""Based on https://pytorch.org/audio/stable/tutorials/ctc_forced_alignment_api_tutorial.html"""
import csv
import os
import re
import sys
import typing
import torch
import torchaudio
import torchaudio.functional as F
import tqdm
import sqlalchemy
import whisperx
from kalpy.gmm.data import CtmInterval, HierarchicalCtm, WordCtmInterval
from montreal_forced_aligner import config
from montreal_forced_aligner.command_line.mfa import mfa_cli
from montreal_forced_aligner.corpus.acoustic_corpus import AcousticCorpus
from montreal_forced_aligner.db import File, Utterance, Word, WordInterval
from montreal_forced_aligner.exceptions import TextGridParseError
from montreal_forced_aligner.helper import mfa_open
from praatio import textgrid as tgio

root_dir = r"D:\Data\experiments\interspeech_benchmarking\word_alignments"

corpus_directories = {
    "timit": r"D:\Data\speech\benchmark_datasets\timit\timit_benchmark",
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


def align_words(
    ref: typing.List[CtmInterval],
    test: typing.List[CtmInterval],
):
    try:
        assert len(ref) == len(test)
    except AssertionError:
        print(ref)
        print(test)
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
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(device)
    compute_type = "float16"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = whisperx.load_model(
        "large-v2", device, compute_type=compute_type, language="en"
    )
    model_a, metadata = whisperx.load_align_model(language_code="en", device=device)

    with torch.inference_mode():
        for corpus_name, root in corpus_directories.items():
            output_directory = os.path.join(root_dir, "alignments", corpus_name, "whisperx")
            #if os.path.exists(output_directory):
            #    continue
            corpus = AcousticCorpus(corpus_directory=root)
            corpus.delete_database()
            corpus._load_corpus()
            os.makedirs(output_directory, exist_ok=True)
            csv_path = os.path.join(output_directory, "word_alignment.csv")
            boundary_csv_path = os.path.join(output_directory, "word_alignment_boundaries.csv")
            with (
                corpus.session() as session,
                mfa_open(csv_path, "w") as f,
                mfa_open(boundary_csv_path, "w") as boundary_f,
                tqdm.tqdm(total=corpus.num_utterances) as progress_bar,
            ):
                writer = csv.DictWriter(f, fieldnames=csv_header)
                writer.writeheader()
                boundary_writer = csv.DictWriter(boundary_f, fieldnames=boundary_csv_header)
                boundary_writer.writeheader()
                file_query = (
                    session.query(File)
                    .options(
                        sqlalchemy.orm.joinedload(File.sound_file, innerjoin=True),
                    )
                    .order_by(File.name)
                )
                for file in file_query:
                    file_ctm = HierarchicalCtm([])
                    if file.relative_path:
                        output_path = os.path.join(output_directory, file.relative_path)
                        os.makedirs(output_path, exist_ok=True)
                    else:
                        output_path = output_directory
                    output_path = os.path.join(output_path, file.name + ".TextGrid")
                    query = (
                        session.query(Utterance)
                        .filter(Utterance.file_id == file.id)
                        .options(
                            sqlalchemy.orm.joinedload(
                                Utterance.file, innerjoin=True
                            ).joinedload(File.sound_file, innerjoin=True),
                        )
                        .order_by(Utterance.begin)
                    )
                    reference_path = reference_directories[corpus_name]
                    if file.relative_path:
                        reference_path = os.path.join(reference_path, file.relative_path)
                    reference_path = os.path.join(reference_path, file.name + ".TextGrid")
                    reference_word_intervals = parse_aligned_textgrid(reference_path)
                    reference_interval_index = 0
                    for utterance in query:
                        kalpy_utterance = utterance.to_kalpy()
                        reference = []
                        while True:
                            try:
                                interval = reference_word_intervals[
                                    reference_interval_index
                                ]
                            except IndexError:
                                break
                            if interval.begin >= utterance.end:
                                break
                            if interval.begin >= utterance.begin:
                                reference.append(interval)
                            reference_interval_index += 1
                        text = " ".join(x.label for x in reference)

                        audio = kalpy_utterance.segment.load_audio()

                        # transcribe_result = model.transcribe(audio, batch_size=1)
                        # print(result["segments"])
                        segments = [
                            {
                                "text": text,
                                "start": 0.0,
                                "end": utterance.duration,
                            }
                        ]
                        result = whisperx.align(
                            segments,
                            model_a,
                            metadata,
                            audio,
                            device,
                            return_char_alignments=True,
                        )

                        word_intervals = []
                        words = result["segments"][0]["words"]
                        chars = result["segments"][0]["chars"]
                        character_index = 0
                        score_sum = 0
                        for word in words:
                            character_intervals = []
                            word_label = word["word"]
                            while True:
                                try:
                                    c = chars[character_index]
                                except IndexError:
                                    break
                                if c["char"] == " ":
                                    character_index += 1
                                    continue
                                if c["start"] >= word["end"]:
                                    break
                                begin = c["start"] + utterance.begin
                                end = c["end"] + utterance.begin
                                character_intervals.append(
                                    CtmInterval(begin, end, c["char"])
                                )
                                character_index += 1
                            word_intervals.append(
                                WordCtmInterval(
                                    word_label, 0, character_intervals
                                )
                            )
                            score_sum += word["score"]
                        ctm = HierarchicalCtm(word_intervals)
                        alignment_likelihood = score_sum / len(words)
                        file_ctm.word_intervals.extend(ctm.word_intervals)
                        try:
                            alignment_score, b_data = align_words(reference, ctm.word_intervals)
                        except AssertionError:
                            print(file.name)
                            raise
                            continue
                        words_per_second = len(reference) / utterance.duration

                        data = {
                            "file": file.name,
                            "begin": utterance.begin,
                            "end": utterance.end,
                            "duration": utterance.duration,
                            "speaker": utterance.speaker_name,
                            "normalized_text": utterance.normalized_text,
                            "filtered_text": text,
                            "alignment_score": alignment_score,
                            "alignment_likelihood": float(alignment_likelihood),
                            "word_count": len(ctm.word_intervals),
                            "frames_per_second": "NA",
                            "words_per_second": words_per_second,
                        }
                        writer.writerow(data)
                        for b in b_data:
                            b.update(
                                {
                                    "file": file.name,
                                    "speaker": utterance.speaker_name,
                                }
                            )
                            boundary_writer.writerow(b)
                        progress_bar.update(1)
                    #file_ctm.export_textgrid(
                    #    output_path,
                    #    file_duration=file.duration,
                    #    output_format="short_textgrid",
                    #)