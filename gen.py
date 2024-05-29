import pickle
import shutil
from typing import Dict

from helpers.utils import MovieMetadata, export_data_to_csv

with open("movie_metadata.pkl", "rb") as file:
    data: Dict[str, MovieMetadata] = pickle.load(file)


export_data_to_csv(data, "dataset.csv")
