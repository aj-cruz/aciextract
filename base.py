from typing import Iterator
from abc import ABC, abstractmethod


def dict_extractor(dictionary: dict, base_key: str, *args) -> list:
    """
    Takes a nested dictionary and a number of keys as inputs and traverses
    the nested dictionary searching for the keys.
    Assumes each key has a 'children' list where the additional keys are nested.
    Returns a list of the keys matching the final key.

    Example dictionary:
    {
    base_key: {
      children: [
        key2: {
          children: [
            key3: {},
            key3: {}
          ]
        }
      ]
    }
    }

    Example usage:
    list_extractor(a_dictionary, 'base_key', 'key2', 'key3')

    The example command with the example dictionary would return:
    [
      key3: {},
      key3: {}
    ]
    """

    list_comp_str: str
    list_comp_str = f"[child{len(args)}['{args[-1]}']"
    list_comp_str += f" for each in dictionary['{base_key}']"
    i: int
    each: str
    for i, each in enumerate(args, start=1):
        if i == 1:
            list_comp_str += f" for child{i} in each['children']"
        else:
            list_comp_str += f" for child{i} in child{i-1}['{args[i-2]}']['children']"
        list_comp_str += f" if '{each}' in child{i}"
    list_comp_str += "]"

    results: list
    try:
        results = eval(list_comp_str)
    except KeyError:
        results = []
    except IndexError:
        results = []

    return results


class ParentExtractorBase(ABC):
    """
    Class for extracting fabric details from raw aci config files.
    Parent Extractor represents major areas of the ACI GUI (System Settings, Fabric Policies, etc).
    It is an aggregator (composition) for specific 'Child' Extractors that perform the config extractions.
    """

    def __init__(self, raw_configs: dict) -> None:
        self.raw_configs: dict = raw_configs
        "Child Extractors will be implemented by subclasses via super()"

    @abstractmethod
    def __str__(self) -> str:
        pass

    def __iter__(self) -> Iterator:
        exclude_attributes: list = ["raw_configs"]
        keys_to_iterate: list = [
            key for key in self.__dict__.keys() if not key in exclude_attributes
        ]

        key: str
        for key in keys_to_iterate:
            yield (key, getattr(self, key))

    def to_dict(self) -> dict:
        return dict(iter(self))


class ChildExtractorBase(ABC):
    """
    Class for extracting fabric details from raw aci config files.
    Child Extractor represents specific areas of the ACI GUI (Leaf Interface Profiles, etc).
    It holds the logic for the config extraction and roll up to Parent Extractors via composition.
    """

    def __init__(self, raw_configs: dict) -> None:
        self.raw_configs: dict = raw_configs
        self.config: dict = {}

        self._extract_config_()

    @abstractmethod
    def _extract_config_(self) -> None:
        """Extraction logic implemented by subclasses"""
        pass
