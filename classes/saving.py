from typing import List, TYPE_CHECKING
import pickle
import os


import pygame.image
from pygame import Surface

from .constants import MODULE_PATH, screen
if TYPE_CHECKING:
    from classes.map import Map


# Créer un dossier "saves" stockant les sauvegardes des mondes
if "saves" not in os.listdir(MODULE_PATH):
    os.mkdir(MODULE_PATH / "saves")
    
# Créer un dossier "thumbnails" stockant les miniatures des mondes
if "thumbnails" not in os.listdir(MODULE_PATH / "images"):
    os.mkdir(MODULE_PATH / "images/thumbnails")
 
# Stock le chemin des différents dossiers
_saves_path: str = MODULE_PATH / "saves"
_thumbnail_path: str = MODULE_PATH / "images" / "thumbnails"

    
def get_thumbnail() -> Surface:
    """
    Retourne une surface au format 1:1 de ce qui est actuellement affiché sur l'écran.
    """

    if screen.get_width() > screen.get_height():
        return screen.subsurface((
            screen.get_width() // 2 - screen.get_height() // 2, 0,
            screen.get_height(), screen.get_height()))

    else:
        return screen.subsurface((
            0, screen.get_height() // 2 - screen.get_width() // 2,
            screen.get_width(), screen.get_width()))

    
def get_saves() -> List[str]:
    """
    Retourne une liste contenant le nom de toutes les sauvegardes.
    """
    
    return [file for file in os.listdir(_saves_path) if not file.endswith(".png")]


def save(file_name, map: "Map") -> None:
    """
    Sauvegarde la Map passée en paramètre dans le fichier du nom également passé en paramètre.
    """
    
    with open(_saves_path / file_name, "wb") as file:
        thumbnail = get_thumbnail()
        pygame.image.save_extended(thumbnail, _thumbnail_path / f"{file_name}.png")
        pickle.dump(map, file)


def load(file_name: str) -> "Map":
    """
    Charge le fichier passé en paramètre.
    """
    
    with open(_saves_path / file_name, "rb") as file:
        return pickle.load(file)
