import json
from typing import Iterator

from .archive_classes import ACIUntarJSON
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
        self.interesting_files: list = list(ACIUntarJSON(backup_file))
        self.raw_configs: dict = ExtractInterestingKeys(
            self.interesting_files
        ).to_dict()
        self.fabric_details: dict = ExtractFabricDetails(self.raw_configs).to_dict()
        self.system_settings: dict = ExtractSystemSettings(self.raw_configs).to_dict()
        self.fabric_policies: dict = ExtractFabricPolicies(self.raw_configs).to_dict()
        self.access_policies: dict = ExtractAccessPolicies(self.raw_configs).to_dict()
        self.tenants: list = self.raw_configs["fvTenant"]

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
