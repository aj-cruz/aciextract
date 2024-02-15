from typing import Generator, Iterator

from .base import ParentExtractorBase
from .fabric_details import FabricInitialization, FabricInventory, FabricTEPPools
from .system_settings import (
    BGPConfig,
    EndpointControls,
    FabricWideSettings,
    ISISPolicy,
    PortTracking,
    MiscConfig,
)
from .fabric_policies import (
    PoliciesPOD,
    PoliciesInterface,
    PoliciesGlobal,
    PoliciesMonitoring,
    PoliciesMACSec,
    PodsPolicyGroup,
    PodsProfiles,
    FabricInterfaces,
)
from .access_policies import (
    AccessPoliciesInterface,
    AccessPoliciesGlobal,
    AccessPoliciesSwitch,
    AccessInterfaces,
    AccessSwitches,
    AccessPhyExtDomains,
    AccessPools,
)


class ExtractInterestingKeys:
    """
    Search the JSON config "files" for dictionaries with specific
    keys we are looking for and save them to a dictionary.
    These are the root keys where all configuration resides.
    """

    def __init__(self, interesting_files: list[dict]) -> None:
        # INTERESTING DATA: The following attributes represent keys in the JSON files that we're searching for
        self.fabricSetupP: list = []  # TEP Pools
        self.fabricNodeIdentPol: list = []  # hostname, node id, serial number
        self.dhcpClient: list = []  # model, version, node role
        self.mgmtMgmtP: list = []  # mgmt IP addresses
        self.fvTenant: list = []  # All Tenant configuration (EPGs, etc.)
        self.fabricInst: list = []  # BGP Route Reflectors, Pod policy, vPC Policy
        self.infraInfra: list = []  # Switch Profiles, vlan pools, int policies
        self.vmmProvP: list = []  # VMM Domains
        self.physDomP: list = []  # Physical Domains
        self.l2extDomP: list = []  # L2 Bridged Domains
        self.fcDomP: list = []  # Fibre Channel Domains
        self.l3extDomP: list = []  # L3 Routed Domains
        self.infraAttEntityP: list = []  # AAEPs
        self.infraFuncP: list = []  # Int Policy Grps
        self.aaaUserEp: list = []  # Fabric Security (FIPS Mode)
        self.ctrlrInst: list = []  # APIC Controller Count & Serial #s

        self._extract_config_(interesting_files)

    def __iter__(self) -> Iterator:
        keys_to_iterate: list = [key for key in self.__dict__.keys()]

        key: str
        for key in keys_to_iterate:
            yield (key, getattr(self, key))

    def to_dict(self) -> dict:
        return dict(iter(self))

    def _extract_config_(self, interesting_files: list[dict]):
        def nested_dict_search(key: str, dictionary: dict) -> Generator:
            """
            Traverses a nested dictionary searching for a key.
            When it finds the key, it returns the key's value.
            """

            for k, v in dictionary.items():
                if k == key:
                    yield v
                elif isinstance(v, dict):
                    for result in nested_dict_search(key, v):
                        yield result
                elif isinstance(v, list):
                    for d in v:
                        if isinstance(d, dict):
                            for result in nested_dict_search(key, d):
                                yield result

        key: str
        for key in self.to_dict().keys():
            for file in interesting_files:
                interesting_data: list = list(nested_dict_search(key, file))
                if interesting_data:
                    setattr(self, key, interesting_data)
                    break
            else:
                pass
                # raise Exception(f"Could not locate key '{key}' in any of the configuration files. Either the Untar operation produced incorrect results or the version of ACI has changed the expected structure.")


class ExtractFabricDetails(ParentExtractorBase):
    """
    Class for extracting fabric details from raw aci config files.
    """

    def __init__(self, raw_configs: dict) -> None:
        super().__init__(raw_configs)
        self.fabric_initialization: dict = FabricInitialization(self.raw_configs).config
        self.fabric_inventory: dict = FabricInventory(self.raw_configs).config
        self.tep_pools: dict = FabricTEPPools(self.raw_configs).config

    def __str__(self) -> str:
        return "ExtractFabricDetails"


class ExtractSystemSettings(ParentExtractorBase):
    """
    Class for extracting System Settings from raw aci config files.
    """

    def __init__(self, raw_configs: dict) -> None:
        super().__init__(raw_configs)
        self.bgp: dict = BGPConfig(self.raw_configs).config
        self.endpoint_controls: dict = EndpointControls(self.raw_configs).config
        self.fabric_wide_settings: dict = FabricWideSettings(self.raw_configs).config
        self.isis_policy: dict = ISISPolicy(self.raw_configs).config
        self.port_tracking: dict = PortTracking(self.raw_configs).config
        self.misc: dict = MiscConfig(self.raw_configs).config

    def __str__(self):
        return "ExtractFabricDetails"


class ExtractFabricPolicies(ParentExtractorBase):
    """
    Class for extracting Fabric Policies from raw aci config files.
    """

    def __init__(self, raw_configs: dict) -> None:
        super().__init__(raw_configs)
        self.policies_pod: dict = PoliciesPOD(self.raw_configs).config
        self.policies_interface: dict = PoliciesInterface(self.raw_configs).config
        self.policies_global: dict = PoliciesGlobal(self.raw_configs).config
        self.policies_monitoring: dict = PoliciesMonitoring(self.raw_configs).config
        self.policies_macsec: dict = PoliciesMACSec(self.raw_configs).config
        self.pods_policy_groups: dict = PodsPolicyGroup(self.raw_configs).config
        self.pods_profiles: dict = PodsProfiles(self.raw_configs).config
        self.interfaces: dict = FabricInterfaces(self.raw_configs).config

    def __str__(self):
        return "ExtractFabricDetails"


class ExtractAccessPolicies(ParentExtractorBase):
    """
    Class for extracting Access Policies from raw aci config files.
    """

    def __init__(self, raw_configs: dict) -> None:
        super().__init__(raw_configs)
        self.policies_interface: dict = AccessPoliciesInterface(self.raw_configs).config
        self.policies_global: dict = AccessPoliciesGlobal(self.raw_configs).config
        self.policies_switch: dict = AccessPoliciesSwitch(self.raw_configs).config
        self.interfaces: dict = AccessInterfaces(self.raw_configs).config
        self.switches: dict = AccessSwitches(self.raw_configs).config
        self.phys_ext_domains: dict = AccessPhyExtDomains(self.raw_configs).config
        self.pools: dict = AccessPools(self.raw_configs).config

    def __str__(self):
        return "ExtractFabricDetails"
