import json
from pathlib import Path

from pydantic import FilePath

from crygeen.settings import settings


class SaveLoadManager:
    def __init__(self) -> None:
        self.save_load_base_path: str = settings.SAVE_LOAD_BASE_PATH

        self.control_data_path: Path = settings.CONTROL_DATA_PATH

    def write_save(self, data, file_path: FilePath | Path) -> None:
        """
        The function writes the data to a file at the specified path. The data is
        written in JSON format.
        :param data: The data to write to the file. It should be a dictionary.
        :param file_path: The path to the file where the data will be written. This should
                        be a 'PathLike'.
        :return:
        """
        file_path: Path = self.__check_file_path(file_path)
        with open(file_path, 'w') as file:
            json.dump(data, file)

    def __load_existing_save(self, save_file) -> dict | list[list[str, int, str]]:
        save_file: Path = self.__check_file_path(save_file)
        with open(save_file, 'r+') as file:
            data = json.load(file)
        return data

    @staticmethod
    def __check_file_path(file_path: FilePath) -> Path:
        return Path(file_path) if not isinstance(file_path, Path) else file_path

    def load_save(self, save: FilePath) -> dict | list[list[str, int, str]]:
        try:
            save: dict | list[str, int, str] = self.__load_existing_save(save)
        except FileNotFoundError as exc:
            raise exc  # TODO handle exception
        return save

    def set_new_control_key(self, button, new_key: int) -> None:
        data: list[list[str, int, str]] = self.load_save(self.control_data_path)
        data[button.index][1] = new_key
        data[button.index][2] = settings.CONTROL_ALLOWED_KEYS[new_key]
        self.write_save(data, self.control_data_path)
