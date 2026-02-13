import os

from montreal_forced_aligner.command_line.mfa import mfa_cli

root_dir = r"D:\Data\experiments\interspeech_benchmarking"
mfa_models_acoustic_directory = r"C:\Users\micha\Documents\Dev\mfa-models\config\acoustic"
phone_groups_directory = os.path.join(mfa_models_acoustic_directory, "phone_groups")
rules_directory = r"C:\Users\micha\Documents\Dev\mfa-interspeech2026\data\rules"
config_directory = r"C:\Users\micha\Documents\Dev\mfa-interspeech2026\data\config"
topologies_directory = os.path.join(mfa_models_acoustic_directory, "topologies")
mfa_models_training_path = r"C:\Users\micha\Documents\Dev\mfa-models\dictionary\training"
remapped_directory = os.path.join(root_dir, "models", "trained")
mfa10_dir = r"D:\Data\models\1.0_archived"
mfa20_dir = r"D:\Data\models\2.0_archived"
mfa20a_dir = r"D:\Data\models\2.0.0a_archived"
mfa21_dir = r"D:\Data\models\2.1_trained"
mfa22_dir = r"D:\Data\models\2.2_trained"
mfa30_dir = r"D:\Data\models\3.0_trained"
mfa31_dir = r"D:\Data\models\3.1_trained"
adapted_directory = os.path.join(root_dir, "models", "adapted")
trained22_dir = r"D:\Data\models\2.2_trained\buckeye"
trained30_dir = r"D:\Data\models\3.0_trained\buckeye"
mapping_directory = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "mapping_files"
)
english_mfa_model_path = os.path.join(mfa31_dir, "english_mfa.zip")

corpus_directories = {
    "timit": r"D:\Data\speech\benchmark_datasets\timit\timit_benchmark",
    "buckeye": r"D:\Data\speech\benchmark_datasets\buckeye\buckeye_corpus_lab",
    "csj": r"D:\Data\speech\benchmark_datasets\csj\csj_lab",
    "seoul_corpus": r"D:\Data\speech\benchmark_datasets\seoul_corpus\seoul_corpus_lab",
}

corpus_languages = {
    "timit": "english",
    "buckeye": "english",
    "csj": "japanese",
    "seoul_corpus": "korean",
}

conditions = {
    "timit": {
        "mfa_trained": {
            "dictionary_path": os.path.join(mfa_models_training_path, "english_us_mfa.dict"),
            "g2p_path": "english_us_mfa",
            "phone_groups_path": os.path.join(phone_groups_directory, "english_mfa.yaml"),
        },
        "mfa_trained_rules": {
            "dictionary_path": os.path.join(mfa_models_training_path, "english_us_mfa.dict"),
            "g2p_path": "english_us_mfa",
            "phone_groups_path": os.path.join(phone_groups_directory, "english_mfa.yaml"),
            "rules_path": os.path.join(rules_directory, "english_mfa.yaml"),
        },
        "arpa_trained": {
            "dictionary_path": os.path.join(mfa_models_training_path, "english_us_arpa.dict"),
            "g2p_path": "english_us_arpa",
            "phone_groups_path": os.path.join(phone_groups_directory, "english_arpa.yaml"),
        },
        "arpa_trained_rules": {
            "dictionary_path": os.path.join(mfa_models_training_path, "english_us_arpa.dict"),
            "g2p_path": "english_us_arpa",
            "phone_groups_path": os.path.join(phone_groups_directory, "english_arpa.yaml"),
            "rules_path": os.path.join(rules_directory, "english_arpa.yaml"),
        },
    },
    "buckeye": {
        "mfa_trained": {
            "dictionary_path": os.path.join(mfa_models_training_path, "english_us_mfa.dict"),
            "g2p_path": "english_us_mfa",
            "phone_groups_path": os.path.join(phone_groups_directory, "english_mfa.yaml"),
        },
        "mfa_trained_no_pronunciation_probability": {
            "dictionary_path": os.path.join(mfa_models_training_path, "english_us_mfa.dict"),
            "g2p_path": "english_us_mfa",
            "phone_groups_path": os.path.join(phone_groups_directory, "english_mfa.yaml"),
            "config_path": os.path.join(config_directory, "no_pronunciation_probability.yaml"),
        },
        "mfa_trained_rules": {
            "dictionary_path": os.path.join(mfa_models_training_path, "english_us_mfa.dict"),
            "g2p_path": "english_us_mfa",
            "phone_groups_path": os.path.join(phone_groups_directory, "english_mfa.yaml"),
            "rules_path": os.path.join(rules_directory, "english_mfa.yaml"),
        },
        "arpa_trained": {
            "dictionary_path": os.path.join(mfa_models_training_path, "english_us_arpa.dict"),
            "g2p_path": "english_us_arpa",
            "phone_groups_path": os.path.join(phone_groups_directory, "english_arpa.yaml"),
            "config_path": os.path.join(config_directory, "no_pronunciation_probability.yaml"),
        },
        "arpa_trained_no_pronunciation_probability": {
            "dictionary_path": os.path.join(mfa_models_training_path, "english_us_arpa.dict"),
            "g2p_path": "english_us_arpa",
            "phone_groups_path": os.path.join(phone_groups_directory, "english_arpa.yaml"),
        },
        "arpa_trained_rules": {
            "dictionary_path": os.path.join(mfa_models_training_path, "english_us_arpa.dict"),
            "g2p_path": "english_us_arpa",
            "phone_groups_path": os.path.join(phone_groups_directory, "english_arpa.yaml"),
            "rules_path": os.path.join(rules_directory, "english_arpa.yaml"),
        },
    },
    "csj": {
        "mfa_trained": {
            "dictionary_path": os.path.join(mfa_models_training_path, "japanese_mfa.dict"),
            "g2p_path": "japanese_mfa",
            "phone_groups_path": os.path.join(phone_groups_directory, "japanese_mfa.yaml"),
            "language": "japanese",
        },
        "mfa_trained_no_pronunciation_probability": {
            "dictionary_path": os.path.join(mfa_models_training_path, "japanese_mfa.dict"),
            "g2p_path": "japanese_mfa",
            "phone_groups_path": os.path.join(phone_groups_directory, "japanese_mfa.yaml"),
            "language": "japanese",
            "config_path": os.path.join(config_directory, "no_pronunciation_probability.yaml"),
        },
        "mfa_trained_rules": {
            "dictionary_path": os.path.join(mfa_models_training_path, "japanese_mfa.dict"),
            "g2p_path": "japanese_mfa",
            "phone_groups_path": os.path.join(phone_groups_directory, "japanese_mfa.yaml"),
            "rules_path": os.path.join(rules_directory, "japanese_mfa.yaml"),
            "language": "japanese",
        },
    },
    "seoul_corpus": {
        "mfa_trained": {
            "dictionary_path": os.path.join(mfa_models_training_path, "korean_mfa.dict"),
            "g2p_path": os.path.join(mfa30_dir, "korean_jamo_mfa.zip"),
            "phone_groups_path": os.path.join(phone_groups_directory, "korean_mfa.yaml"),
            "language": "korean",
        },
        "mfa_trained_no_pronunciation_probability": {
            "dictionary_path": os.path.join(mfa_models_training_path, "korean_mfa.dict"),
            "g2p_path": os.path.join(mfa30_dir, "korean_jamo_mfa.zip"),
            "phone_groups_path": os.path.join(phone_groups_directory, "korean_mfa.yaml"),
            "language": "korean",
            "config_path": os.path.join(config_directory, "no_pronunciation_probability.yaml"),
        },
        "mfa_trained_rules": {
            "dictionary_path": os.path.join(mfa_models_training_path, "korean_mfa.dict"),
            "g2p_path": os.path.join(mfa30_dir, "korean_jamo_mfa.zip"),
            "phone_groups_path": os.path.join(phone_groups_directory, "korean_mfa.yaml"),
            "rules_path": os.path.join(rules_directory, "korean_mfa.yaml"),
            "language": "korean",
        },
    }
}

if __name__ == "__main__":
    for corpus, root in corpus_directories.items():
        print(corpus)
        lang = corpus_languages[corpus]

        for condition, data in conditions[corpus].items():
            dictionary_path = data["dictionary_path"]
            phone_groups_path = data.get("phone_groups_path", None)
            phone_remapping_path = data.get("phone_remapping_path", None)
            config_path = data.get("config_path", None)
            language = data.get("language", None)
            remapped_dictionary_path = os.path.join(remapped_directory, f"{corpus}_english_mfa.dict")
            g2p_model_path = os.path.join(remapped_directory, f"{corpus}_english_mfa.zip")
            if not os.path.exists(remapped_dictionary_path):
                command = ['remap_dictionary',
                           str(dictionary_path),
                           str(english_mfa_model_path),
                           str(phone_remapping_path),
                           str(remapped_dictionary_path),
                           '--clean',
                           ]
                print(command)
                mfa_cli(command, standalone_mode=False)
            if not os.path.exists(g2p_model_path):
                command = [
                    "train_g2p",
                    str(remapped_dictionary_path),
                    str(g2p_model_path),
                    "-j",
                    "10",
                    "--clean",
                    "--no_debug",
                    "--use_mp",
                    "--phonetisaurus",
                ]
                if language == 'korean':
                    command += [
                    "--unicode_decomposition",
                    "True"]
                print(command)
                mfa_cli(command, standalone_mode=False)
            output_directory = os.path.join(root_dir, "alignments", corpus, f"{condition}")
            if os.path.exists(output_directory):
                continue
            print(condition)
            model_path = english_mfa_model_path
            if "adapt" in condition:
                os.makedirs(adapted_directory, exist_ok=True)
                output_model_path = os.path.join(
                    adapted_directory, corpus, condition, f"{condition}.zip"
                )
                if not os.path.exists(output_model_path):
                    command = [
                        "adapt",
                        root,
                        str(remapped_dictionary_path),
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
                    if g2p_model_path:
                        command += ["--g2p_model_path",
                        g2p_model_path,]
                    print(command)
                    mfa_cli(command, standalone_mode=False)
                model_path = output_model_path
            command = [
                "align",
                root,
                remapped_dictionary_path,
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
            if g2p_model_path:
                command += ["--g2p_model_path",
                g2p_model_path,]
            print(command)
            mfa_cli(command, standalone_mode=False)
