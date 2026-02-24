import os

from montreal_forced_aligner.command_line.mfa import mfa_cli

root_dir = r"D:\Data\experiments\interspeech_benchmarking"
mfa10_dir = r"D:\Data\models\1.0_archived"
mfa20_dir = r"D:\Data\models\2.0_archived"
mfa20a_dir = r"D:\Data\models\2.0.0a_archived"
mfa21_dir = r"D:\Data\models\2.1_trained"
mfa22_dir = r"D:\Data\models\2.2_trained"
mfa30_dir = r"D:\Data\models\3.0_trained"
mfa31_dir = r"D:\Data\models\3.1_trained"
adapted_dir = r"D:\Data\models\adapted"
trained22_dir = r"D:\Data\models\2.2_trained\buckeye"
trained30_dir = r"D:\Data\models\3.0_trained\buckeye"
mapping_directory = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "mapping_files"
)

conditions = {
    "buckeye": {"mfa_3.1": (
        os.path.join(mfa31_dir, "english_us_mfa.dict"),
        os.path.join(mfa31_dir, "english_mfa.zip"),
        "english_us_mfa",
    ),
        "mfa_3.1_finetune": (
            os.path.join(mfa31_dir, "english_us_mfa.dict"),
            os.path.join(mfa31_dir, "english_mfa.zip"),
        "english_us_mfa",
        ),
        "mfa_3.1_adapted": (
            os.path.join(mfa31_dir, "english_us_mfa.dict"),
            os.path.join(mfa31_dir, "english_mfa.zip"),
        "english_us_mfa",
        ),
        "mfa_3.1_adapted_finetune": (
            os.path.join(mfa31_dir, "english_us_mfa.dict"),
            os.path.join(mfa31_dir, "english_mfa.zip"),
        "english_us_mfa",
        ),
        "arpa_3.0": (
            os.path.join(mfa30_dir, "english_us_arpa.dict"),
            os.path.join(mfa30_dir, "english_us_arpa.zip"),
        "english_us_arpa",
        ),
        "arpa_3.0_finetune": (
            os.path.join(mfa30_dir, "english_us_arpa.dict"),
            os.path.join(mfa30_dir, "english_us_arpa.zip"),
        "english_us_arpa",
        ),
        "arpa_3.0_adapted": (
            os.path.join(mfa30_dir, "english_us_arpa.dict"),
            os.path.join(mfa30_dir, "english_us_arpa.zip"),
        "english_us_arpa",
        ),
        "arpa_3.0_adapted_finetune": (
            os.path.join(mfa30_dir, "english_us_arpa.dict"),
            os.path.join(mfa30_dir, "english_us_arpa.zip"),
        "english_us_arpa",
        ), },
    "timit": {"mfa_3.1": (
        os.path.join(mfa31_dir, "english_us_mfa.dict"),
        os.path.join(mfa31_dir, "english_mfa.zip"),
        "english_us_mfa",
    ),
        "mfa_3.1_finetune": (
            os.path.join(mfa31_dir, "english_us_mfa.dict"),
            os.path.join(mfa31_dir, "english_mfa.zip"),
        "english_us_mfa",
        ),
        "mfa_3.1_adapted": (
            os.path.join(mfa31_dir, "english_us_mfa.dict"),
            os.path.join(mfa31_dir, "english_mfa.zip"),
        "english_us_mfa",
        ),
        "mfa_3.1_adapted_finetune": (
            os.path.join(mfa31_dir, "english_us_mfa.dict"),
            os.path.join(mfa31_dir, "english_mfa.zip"),
        "english_us_mfa",
        ),
        "arpa_3.0": (
            os.path.join(mfa30_dir, "english_us_arpa.dict"),
            os.path.join(mfa30_dir, "english_us_arpa.zip"),
        "english_us_arpa",
        ),
        "arpa_3.0_finetune": (
            os.path.join(mfa30_dir, "english_us_arpa.dict"),
            os.path.join(mfa30_dir, "english_us_arpa.zip"),
        "english_us_arpa",
        ),
        "arpa_3.0_adapted": (
            os.path.join(mfa30_dir, "english_us_arpa.dict"),
            os.path.join(mfa30_dir, "english_us_arpa.zip"),
        "english_us_arpa",
        ),
        "arpa_3.0_adapted_finetune": (
            os.path.join(mfa30_dir, "english_us_arpa.dict"),
            os.path.join(mfa30_dir, "english_us_arpa.zip"),
        "english_us_arpa",
        ), },
    "csj": {
        "mfa_3.1": (os.path.join(mfa30_dir, "japanese_mfa.dict"), os.path.join(mfa30_dir, "japanese_mfa.zip"), "japanese_mfa"),
        "mfa_3.1_finetune": (os.path.join(mfa30_dir, "japanese_mfa.dict"), os.path.join(mfa30_dir, "japanese_mfa.zip"), "japanese_mfa"),
        "mfa_3.1_adapted": (os.path.join(mfa30_dir, "japanese_mfa.dict"), os.path.join(mfa30_dir, "japanese_mfa.zip"), "japanese_mfa"),
        "mfa_3.1_adapted_finetune": (os.path.join(mfa30_dir, "japanese_mfa.dict"), os.path.join(mfa30_dir, "japanese_mfa.zip"), "japanese_mfa"),
    },
    "seoul_corpus": {
    'gp_1.0': (os.path.join(mfa10_dir, 'KO_dictionary.txt'), os.path.join(mfa10_dir, "korean.zip")),
        "mfa_3.1": (os.path.join(mfa30_dir, "korean_mfa.dict"), os.path.join(mfa30_dir, "korean_mfa.zip"), "korean_mfa"),
        "mfa_3.1_finetune": (os.path.join(mfa30_dir, "korean_mfa.dict"), os.path.join(mfa30_dir, "korean_mfa.zip"), "korean_mfa"),
        "mfa_3.1_adapted": (os.path.join(mfa30_dir, "korean_mfa.dict"), os.path.join(mfa30_dir, "korean_mfa.zip"), "korean_mfa"),
        "mfa_3.1_adapted_finetune": (os.path.join(mfa30_dir, "korean_mfa.dict"), os.path.join(mfa30_dir, "korean_mfa.zip"), "korean_mfa"),
    }
}

reference_directories = {
    "timit": r"D:\Data\speech\benchmark_datasets\timit\timit_reference",
    "buckeye": r"D:\Data\speech\benchmark_datasets\buckeye\buckeye_corpus_lab_reference",
    "csj": r"D:\Data\speech\benchmark_datasets\csj\csj_lab_reference",
    "seoul_corpus": r"D:\Data\speech\benchmark_datasets\seoul_corpus\seoul_corpus_lab_reference",
}

audio_directories = {
    "timit": r"D:\Data\speech\benchmark_datasets\timit\timit_benchmark",
    "buckeye": r"D:\Data\speech\benchmark_datasets\buckeye\buckeye_corpus_lab",
    "csj": r"D:\Data\speech\benchmark_datasets\csj\csj_lab",
    "seoul_corpus": r"D:\Data\speech\benchmark_datasets\seoul_corpus\seoul_corpus_lab",
}

if __name__ == "__main__":
    for corpus, reference_directory in reference_directories.items():
        alignment_root = os.path.join(root_dir, "alignments", corpus)
        for condition in os.listdir(alignment_root):
            alignment_directory = os.path.join(alignment_root, condition)
            output_directory = os.path.join(root_dir, "evaluation_data", corpus, condition)
            if "arpa" in condition:
                phone_set = "arpa"
            elif "mfa" in condition:
                phone_set = "mfa"
            elif "gp" in condition:
                phone_set = 'gp'
            else:
                phone_set = condition
            if "remapped" in condition:
                phone_set = "english_mfa"
            mapping_file = os.path.join(
                mapping_directory, f"{phone_set}_{corpus}_mapping.yaml"
            )
            if not os.path.exists(mapping_file):
                print(f"MISSING {mapping_file}")
                error
            if not os.path.exists(output_directory):
                command = ['compare_alignments',
                           reference_directory,
                           alignment_directory,
                           output_directory,
                           "--custom_mapping_path",
                           mapping_file,
                           '--clean',
                           '-j', '10',
                           '--use_mp',
                           '--no_final_clean',
                           "--strict_mapping",
                           ]
                print(command)
                mfa_cli(command, standalone_mode=False)
                #error