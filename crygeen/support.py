import functools
from _csv import reader
from os import walk

import pygame as pg


def import_csv_layout(path: str):
    with open(path) as level_map:
        terrain_map: list = []
        layout = reader(level_map, delimiter=',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map


def import_folder(path: str, *, scale: bool = False):
    """
    Import a folder of images
    :param path:
    :param scale: enlarging the image to fit the screen
    :return:
    """
    surface_list = []
    for _, __, img_files in walk(path):
        for image in sorted(img_files):
            full_path = f'{path}/{image}'
            image_surface = pg.image.load(full_path).convert_alpha() \
                if image.endswith('.png') \
                else pg.image.load(full_path).convert()

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


if __name__ == '__main__':
    ...
