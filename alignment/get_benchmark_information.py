from pathlib import Path

import sqlalchemy
from montreal_forced_aligner import config

config.USE_POSTGRES = False
config.CLEAN = True
config.QUIET = True

from montreal_forced_aligner.corpus.acoustic_corpus import AcousticCorpus
from montreal_forced_aligner.db import Utterance

corpus_directories = {
    "timit": r"D:\Data\speech\benchmark_datasets\timit\timit_benchmark",
    "buckeye": r"D:\Data\speech\benchmark_datasets\buckeye\buckeye_corpus_lab",
    "csj": r"D:\Data\speech\benchmark_datasets\csj\csj_lab",
    "seoul_corpus": r"D:\Data\speech\benchmark_datasets\seoul_corpus\seoul_corpus_lab",
}

for corpus, root in corpus_directories.items():
    print(corpus)
    print("=" * len(corpus))
    c = AcousticCorpus(corpus_directory=root)
    c._load_corpus()
    print("Num utterances:", c.num_utterances)
    print("Num files:", c.num_files)
    print("Num speakers:", c.num_speakers)
    with c.session() as session:
        total_duration = (
            session.query(sqlalchemy.func.sum(Utterance.duration))
            .filter(Utterance.text != "")
            .first()[0]
            / 3600
        )
    print("Num hours:", total_duration)
    print()
