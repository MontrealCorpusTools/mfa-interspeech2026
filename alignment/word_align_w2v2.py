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


def align(emission, tokens):
    targets = torch.tensor([tokens], dtype=torch.int32, device=device)
    alignments, scores = F.forced_align(emission, targets, blank=0)

    alignments, scores = (
        alignments[0],
        scores[0],
    )  # remove batch dimension for simplicity
    scores = scores.exp()  # convert back to probability
    return alignments, scores


def unflatten(list_, lengths):
    assert len(list_) == sum(lengths)
    i = 0
    ret = []
    for l in lengths:
        ret.append(list_[i : i + l])
        i += l
    return ret


def generate_ctm(
    token_spans, transcript, ratio, sample_rate, utterance_begin, reference
) -> HierarchicalCtm:
    i = 0
    reference_index = 0
    word_intervals = []
    for word in transcript:
        character_intervals = []
        for j in range(len(word)):
            span = token_spans[i]
            begin = int(ratio * span.start) / sample_rate
            begin += utterance_begin
            end = int(ratio * span.end) / sample_rate
            end += utterance_begin
            character_intervals.append(
                CtmInterval(begin, end, LABELS[span.token], span.token)
            )
            i += 1
        if word == reference[reference_index].label:
            reference_index += 1
        elif (
            word_intervals
            and f"{word_intervals[-1].label}-{word}" in reference[reference_index].label
        ):
            word_intervals[-1].label = f"{word_intervals[-1].label}-{word}"
            word_intervals[-1].symbol = 0
            word_intervals[-1].phones.extend(character_intervals)
            if reference[reference_index].label == word_intervals[-1].label:
                reference_index += 1
            continue
        word_intervals.append(WordCtmInterval(word, 0, character_intervals))
    return HierarchicalCtm(word_intervals)


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
    with torch.inference_mode():
        for c, benchmark_directory in corpus_directories.items():
            output_directory = os.path.join(root_dir, "alignments", c, "w2v2")
            #if os.path.exists(output_directory):
            #    continue
            try:
                bundle = torchaudio.pipelines.MMS_FA
            except AttributeError:
                print("Incorrect version of torchaudio, skipping torchaudio_mms_fa")
                raise

            model = bundle.get_model(with_star=False).to(device)

            LABELS = bundle.get_labels(star=None)
            DICTIONARY = bundle.get_dict(star=None)
            corpus = AcousticCorpus(corpus_directory=benchmark_directory)
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
                    reference_path = reference_directories[c]
                    if file.relative_path:
                        reference_path = os.path.join(reference_path, file.relative_path)
                    reference_path = os.path.join(reference_path, file.name + ".TextGrid")
                    reference_word_intervals = parse_aligned_textgrid(reference_path)
                    reference_interval_index = 0
                    for utterance in query:
                        kalpy_utterance = utterance.to_kalpy()
                        waveform = torch.unsqueeze(
                            torch.Tensor(kalpy_utterance.segment.load_audio()),
                            0,
                        )
                        text = utterance.text.lower().replace("-", " ")
                        transcript = [
                            re.sub(rf'[^{"".join(LABELS[1:])}]', "", x)
                            for x in text.split()
                            if not re.match(r"^[\[(<].*", x)
                        ]
                        transcript = [x for x in transcript if x]
                        tokenized_transcript = [
                            DICTIONARY[c] for word in transcript for c in word
                        ]
                        emission, _ = model(waveform.to(device))
                        aligned_tokens, alignment_scores = align(
                            emission, tokenized_transcript
                        )
                        token_spans = F.merge_tokens(aligned_tokens, alignment_scores)
                        alignment_likelihood = sum(alignment_scores) / len(
                            alignment_scores
                        )
                        word_spans = unflatten(
                            token_spans, [len(word) for word in transcript]
                        )
                        ratio = waveform.size(1) / emission.size(1)
                        frames_per_second = emission.size(1) / utterance.duration
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
                        ctm = generate_ctm(
                            token_spans,
                            transcript,
                            ratio,
                            bundle.sample_rate,
                            utterance.begin,
                            reference,
                        )
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
                            "normalized_text": text.replace(",", ""),
                            "filtered_text": " ".join(transcript),
                            "alignment_score": alignment_score,
                            "alignment_likelihood": float(alignment_likelihood),
                            "word_count": len(ctm.word_intervals),
                            "frames_per_second": frames_per_second,
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