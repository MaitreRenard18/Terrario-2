from typing import List
import pickle
import os

import pygame.image

from .map import Map

from pathlib import Path
MODULE_PATH = Path(__file__).parent.parent

if "Saves" not in os.listdir(MODULE_PATH):
    os.mkdir(MODULE_PATH / "Saves")

if "Thumbnails" not in os.listdir(MODULE_PATH / "Images"):
    os.mkdir(MODULE_PATH / "Images/Thumbnails")
 
_saves_path = MODULE_PATH / "saves"
_thumbnail_path = MODULE_PATH / "images" / "thumbnail"


def get_saves() -> List[str]:
    return [file for file in os.listdir(_saves_path) if not file.endswith(".png")]


def save(file_name, map: Map) -> None:
    with open(_saves_path / file_name, "wb") as file:
        thumbnail = map.get_thumbnail()
        pygame.image.save_extended(thumbnail, _thumbnail_path / f"{file_name}.png")
        pickle.dump(map, file)


def load(file_name: str) -> Map:
    with open(_saves_path / file_name, "rb") as file:
        return pickle.load(file)
