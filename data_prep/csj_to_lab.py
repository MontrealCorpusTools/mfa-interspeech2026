from pathlib import Path
import soundfile as sf
from montreal_forced_aligner.corpus.acoustic_corpus import AcousticCorpusWithPronunciations
from montreal_forced_aligner.command_line.utils import validate_dictionary
from montreal_forced_aligner import config
from kalpy.gmm.data import to_tg_interval
from montreal_forced_aligner.data import Language
from montreal_forced_aligner.db import Utterance, File, SoundFile, Speaker, ReferenceWordInterval, ReferencePhoneInterval
from sqlalchemy.orm import selectinload
from praatio import textgrid as tgio

benchmark_directory = Path(r"D:\Data\speech\benchmark_datasets\csj")

if __name__ == "__main__":
    config.CLEAN = True
    corpus_path = benchmark_directory.joinpath("csj_benchmark")
    reference_path = benchmark_directory.joinpath("csj_reference")
    audio_path = benchmark_directory.joinpath("original")
    lab_directory = benchmark_directory.joinpath("csj_lab")
    lab_reference_directory = benchmark_directory.joinpath("csj_lab_reference")
    dictionary_path = validate_dictionary(None, None, "japanese_mfa")
    corpus = AcousticCorpusWithPronunciations(
        corpus_directory=corpus_path, reference_directory=reference_path,
        dictionary_path=dictionary_path,
        audio_directory=audio_path,
        language=Language.japanese
    )
    corpus.initialize_database()
    corpus.dictionary_setup()
    corpus._load_corpus()
    corpus.load_reference_alignments(reference_path)
    corpus.initialize_jobs()
    corpus.normalize_text()

    with corpus.session() as session:
        query = (
            session.query(Utterance, Speaker, File, SoundFile)
            .join(Utterance.speaker)
            .join(Utterance.file)
            .join(File.sound_file)
            .filter(Utterance.text.not_like("%<%"))
            .options(
                selectinload(Utterance.reference_word_intervals).joinedload(ReferenceWordInterval.word, innerjoin=True),
                selectinload(Utterance.reference_phone_intervals).joinedload(ReferencePhoneInterval.phone, innerjoin=True),
            )
        )
        count = 0
        for utterance, speaker, file, sound_file in query:
            if not utterance.reference_word_intervals:
                continue
            file_name = f"{file.name}_{utterance.begin:.3f}_{utterance.end:.3f}".replace('.', '_')
            word_count = utterance.normalized_text.count(" ") + 1
            oovs = set(utterance.oovs.split(','))
            oov_count = len([x for x in utterance.normalized_text.split() if x in oovs])
            if word_count - oov_count <= 3:
                print("SKIPPING")
                print(utterance.text)
                print(utterance.normalized_text)
                print(utterance.normalized_character_text)
                print(utterance.oovs)
                continue
            speaker_directory = lab_directory.joinpath(speaker.name)
            speaker_directory.mkdir(parents=True, exist_ok=True)
            reference_speaker_directory = lab_reference_directory.joinpath(speaker.name)
            reference_speaker_directory.mkdir(parents=True, exist_ok=True)
            lab_file_path = speaker_directory.joinpath(file_name + ".txt")
            tg_file_path = reference_speaker_directory.joinpath(file_name + ".TextGrid")
            wav_file_path = speaker_directory.joinpath(file_name + ".wav")
            with open(lab_file_path, 'w', encoding='utf8') as f:
                f.write(utterance.text.replace("(F", ''))
            if not wav_file_path.exists():
                audio_segment = utterance.segment.load_audio()
                sf.write(wav_file_path, audio_segment, 16000)
            tg = tgio.Textgrid()
            tg.minTimestamp = 0
            file_duration = utterance.end - utterance.begin
            tg.maxTimestamp = file_duration
            word_intervals = []
            for wi in utterance.reference_word_intervals:
                try:
                    ctm = wi.as_ctm()
                    ctm.begin -= utterance.begin
                    ctm.begin = max(ctm.begin, 0)
                    ctm.end -= utterance.begin
                    word_intervals.append(to_tg_interval(ctm, file_duration=file_duration))
                except AssertionError:
                    print(file_name)
                    print(utterance.begin, utterance.end, utterance.text)
                    print(utterance.reference_word_intervals)
                    print(ctm.begin, ctm.end, ctm.label)
            tg.addTier(tgio.IntervalTier("words", word_intervals, 0.0, file_duration))
            phone_intervals = []
            for pi in utterance.reference_phone_intervals:
                try:
                    ctm = pi.as_ctm()
                    ctm.begin -= utterance.begin
                    ctm.begin = max(ctm.begin, 0)
                    ctm.end -= utterance.begin
                    phone_intervals.append(to_tg_interval(ctm, file_duration=file_duration))
                except AssertionError:
                    print(file_name)
                    print(utterance.begin, utterance.end, utterance.text)
                    print(utterance.reference_phone_intervals)
                    print(ctm.begin, ctm.end, ctm.label)
            tg.addTier(tgio.IntervalTier("phones", phone_intervals, 0.0, file_duration))
            tg.save(str(tg_file_path), "short_textgrid", includeBlankSpaces=True)
            count += 1
        print(session.query(Utterance).count(), query.count(), count)
