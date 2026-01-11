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
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "mapping_files"
)

corpus_directories = {
    "timit": r"D:\Data\speech\benchmark_datasets\timit\timit_benchmark",
    "buckeye": r"D:\Data\speech\benchmark_datasets\buckeye\buckeye_corpus_lab",
}

conditions = {
    "mfa_3.1": (
        os.path.join(mfa31_dir, "english_us_mfa.dict"),
        os.path.join(mfa31_dir, "english_mfa.zip"),
    ),
    "mfa_3.1_finetune": (
        os.path.join(mfa31_dir, "english_us_mfa.dict"),
        os.path.join(mfa31_dir, "english_mfa.zip"),
    ),
    "mfa_3.1_adapted": (
        os.path.join(mfa31_dir, "english_us_mfa.dict"),
        os.path.join(mfa31_dir, "english_mfa.zip"),
    ),
    "mfa_3.1_adapted_finetune": (
        os.path.join(mfa31_dir, "english_us_mfa.dict"),
        os.path.join(mfa31_dir, "english_mfa.zip"),
    ),
    "arpa_3.0": (
        os.path.join(mfa30_dir, "english_us_arpa.dict"),
        os.path.join(mfa30_dir, "english_us_arpa.zip"),
    ),
    "arpa_3.0_finetune": (
        os.path.join(mfa30_dir, "english_us_arpa.dict"),
        os.path.join(mfa30_dir, "english_us_arpa.zip"),
    ),
    "arpa_3.0_adapted": (
        os.path.join(mfa30_dir, "english_us_arpa.dict"),
        os.path.join(mfa30_dir, "english_us_arpa.zip"),
    ),
    "arpa_3.0_adapted_finetune": (
        os.path.join(mfa30_dir, "english_us_arpa.dict"),
        os.path.join(mfa30_dir, "english_us_arpa.zip"),
    ),
}

if __name__ == "__main__":
    for condition, (dictionary_path, model_path) in conditions.items():
        print(condition)
        for corpus, root in corpus_directories.items():
            output_directory = os.path.join(root_dir, "alignments", corpus, condition)
            if os.path.exists(output_directory):
                continue
            if not os.path.exists(model_path):
                continue
            if not os.path.exists(dictionary_path):
                continue
            if "adapt" in condition:
                os.makedirs(adapted_dir, exist_ok=True)
                output_model_path = os.path.join(
                    adapted_dir, f"{condition.replace('_finetune', '')}.zip"
                )
                if not os.path.exists(output_model_path):
                    command = [
                        "adapt",
                        root,
                        str(dictionary_path),
                        str(model_path),
                        str(output_model_path),
                        "-j",
                        "10",
                        "--clean",
                        "--no_debug",
                        "--use_mp",
                        "--use_cutoff_model",
                        "--use_postgres",
                        "--beam",
                        "10",
                        "--retry_beam",
                        "40",
                    ]
                    print(command)
                    mfa_cli(command, standalone_mode=False)
                model_path = output_model_path
            command = [
                "align",
                root,
                dictionary_path,
                model_path,
                output_directory,
                "-j",
                "10",
                "--clean",
                "--no_debug",
                "--use_mp",
                "--use_cutoff_model",
                "--use_postgres",
                "--beam",
                "10",
                "--retry_beam",
                "40",
            ]
            if "finetune" in condition:
                command += ["--fine_tune"]
            print(command)
            mfa_cli(command, standalone_mode=False)
