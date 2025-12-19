import json
import tarfile
from typing import Iterator

from .archive_classes import ACIUntarBase, ACIUntarJSON, ACIUntarXML
from .extractor_classes import (
    ExtractInterestingKeys,
    ExtractFabricDetails,
    ExtractSystemSettings,
    ExtractFabricPolicies,
    ExtractAccessPolicies,
)


class ACIConfig:
    def __init__(self, backup_file: str) -> None:
        self.backup_file: str = backup_file
        self.interesting_files: list = list(self._get_extractor_())
        self.raw_configs: dict = ExtractInterestingKeys(
            self.interesting_files
        ).to_dict()
        self.fabric_details: dict = ExtractFabricDetails(self.raw_configs).to_dict()
        self.system_settings: dict = ExtractSystemSettings(self.raw_configs).to_dict()
        self.fabric_policies: dict = ExtractFabricPolicies(self.raw_configs).to_dict()
        self.access_policies: dict = ExtractAccessPolicies(self.raw_configs).to_dict()
        self.tenants: list = self.raw_configs["fvTenant"]
        self.virtual_networking: list = self.raw_configs["vmmProvP"]

    def __str__(self) -> str:
        return self.backup_file

    def __iter__(self) -> Iterator:
        exclude_attributes: list = ["interesting_files", "raw_configs"]
        keys_to_iterate: list = [
            key for key in self.__dict__.keys() if not key in exclude_attributes
        ]

        key: str
        for key in keys_to_iterate:
            yield (key, getattr(self, key))

    def _get_extractor_(self) -> ACIUntarBase:
        """Validate backup archive and determine which Untar subclass to use"""

        tarball: tarfile.TarFile
        with tarfile.open(self.backup_file, "r") as tarball:
            # Create a list of JSON & XML files in the backup tarball
            json_files: list = [
                file for file in tarball.getnames() if file.endswith(".json")
            ]
            xml_files: list = [
                file for file in tarball.getnames() if file.endswith(".xml")
            ]

        if json_files:
            return ACIUntarJSON(self.backup_file)
        elif xml_files:
            raise Exception("XML backup parsing not yet implemented")
            # return ACIUntarXML(self.backup_file)
        else:
            raise ValueError(
                f"Unable to locate JSON or XML files in the archive. {self.backup_file} doesn't appear to be a valid ACI Config Backup."
            )

    def to_dict(self) -> dict:
        return dict(iter(self))

    def pretty_print(self, obj=None) -> None:
        if not obj:
            return print(json.dumps(dict(self), indent=4))
        elif isinstance(obj, (dict, list)):
            return print(json.dumps(obj, indent=4))
        else:
            print(str(obj))

    def write(self, obj: dict | None = None) -> None:
        def writer(obj) -> None:
            with open("config.json", "w") as f:
                f.write(json.dumps(obj, indent=4))

        if not obj:
            writer(dict(self))
        elif isinstance(obj, (list, dict)):
            writer(obj)
