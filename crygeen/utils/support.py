import functools
from _csv import reader
from os import walk
from pathlib import Path

import pygame as pg
from pydantic import FilePath, BaseModel, validator
from pygame import Surface


class FolderPath(BaseModel):
    path: FilePath
    scale: bool = False

    @validator('path')
    def validate_path(cls, value):
        if not value.is_dir():
            raise ValueError('Invalid folder path')
        return value


def import_csv_layout(path: str):
    with open(path) as level_map:
        terrain_map: list = []
        layout = reader(level_map, delimiter=',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map


def import_folder_img(path: FolderPath | Path, *, scale: bool = False) -> list[Surface]:
    surface_list: list = []
    path: Path = Path(path) if isinstance(path, str) else path
    for image in sorted(path.iterdir()):
        if image.is_file():
            image_surface: Surface = pg.image.load(image).convert_alpha() \
                if image.suffix == '.png' \
                else pg.image.load(image).convert()
            surface_list.append(image_surface)
    return surface_list


def deprecated(func):
    """
    Decorator to mark a function | method as deprecated.
    :param func: func | method need to be deprecated.
    :return:
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f'{func.__name__} is deprecated')
        return func(*args, **kwargs)

    return wrapper


@deprecated
def import_folder_old(path: str, *, scale: bool = False):
    """
    Import a folder of images
    :param path:
    :param scale: enlarging the image to fit the screen
    :return:
    """
    surface_list = []
    for _, __, img_files in walk(path):
        print(_, __, img_files)
        for image in sorted(img_files):
            full_path = f'{path}/{image}'
            image_surface = pg.image.load(full_path).convert_alpha() \
                if image.endswith('.png') \
                else pg.image.load(full_path).convert()

            surface_list.append(image_surface)
    return surface_list


if __name__ == '__main__':
    ...
