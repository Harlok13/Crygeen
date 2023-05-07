import json
import os
from pathlib import Path

import pygame as pg
from pydantic import FilePath

from crygeen.settings import settings


class SaveLoadManager:
    def __init__(self) -> None:
        self.save_file = os.path.join(os.getcwd(), 'save.json')

        self.save_load_base_path: str = settings.SAVE_LOAD_BASE_PATH

        # self.control_data_path: str = settings.CONTROL_DATA_PATH
        # self.name_control_file: str = settings.NAME_CONTROL_FILE

    def write_save(self, data: dict, file_path: FilePath) -> None:
        """
        The function writes the data to a file at the specified path. The data is
        written in JSON format.
        :param data: The data to write to the file. It should be a dictionary.
        :param file_path: The path to the file where the data will be written. This should
                        be a 'PathLike'.
        :return:
        """
        file_path = Path(file_path) if not isinstance(file_path, Path) else file_path
        with open(os.path.join(self.save_load_base_path, file_path), 'w') as file:
            json.dump(data, file)

    @staticmethod
    def __load_existing_save(save_file) -> dict:
        with open(os.path.join(save_file), 'r+') as file:
            data = json.load(file)
        return data

    def load_save(self, save) -> dict:
        try:
            save: dict = self.__load_existing_save(save)
        except FileNotFoundError as exc:
            raise exc  # TODO handle exception
        return save

    def create_control_save(self):
        pass

