"""
A simple script to swap between Rasa formats md and json
"""
import os
from os import listdir, path

from tqdm import tqdm

# from constants import DATA_DIR

PROJECT_NAME = "GDA"
MODEL_NAME = "AOD"

parent = path.dirname(path.dirname(__file__))
dir_path = path.join(parent, "data", "weather")  # PROJECT_NAME, MODEL_NAME, "intents")


def transform_format_rasa(dst_ext):

    """
    It transform the text to rasa format and it executes rasa process.
    :param dst_ext: str
    """

    files = listdir(dir_path)

    for idx, file in enumerate(tqdm(files)):
        os.system(
            f"rasa data convert nlu "
            f'--data "{path.join(dir_path, file)}" '
            f'--out "{path.join(dir_path, path.splitext(file)[0])}.{dst_ext}" --format {dst_ext}'
        )


if __name__ == "__main__":
    transform_format_rasa(dst_ext="md")
