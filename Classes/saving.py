from typing import List
import pickle
import os

from .map import Map

from pathlib import Path
MODULE_PATH = Path(__file__).parent.parent

if "Saves" not in os.listdir(MODULE_PATH):
    os.mkdir(MODULE_PATH / "Saves")

_saves_path = MODULE_PATH / "saves"


def get_saves() -> List[str]:
    return os.listdir(_saves_path)


def save(file_name, map: Map) -> None:
    with open(_saves_path / file_name, "wb") as file:
        pickle.dump(map, file)


def load(file_name: str) -> Map:
    with open(_saves_path / file_name, "rb") as file:
        return pickle.load(file)
