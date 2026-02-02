import os
from praatio import textgrid as tgio
from praatio.utilities.constants import Interval

root_dir = r"D:\Data\experiments\interspeech_benchmarking"
output_dir = r"D:\Data\experiments\interspeech_benchmarking\temp"

corpus_directories = {
    "seoul_corpus": r"D:\Data\speech\benchmark_datasets\seoul_corpus\seoul_corpus_lab",
}

def reformat_textgrid(tg_path):
    tg = tgio.openTextgrid(tg_path, includeEmptyIntervals=False)
    new_tg = tgio.Textgrid()
    old_word_tier = tg._tierDict["word"]
    old_phone_tier = tg._tierDict["phone"]
    word_tier = tgio.IntervalTier(
        f"{speaker} - words",
        [Interval(round(x[0], 3), round(x[1], 3), x[2]) for x in old_word_tier._entries if x.label not in {"sil", "sp", "SIL", "SP"}],
        old_word_tier.minTimestamp,
        old_word_tier.maxTimestamp
    )
    phone_tier = tgio.IntervalTier(
        f"{speaker} - phones",
        [Interval(round(x[0], 3), round(x[1], 3), x[2]) for x in old_phone_tier._entries if x.label not in {"sil", "sp", "SIL", "SP"}],
        old_phone_tier.minTimestamp,
        old_phone_tier.maxTimestamp
    )
    new_tg.addTier(word_tier)
    new_tg.addTier(phone_tier)
    return new_tg

if __name__ == "__main__":
    for corpus in corpus_directories.keys():
        alignment_directory = os.path.join(root_dir, "alignments", corpus, "koreanforcedaligner")
        if not os.path.exists(alignment_directory):
            continue
        print(corpus)
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
                except Exception:
                    print(f)
                    raise
                new_tg.save(tg_path, "short_textgrid", includeBlankSpaces=True)


