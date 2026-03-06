import os
import csv
import time

import soundfile
from praatio import textgrid as tgio


model_training_directory = r"C:\Users\micha\Documents\Data\model_training_corpora"
root_dir = r"D:\Data\experiments\interspeech_benchmarking\model_training_analysis"
languages = [
    "english",
    "czech",
    "spanish",
    "portuguese",
    "russian",
    "serbo-croatian",
]

if __name__ == '__main__':
    os.makedirs(root_dir, exist_ok=True)
    csv_header = ["corpus", "file", "modified_date", "file_format", "manual_alignments","utterance_count"]
    for lang in languages:
        print(lang)
        lang_directory = os.path.join(model_training_directory, lang)
        output_file = os.path.join(root_dir, f"{lang}.csv")
        #if os.path.exists(output_file):
        #    continue
        with open(output_file, 'w', encoding='utf8', newline='') as out_f:
            writer = csv.DictWriter(out_f, fieldnames=csv_header)
            writer.writeheader()
            for corpus in os.listdir(lang_directory):
                print(corpus)
                corpus_path = os.path.join(lang_directory, corpus)
                if not os.path.isdir(corpus_path):
                    continue
                for root, _, file_listing in os.walk(corpus_path):
                    for f in file_listing:
                        name, ext = os.path.splitext(f)
                        manual_alignments = False
                        utterance_count = 1
                        if ext.endswith("TextGrid"):
                            file_format = "TextGrid"
                            tg = tgio.openTextgrid(os.path.join(root, f), includeEmptyIntervals=False)
                            for tn in tg.tierNames:
                                if "phone" in tn:
                                    manual_alignments = True
                                elif "word" not in tn:
                                    utterance_count = len(tg._tierDict[tn]._entries)
                        elif ext.endswith("txt") or ext.endswith("lab"):
                            file_format = "lab"
                        else:
                            continue
                        modified_time = time.localtime(os.path.getmtime(os.path.join(root, f)))
                        modified_date = time.strftime("%Y-%m-%d", modified_time)
                        writer.writerow({"corpus": corpus, "file": name, "modified_date": modified_date, "file_format": file_format, "manual_alignments": manual_alignments, "utterance_count":utterance_count})

