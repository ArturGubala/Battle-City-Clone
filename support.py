from os import walk
from typing import List
import pygame

from settings import PlayerSettings


def import_folder(path: str) -> List:
    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.transform.scale(
                pygame.image.load(full_path).convert_alpha(), PlayerSettings.PLAYER_SIZE)
            surface_list.append(image_surf)

    return surface_list
