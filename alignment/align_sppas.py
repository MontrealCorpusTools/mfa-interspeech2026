import os
import sys
import unicodedata

from praatio import textgrid as tgio
import soundfile as sf
from praatio.utilities.constants import Interval as PraatInterval
# If there's a SPPAS environment variable
SPPAS = os.getenv("SPPAS")
if SPPAS is None:
    SPPAS = r"C:\Users\micha\Downloads\SPPAS-4.30-2025-12-21"
sys.path.append(SPPAS)
os.environ['PATH'] += f';{SPPAS}'
from sppas.core.coreutils import u
from sppas.src.annotations.TextNorm.sppastextnorm import sppasTextNorm
from sppas.src.annotations.TextNorm.normalize import TextNormalizer
from sppas.src.annotations.Phon.sppasphon import sppasPhon
from sppas.src.annotations.Align.sppasalign import sppasAlign
from sppas.src.annotations.Align.aligners import JuliusAligner
from sppas.src.resources.vocab import sppasVocabulary
from sppas.src.resources.dictpron import sppasDictPron

from sppas.src.annotations.Phon.phonetize import sppasDictPhonetizer

root_dir = r"D:\Data\experiments\interspeech_benchmarking"

sppas_model_dir = r"C:\Users\micha\Downloads\SPPAS-4.30-2025-12-21\resources"


corpus_directories = {
    "timit": r"D:\Data\speech\benchmark_datasets\timit\timit_benchmark",
    "buckeye": r"D:\Data\speech\benchmark_datasets\buckeye\buckeye_corpus_lab",
    "csj": r"D:\Data\speech\benchmark_datasets\csj\csj_lab",
}

def parse_julius_output(output_path):
    with open(output_path, 'r', encoding='utf8') as f:
        skip = True
        phone_intervals = []
        for line in f:
            line = line.strip()
            if "ALIGN: === phoneme alignment begin ===" in line:
                skip = False
                continue
            if skip:
                continue
            if line.startswith("phseq1:"):
                prons = line.lstrip("phseq1:").split("|")
                prons = [x.strip() for x in prons]
            elif line.startswith("sentence1:"):
                words = line.lstrip("sentence1::").split()
            elif line.startswith('['):
                line = line.replace('[', '').replace(']', '').split()
                beg = (int(line[0]) + 1)/ 100
                end = (int(line[1]) + 2) / 100
                label = line[-1]
                phone_intervals.append((beg, end, label))
        word_intervals = []
        current_index = 0
        current_intervals = []
        for w, pron in zip(words,prons):
            for i in range(current_index, len(phone_intervals)):
                p = phone_intervals[i]
                current_intervals.append(p)
                if ' '.join(x[-1] for x in current_intervals) == pron:
                    current_index = i + 1
                    break
            word_intervals.append((current_intervals[0][0], current_intervals[-1][1], w))
            current_intervals = []
    os.remove(output_path)
    return word_intervals, phone_intervals


if __name__ == "__main__":
    for corpus, root in corpus_directories.items():
        print(corpus)
        lang = 'eng'
        if corpus == 'csj':
            lang = 'jpn'
        elif corpus == 'seoul_corpus':
            lang = 'kor'
        output_directory = os.path.join(root_dir, "alignments", corpus, "sppas")
        vocab_dir = os.path.join(sppas_model_dir, "vocab")
        vocab_file = os.path.join(vocab_dir, f"{lang}.vocab")
        punct_file = os.path.join(vocab_dir, "Punctuations.txt")
        wds = sppasVocabulary(vocab_file)
        puncts = sppasVocabulary(punct_file)
        tok = TextNormalizer(wds, lang)
        tok.set_punct(puncts)
        dd = sppasDictPron(os.path.join(sppas_model_dir, 'dict', f"{lang}.dict"))
        grph = sppasDictPhonetizer(dd)
        aligner = JuliusAligner(os.path.join(sppas_model_dir, 'models', f"models-{lang}"))

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
                with open(text_path, encoding='utf8') as inf:
                    text = inf.read()
                    if lang == 'kor':
                        text = unicodedata.normalize("NFKD", text)
                tokenized = ['#'] + tok.normalize(u(text)) + ['#']
                phones = []
                filtered_tokenized = []
                for t in tokenized:
                    p = grph.get_phon_entry(t)
                    if t == 'ー' and p == 'dummy':
                        phones[-1] += ":"
                        filtered_tokenized[-1] += t
                    else:
                        phones.append(p)
                        filtered_tokenized.append(t)
                tokenized = filtered_tokenized
                aligner.set_phones(" ".join(phones))
                aligner.set_tokens(" ".join(tokenized))
                try:
                    aligner.run_alignment(audio_path, output_path)
                    word_intervals, phone_intervals = parse_julius_output(output_path + ".palign")
                    info = sf.info(audio_path)
                    tg = tgio.Textgrid(minTimestamp=0, maxTimestamp=info.duration)
                    tg.addTier(tgio.IntervalTier(f"{speaker} - words", word_intervals, 0,info.duration))
                    tg.addTier(tgio.IntervalTier(f"{speaker} - phones", phone_intervals, 0,info.duration))
                    tg.save(output_path, "short_textgrid", True)
                except Exception:
                    print(f)
                    continue
                finally:
                    os.remove(text_path.replace('.txt', '.dfa'))
                    os.remove(text_path.replace('.txt', '.dict'))