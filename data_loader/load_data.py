import numpy as np
import os
import json
import torch
np.random.seed(100)

class DataPreprocessor:
    """
    A class to load and preprocess JSON files.
    """
    def __init__(self):
        pass
    def __call__(self, path):
        """
        Loads and parses JSON data from a file.
        :param path: Path to the JSON file.
        :return: Parsed JSON data.
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)

class Extract_Information:
    """
    A class to extract track information from JSON data.
    """
    def __init__(self):
        self.playlists = {}
    def extract_tracks(self, data):
        """
        Extracts track information from JSON data.
        :param data: Parsed JSON data.
        :return: Dictionary of playlist names and their corresponding track information.
        """
        playlists = data.get("playlists", [])
        for playlist in playlists:
            playlist_name = playlist.get("name")
            tracks = playlist.get("tracks", [])
            track_info = [
                {
                    "artist_name": track.get("artist_name"),
                    "track_name": track.get("track_name"),
                    "album_name": track.get("album_name")
                }
                for track in tracks
            ]
            self.playlists[playlist_name] = track_info
        return self.playlists

def process_folder(folder_path, preprocessor, extractor):
    """
    Processes all JSON files in a folder and extracts track information.
    :param folder_path: Path to the folder containing JSON files.
    :param preprocessor: An instance of the DataPreprocessor class.
    :param extractor: An instance of the Extract_Information class.
    :return: Dictionary of playlist names and their corresponding track information.
    """
    files = os.listdir(folder_path)
    all_playlists = {}
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path) and file_name.endswith(".json"):
            data = preprocessor(file_path)
            all_playlists[file_path] = extractor.extract_tracks(data)
    return all_playlists

def create_loader(path_type, batch_size):
    """
    Creates a PyTorch DataLoader for loading and preprocessing JSON files.
    :param path_type: Type of JSON files.
    :param batch_size: Batch size for the DataLoader.
    :return: PyTorch DataLoader.
    """
    preprocessor = DataPreprocessor()
    extractor = Extract_Information()
    train_samples = process_folder(f'{path_type}/data',preprocessor, extractor)
    return train_samples