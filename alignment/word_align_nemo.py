"""Based on https://pytorch.org/audio/stable/tutorials/ctc_forced_alignment_api_tutorial.html"""
import csv
import os
import re
import sys
import typing
import torch
import torchaudio
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
nemo_tools_path = r"C:\Users\micha\Documents\Dev\NeMo\tools"

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
                    "following_reference_word": r.label,
                    "following_test_word": t.label,
                    "previous_reference_word": prev_ref.label,
                    "previous_test_word": prev_test.label,
                    "boundary_error": round(r.begin - t.begin, 3),
                    "reference_boundary": round(r.begin, 3),
                    "test_boundary": round(t.begin, 3),
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
        "utterance_begin",
        "utterance_end",
        "speaker",
        "following_reference_word",
        "following_test_word",
        "previous_reference_word",
        "previous_test_word",
        "boundary_error",
        "reference_boundary",
        "test_boundary",
    ]
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(device)
    try:
        from dataclasses import dataclass, field, is_dataclass

        from nemo.collections.asr.models.ctc_models import EncDecCTCModel
        from nemo.collections.asr.models.hybrid_rnnt_ctc_models import (
            EncDecHybridRNNTCTCModel,
        )
        from nemo.collections.asr.parts.utils.streaming_utils import FrameBatchASR
        from nemo.collections.asr.parts.utils.transcribe_utils import setup_model
        from nemo.core.config import hydra_runner
    except ImportError:
        raise
    sys.path.append(nemo_tools_path)
    sys.path.insert(0, os.path.join(nemo_tools_path, "nemo_forced_aligner"))
    import tempfile

    from nemo_forced_aligner.align import AlignmentConfig, ASSFileConfig, CTMFileConfig
    from nemo_forced_aligner.utils.data_prep import (
        V_NEGATIVE_NUM,
        Segment,
        Token,
        Word,
        add_t_start_end_to_utt_obj,
        get_utt_obj,
    )
    from nemo_forced_aligner.utils.viterbi_decoding import viterbi_decoding

    cfg = AlignmentConfig()
    cfg.pretrained_name = "stt_en_conformer_ctc_medium"
    if cfg.transcribe_device is None:
        transcribe_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    else:
        transcribe_device = torch.device(cfg.transcribe_device)
    if cfg.viterbi_device is None:
        viterbi_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    else:
        viterbi_device = torch.device(cfg.viterbi_device)
    model, _ = setup_model(cfg, transcribe_device)
    model.eval()
    if isinstance(model, EncDecHybridRNNTCTCModel):
        model.change_decoding_strategy(decoder_type="ctc")
    if cfg.use_local_attention:
        model.change_attention_model(
            self_attention_model="rel_pos_local_attn", att_context_size=[64, 64]
        )

    with torch.inference_mode():
        for c, corpus_directory in corpus_directories.items():
            output_directory = os.path.join(root_dir, "alignments", c, "nemo")
            #if os.path.exists(output_directory):
            #    continue
            corpus = AcousticCorpus(corpus_directory=corpus_directory)
            corpus.delete_database()
            corpus._load_corpus()
            os.makedirs(output_directory, exist_ok=True)
            csv_path = os.path.join(output_directory, "word_alignment.csv")
            boundary_csv_path = os.path.join(output_directory, "word_alignment_boundaries.csv")
            with (
                corpus.session() as session,
                mfa_open(csv_path, "w") as f,
                mfa_open(boundary_csv_path, "w") as boundary_f,
                tempfile.TemporaryDirectory() as tmpdir,
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
                        with torch.no_grad():
                            output_timestep_duration = None
                            path = os.path.join(tmpdir, f"sound_file.wav")
                            torchaudio.save(
                                path,
                                torch.unsqueeze(
                                    torch.Tensor(kalpy_utterance.segment.load_audio()),
                                    0,
                                ),
                                16000,
                            )
                            hypotheses = model.transcribe(
                                [path],
                                return_hypotheses=True,
                                verbose=False,
                                batch_size=1,
                            )
                            # if hypotheses form a tuple (from Hybrid model), extract just "best" hypothesis
                            if type(hypotheses) == tuple and len(hypotheses) == 2:
                                hypotheses = hypotheses[0]

                            for hypothesis in hypotheses:
                                log_probs_list_batch = [hypothesis.y_sequence]
                                T_list_batch = [hypothesis.y_sequence.shape[0]]
                                pred_text_batch = [hypothesis.text]
                                utt_obj = get_utt_obj(
                                    text,
                                    model,
                                    cfg.additional_segment_grouping_separator,
                                    T_list_batch[0],
                                    file.sound_file.sound_file_path,
                                    utterance.kaldi_id,
                                )
                            alignment_likelihood = float(hypothesis.score)
                        y_list_batch = [utt_obj.token_ids_with_blanks]
                        U_list_batch = [len(utt_obj.token_ids_with_blanks)]
                        utt_obj_batch = [utt_obj]
                        T_max = max(T_list_batch)
                        U_max = max(U_list_batch)
                        if hasattr(model, "tokenizer"):
                            V = len(model.tokenizer.vocab) + 1
                        else:
                            V = len(model.decoder.vocabulary) + 1
                        T_batch = torch.tensor(T_list_batch)
                        U_batch = torch.tensor(U_list_batch)
                        log_probs_batch = V_NEGATIVE_NUM * torch.ones((1, T_max, V))
                        for b, log_probs_utt in enumerate(log_probs_list_batch):
                            t = log_probs_utt.shape[0]
                            log_probs_batch[b, :t, :] = log_probs_utt
                        y_batch = V * torch.ones((1, U_max), dtype=torch.int64)
                        for b, y_utt in enumerate(y_list_batch):
                            U_utt = U_batch[b]
                            y_batch[b, :U_utt] = torch.tensor(y_utt)
                        # calculate output_timestep_duration if it is None
                        if output_timestep_duration is None:
                            if not "window_stride" in model.cfg.preprocessor:
                                raise ValueError(
                                    "Don't have attribute 'window_stride' in "
                                    "'model.cfg.preprocessor' => cannot calculate "
                                    " model_downsample_factor => stopping process"
                                )

                            if not "sample_rate" in model.cfg.preprocessor:
                                raise ValueError(
                                    "Don't have attribute 'sample_rate' in "
                                    "'model.cfg.preprocessor' => cannot calculate start "
                                    " and end time of segments => stopping process"
                                )

                            audio_dur = utterance.duration
                            n_input_frames = (
                                    audio_dur / model.cfg.preprocessor.window_stride
                            )
                            model_downsample_factor = round(
                                n_input_frames / int(T_batch[0])
                            )

                            output_timestep_duration = (
                                    model.preprocessor.featurizer.hop_length
                                    * model_downsample_factor
                                    / model.cfg.preprocessor.sample_rate
                            )
                        alignments_batch = viterbi_decoding(
                            log_probs_batch,
                            y_batch,
                            T_batch,
                            U_batch,
                            viterbi_device,
                        )
                        utt_obj, alignment_utt = (
                            utt_obj_batch[0],
                            alignments_batch[0],
                        )

                        utt_obj = add_t_start_end_to_utt_obj(
                            utt_obj, alignment_utt, output_timestep_duration
                        )
                        segment = [
                            x
                            for x in utt_obj.segments_and_tokens
                            if isinstance(x, Segment)
                        ][0]
                        words = [
                            x for x in segment.words_and_tokens if isinstance(x, Word)
                        ]
                        word_intervals = []
                        for word in words:
                            character_intervals = []
                            word_label = word.text
                            for token in word.tokens:
                                if token.text == "<b>":
                                    continue
                                begin = token.t_start + utterance.begin
                                end = token.t_end + utterance.begin
                                if end > utterance.end:
                                    end = utterance.end
                                label = token.text
                                character_intervals.append(
                                    CtmInterval(begin, end, label, 0)
                                )
                            word_intervals.append(
                                WordCtmInterval(
                                    word_label, 0, character_intervals
                                )
                            )
                        ctm = HierarchicalCtm(word_intervals)

                        frames_per_second = (
                                log_probs_list_batch[0].size(0) / utterance.duration
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
                            "normalized_text": utterance.normalized_text,
                            "filtered_text": text,
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
                                    "utterance_begin": utterance.begin,
                                    "utterance_end": utterance.end,
                                    "speaker": utterance.speaker_name,
                                }
                            )
                            boundary_writer.writerow(b)
                        progress_bar.update(1)
                    file_ctm.export_textgrid(
                        output_path,
                        file_duration=file.duration,
                        output_format="short_textgrid",
                    )