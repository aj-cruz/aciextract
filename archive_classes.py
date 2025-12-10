import json
import xml.etree.ElementTree as ET
import tarfile
from typing import Iterator
from abc import ABC, abstractmethod

import xmltodict  # type: ignore


class ACIUntarBase(ABC):
    def __init__(self, backup_file: str) -> None:
        self.file_name: str = backup_file
        self.files: list[dict] = self._get_files_from_archive_()

    def __str__(self) -> str:
        return self.file_name

    def __iter__(self) -> Iterator:
        return iter(self.files)

    @abstractmethod
    def _get_files_from_archive_(self) -> list:
        """
        Extracts all configuration files from an ACI backup archive.
        NOTE: Extractors must return a list of config dictionaries
        """


class ACIUntarJSON(ACIUntarBase):
    """
    Extracts .json files from an ACI JSON backup file and returns themn as a list of dictionaries.
    """

    def _get_files_from_archive_(self) -> list:
        files: list[dict] = []

        tarball: tarfile.TarFile
        with tarfile.open(self.file_name, "r") as tarball:
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


# BROKEN, NOT IMPLEMENTED YET
class ACIUntarXML(ACIUntarBase):
    def _get_files_from_archive_(self) -> list:
        return []


#         files: list[dict] = []

#         tarball: tarfile.TarFile
#         with tarfile.open(self.file_name, "r") as tarball:
#             # Create a list of XML files in the backup tarball
#             xml_files: list = [
#                 file for file in tarball.getnames() if file.endswith(".xml")
#             ]

#             if not xml_files:
#                 raise ValueError(
#                     "No XML files detected in the backup archive. The backup file might be a JSON backup."
#                 )

#             files = [xmltodict.parse(tarball.extractfile(file).read()) for file in xml_files]  # type: ignore

#         # converted_files = [self._element_to_dict_(ET.fromstring(file)) for file in files]

#         return files

#     def _element_to_dict_(self, element: bytes) -> dict:
#         result: dict = {}
#         for child in element:
#             if child:
#                 if len(child) == 1 and child[0].tag == child.tag:
#                     if child.tag in result:
#                         if isinstance(result[child.tag], list):
#                             result[child.tag].append(self._element_to_dict_(child))
#                         else:
#                             result[child.tag] = [
#                                 result[child.tag],
#                                 self._element_to_dict_(child),
#                             ]
#                     else:
#                         result[child.tag] = self._element_to_dict_(child)
#                 else:
#                     if child.tag in result:
#                         if not isinstance(result[child.tag], list):
#                             result[child.tag] = [result[child.tag]]
#                         result[child.tag].append(self._element_to_dict_(child))
#                     else:
#                         result[child.tag] = self._element_to_dict_(child)
#             else:
#                 result[child.tag] = child.text.strip() if child.text else None

#         return result
