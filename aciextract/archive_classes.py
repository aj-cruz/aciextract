import json
import tarfile
from typing import Iterator


class ACIUntarBase:
    def __init__(self, backup_file: str) -> None:
        self.file_name: str = backup_file
        self.files: list[dict] = self._get_files_from_archive_()

    def __str__(self) -> str:
        return self.file_name

    def __iter__(self) -> Iterator:
        return iter(self.files)

    def _get_files_from_archive_(self) -> list:
        """
        Extracts files from an ACI backup and returns them as a list of dictionaries
        NOTE: If an XML extractor is created, it must convert the data to dicitonaries/JSON
        """
        raise NotImplementedError


class ACIUntarJSON(ACIUntarBase):
    """
    Extracts .json files from an ACI JSON backup file and returns themn as a list of dictionaries.
    """

    def _get_files_from_archive_(self) -> list:
        files: list[dict] = []

        tarball: tarfile.TarFile
        with tarfile.open(self.file_name, "r") as tarball:
            file: str

            # Create a list of JSON files in the backup tarball
            json_files: list = [
                file for file in tarball.getnames() if file.endswith(".json")
            ]

            if not json_files:
                raise ValueError(
                    "No JSON files detected in the backup archive. The backup file might be an XML backup."
                )

            # Create a list of dicts: Extract each file and load it as a dictionary
            files = [json.loads(tarball.extractfile(file).read()) for file in json_files]  # type: ignore

        return files
