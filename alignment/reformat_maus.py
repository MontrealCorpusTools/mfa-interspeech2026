import os
from praatio import textgrid as tgio
from praatio.utilities.constants import Interval as PraatInterval

root_dir = r"D:\Data\experiments\interspeech_benchmarking"
output_dir = r"D:\Data\experiments\interspeech_benchmarking\temp"

corpus_directories = {
    #"timit": r"D:\Data\speech\benchmark_datasets\timit\timit_benchmark",
    #"buckeye": r"D:\Data\speech\benchmark_datasets\buckeye\buckeye_corpus_lab",
    "csj": r"D:\Data\speech\benchmark_datasets\csj\csj_lab",
    #"seoul_corpus": r"D:\Data\speech\benchmark_datasets\seoul_corpus\seoul_corpus_lab",
}

def reformat_textgrid(tg_path):
    tg = tgio.openTextgrid(tg_path, includeEmptyIntervals=False)
    new_tg = tgio.Textgrid()
    old_word_tier = tg._tierDict["ORT-MAU"]
    old_phone_tier = tg._tierDict["MAU"]
    word_tier = tgio.IntervalTier(
        f"{speaker} - words",
        old_word_tier._entries,
        old_word_tier.minTimestamp,
        old_word_tier.maxTimestamp
    )
    phone_tier = tgio.IntervalTier(
        f"{speaker} - phones",
        [x for x in old_phone_tier._entries if x.label != "<p:>"],
        old_phone_tier.minTimestamp,
        old_phone_tier.maxTimestamp
    )
    new_tg.addTier(word_tier)
    new_tg.addTier(phone_tier)
    return new_tg

if __name__ == "__main__":
    for corpus in corpus_directories.keys():
        alignment_directory = os.path.join(root_dir, "alignments", corpus, "maus")
        if not os.path.exists(alignment_directory):
            continue
        if corpus == 'timit':
            for f in os.listdir(alignment_directory):
                if not f.endswith('.TextGrid'):
                    continue
                speaker = f.rsplit("_", maxsplit=1)[0]
                speaker_dir = os.path.join(alignment_directory, speaker)
                os.makedirs(speaker_dir, exist_ok=True)
                output_path = os.path.join(speaker_dir, f)
                if os.path.exists(output_path):
                    continue
                tg_path = os.path.join(alignment_directory, f)
                try:
                    new_tg = reformat_textgrid(tg_path)
                except KeyError:
                    continue
                new_tg.save(output_path, "short_textgrid", includeBlankSpaces=True)
        else:
            for speaker in os.listdir(alignment_directory):
                speaker_dir = os.path.join(alignment_directory, speaker)
                for f in os.listdir(speaker_dir):
                    if not f.endswith('.TextGrid'):
                        continue
                    tg_path = os.path.join(speaker_dir, f)
                    try:
                        new_tg = reformat_textgrid(tg_path)
                    except KeyError:
                        continue
                    new_tg.save(tg_path, "short_textgrid", includeBlankSpaces=True)


