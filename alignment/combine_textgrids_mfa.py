import os
import shutil

from praatio import textgrid as tgio

root_dir = r"D:\Data\experiments\interspeech_benchmarking"
output_dir = r"D:\Data\experiments\interspeech_benchmarking\temp\combined_mfa"

corpus_directories = {
    "timit": r"D:\Data\speech\benchmark_datasets\timit\timit_benchmark",
    "buckeye": r"D:\Data\speech\benchmark_datasets\buckeye\buckeye_corpus_lab",
    "csj": r"D:\Data\speech\benchmark_datasets\csj\csj_lab",
    "seoul_corpus": r"D:\Data\speech\benchmark_datasets\seoul_corpus\seoul_corpus_lab",
}

reference_directories = {
    #"timit": r"D:\Data\speech\benchmark_datasets\timit\timit_reference",
    #"buckeye": r"D:\Data\speech\benchmark_datasets\buckeye\buckeye_corpus_lab_reference",
    "csj": r"D:\Data\speech\benchmark_datasets\csj\csj_lab_reference",
    "seoul_corpus": r"D:\Data\speech\benchmark_datasets\seoul_corpus\seoul_corpus_lab_reference",
}

if __name__ == '__main__':
    for corpus, reference_directory in reference_directories.items():
        corpus_alignment_directory = os.path.join(root_dir, "alignments", corpus)
        for speaker in os.listdir(reference_directory):
            speaker_dir = os.path.join(reference_directory, speaker)
            output_speaker_dir = os.path.join(output_dir, corpus, speaker)
            os.makedirs(output_speaker_dir, exist_ok=True)
            for f in os.listdir(speaker_dir):
                tg_path = os.path.join(speaker_dir, f)
                output_path = os.path.join(output_speaker_dir, f)
                output_wav_path = os.path.join(output_speaker_dir, f.replace('.TextGrid', '.wav'))
                original_wav_path = os.path.join(corpus_directories[corpus], speaker, f.replace('.TextGrid', '.wav'))
                if not os.path.exists(output_wav_path):
                    shutil.copyfile(original_wav_path, output_wav_path)
                tg = tgio.openTextgrid(tg_path, includeEmptyIntervals=False)
                for e in os.listdir(corpus_alignment_directory):
                    if "mfa" not in e:
                        continue
                    aligned_file = os.path.join(corpus_alignment_directory, e, speaker, f)
                    e_name = e # .replace("_adapted", '')
                    aligned_word_tier = tgio.IntervalTier(f"{e_name} - words", [],
                                                          tg.minTimestamp, tg.maxTimestamp)
                    aligned_phone_tier = tgio.IntervalTier(f"{e_name} - phones", [],
                                                          tg.minTimestamp, tg.maxTimestamp)
                    if os.path.exists(aligned_file):
                        aligned_tg = tgio.openTextgrid(aligned_file, includeEmptyIntervals=False)
                        for t_name in aligned_tg.tierNames:
                            if 'word' in t_name:
                                aligned_word_tier = tgio.IntervalTier(f"{e_name} - words", aligned_tg._tierDict[t_name]._entries, tg.minTimestamp, tg.maxTimestamp)
                            elif 'phone' in t_name:
                                aligned_phone_tier = tgio.IntervalTier(f"{e_name} - phones", aligned_tg._tierDict[t_name]._entries, tg.minTimestamp, tg.maxTimestamp)
                    tg.addTier(aligned_word_tier)
                    tg.addTier(aligned_phone_tier)
                tg.save(output_path, "short_textgrid", includeBlankSpaces=True)
