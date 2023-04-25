from typing import List
import pickle
import os

import pygame.image

from .constants import MODULE_PATH

if "Saves" not in os.listdir(MODULE_PATH):
    os.mkdir(MODULE_PATH / "Saves")

if "Thumbnails" not in os.listdir(MODULE_PATH / "Images"):
    os.mkdir(MODULE_PATH / "Images/Thumbnails")
 
_saves_path: str = MODULE_PATH / "saves"
_thumbnail_path: str = MODULE_PATH / "images" / "thumbnails"


def get_saves() -> List[str]:
    return [file for file in os.listdir(_saves_path) if not file.endswith(".png")]

from .map import Map
def save(file_name, map: Map) -> None:
    with open(_saves_path / file_name, "wb") as file:
        thumbnail = map.get_thumbnail()
        pygame.image.save_extended(thumbnail, _thumbnail_path / f"{file_name}.png")
        pickle.dump(map, file)


def load(file_name: str) -> Map:
    with open(_saves_path / file_name, "rb") as file:
        return pickle.load(file)
