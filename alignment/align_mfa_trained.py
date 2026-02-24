import os

from montreal_forced_aligner.command_line.mfa import mfa_cli

root_dir = r"D:\Data\experiments\interspeech_benchmarking"
mfa_models_acoustic_directory = r"C:\Users\micha\Documents\Dev\mfa-models\config\acoustic"
phone_groups_directory = os.path.join(mfa_models_acoustic_directory, "phone_groups")
rules_directory = r"C:\Users\micha\Documents\Dev\mfa-interspeech2026\data\rules"
config_directory = r"C:\Users\micha\Documents\Dev\mfa-interspeech2026\data\config"
topologies_directory = os.path.join(mfa_models_acoustic_directory, "topologies")
mfa_models_training_path = r"C:\Users\micha\Documents\Dev\mfa-models\dictionary\training"
trained_directory = os.path.join(root_dir, "models", "trained")
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
        },
        "arpa_trained_rules": {
            "dictionary_path": os.path.join(mfa_models_training_path, "english_us_arpa.dict"),
            "g2p_path": "english_us_arpa",
            "phone_groups_path": os.path.join(phone_groups_directory, "english_arpa.yaml"),
            "rules_path": os.path.join(rules_directory, "english_arpa.yaml"),
        },
        "arpa_trained_no_pronunciation_probability": {
            "dictionary_path": os.path.join(mfa_models_training_path, "english_us_arpa.dict"),
            "g2p_path": "english_us_arpa",
            "phone_groups_path": os.path.join(phone_groups_directory, "english_arpa.yaml"),
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
            "g2p_path": os.path.join(mfa30_dir, "g2p", "korean_mfa.zip"),
            "phone_groups_path": os.path.join(phone_groups_directory, "korean_mfa.yaml"),
            "language": "korean",
        },
        "mfa_trained_no_pronunciation_probability": {
            "dictionary_path": os.path.join(mfa_models_training_path, "korean_mfa.dict"),
            "g2p_path": os.path.join(mfa30_dir, "g2p", "korean_mfa.zip"),
            "phone_groups_path": os.path.join(phone_groups_directory, "korean_mfa.yaml"),
            "language": "korean",
            "config_path": os.path.join(config_directory, "no_pronunciation_probability.yaml"),
        },
        "mfa_trained_rules": {
            "dictionary_path": os.path.join(mfa_models_training_path, "korean_mfa.dict"),
            "g2p_path": os.path.join(mfa30_dir, "g2p", "korean_mfa.zip"),
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
            g2p_path = data.get("g2p_path", None)
            phone_groups_path = data.get("phone_groups_path", None)
            rules_path = data.get("rules_path", None)
            config_path = data.get("config_path", None)
            language = data.get("language", None)
            trained_model_path = os.path.join(trained_directory, corpus, condition, f"{lang}.zip")
            trained_dictionary_path = os.path.join(trained_directory, corpus, condition, dictionary_path.split("\\")[-1])
            if not os.path.exists(trained_model_path):
                command = [
                    "train",
                        root,
                        str(dictionary_path),
                        str(trained_model_path),
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
                        "--oov_count_threshold",
                        "0",
                ]
                if g2p_path:
                    command += ["--g2p_model_path",
                    g2p_path,]
                if phone_groups_path:
                    command += ["--phone_groups_path",
                    phone_groups_path,]
                if rules_path:
                    command += ["--rules_path",
                    rules_path,]
                if config_path:
                    command += ["--config_path",
                    config_path,]
                if language:
                    command += ["--language", language]
                print(command)
                mfa_cli(command, standalone_mode=False)

            output_directory = os.path.join(root_dir, "alignments", corpus, f"{condition}")
            if os.path.exists(output_directory):
                continue
            print(condition)
            if not os.path.exists(trained_dictionary_path):
                trained_dictionary_path = dictionary_path
            command = [
                "align",
                root,
                trained_dictionary_path,
                trained_model_path,
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
            if g2p_path:
                command += ["--g2p_model_path",
                g2p_path,]
            print(command)
            mfa_cli(command, standalone_mode=False)
