from .base import ChildExtractorBase


class BGPConfig(ChildExtractorBase):
    def _extract_config_(self) -> None:
        # Extract the BGP Policy Name
        bgp_policy_name: str
        try:
            bgp_policy_name = [
                child["bgpInstPol"]["attributes"]["name"]
                for each in self.raw_configs["fabricInst"]
                for child in each["children"]
                if "bgpInstPol" in child
            ][0]
        except KeyError:
            bgp_policy_name = ""
        except IndexError:
            bgp_policy_name = ""

        # Extract the BGP ASN
        bgp_asn: str
        try:
            bgp_asn = [
                rr["bgpAsP"]["attributes"]["asn"]
                for each in self.raw_configs["fabricInst"]
                for child in each["children"]
                if "bgpInstPol" in child
                for rr in child["bgpInstPol"]["children"]
                if "bgpAsP" in rr
            ][0]
        except IndexError:
            bgp_asn = "No BGP ASN Configured"

        # Extract the BGP Route Reflectors
        bgp_rrs: list
        try:
            bgp_rrs = sorted(
                [
                    f"pod-{node['bgpRRNodePEp']['attributes']['podId']}/spine-{node['bgpRRNodePEp']['attributes']['id']}"
                    for each in self.raw_configs["fabricInst"]
                    for child in each["children"]
                    if "bgpInstPol" in child
                    for rr in child["bgpInstPol"]["children"]
                    if "bgpRRP" in rr
                    for node in rr["bgpRRP"]["children"]
                    if "bgpRRNodePEp" in node
                ]
            )
        except KeyError as e:
            if str(e) == "'children'":
                bgp_rrs = ["No Route Reflectors Configured"]
            else:
                raise KeyError(str(e))

        self.config = {
            "bgp_policy_name": bgp_policy_name,
            "bgp_asn": bgp_asn,
            "bgp_route_reflectors": bgp_rrs,
        }


class EndpointControls(ChildExtractorBase):
    def _extract_config_(self) -> None:
        # EP LOOP PROTECTION
        ep_loop_protection: dict = [
            child["epLoopProtectP"]["attributes"]
            for child in self.raw_configs["infraInfra"][0]["children"]
            if "epLoopProtectP" in child
        ][0]
        self.config["ep_loop_protection"] = {
            "adminSt": ep_loop_protection["adminSt"],
            "loopDetectIntvl": ep_loop_protection["loopDetectIntvl"],
            "loopDetectMult": ep_loop_protection["loopDetectMult"],
            "action": ep_loop_protection["action"],
        }

        # ROGUE EP CONTROL
        rogue_ep_control: dict = [
            child["epControlP"]["attributes"]
            for child in self.raw_configs["infraInfra"][0]["children"]
            if "epControlP" in child
        ][0]
        self.config["rogue_ep_control"] = {
            "adminSt": rogue_ep_control["adminSt"],
            "rogueEpDetectIntvl": rogue_ep_control["rogueEpDetectIntvl"],
            "rogueEpDetectMult": rogue_ep_control["rogueEpDetectMult"],
            "holdIntvl": rogue_ep_control["holdIntvl"],
        }

        # IP AGING
        ip_aging: dict = [
            child["epIpAgingP"]["attributes"]
            for child in self.raw_configs["infraInfra"][0]["children"]
            if "epIpAgingP" in child
        ][0]
        self.config["ip_aging"] = {
            "adminSt": ip_aging["adminSt"],
        }


class FabricWideSettings(ChildExtractorBase):
    def _extract_config_(self) -> None:
        fabric_wide_settings: dict = [
            child["infraSetPol"]["attributes"]
            for child in self.raw_configs["infraInfra"][0]["children"]
            if "infraSetPol" in child
        ][0]

        # ATTEMPT TO SET ATTRIBUTES THAT MAY NOT EXIST ON OLDER VESIONS OF ACI
        enforce_subnet_check: str
        try:
            enforce_subnet_check = fabric_wide_settings["enforceSubnetCheck"]
        except KeyError:
            enforce_subnet_check = "unsupported attribute"
        enforce_epg_vlan_validation: str
        try:
            enforce_epg_vlan_validation = fabric_wide_settings[
                "validateOverlappingVlans"
            ]
        except KeyError:
            enforce_epg_vlan_validation = "unsupported attribute"
        leaf_opflex_client_auth: str
        try:
            leaf_opflex_client_auth = fabric_wide_settings[
                "leafOpflexpAuthenticateClients"
            ]
        except KeyError:
            leaf_opflex_client_auth = "unsupported attribute"
        leaf_ssl_opflex: str
        try:
            leaf_ssl_opflex = fabric_wide_settings["leafOpflexpUseSsl"]
        except KeyError:
            leaf_ssl_opflex = "unsupported attribute"
        ssl_opflex_versions: str
        try:
            ssl_opflex_versions = fabric_wide_settings["opflexpSslProtocols"]
        except KeyError:
            ssl_opflex_versions = "unsupported attribute"
        restrict_infra_vlan_traffic: str
        try:
            restrict_infra_vlan_traffic = fabric_wide_settings[
                "restrictInfraVLANTraffic"
            ]
        except KeyError:
            restrict_infra_vlan_traffic = "unsupported attribute"

        self.config = {
            "disable_remote_ep_learning": fabric_wide_settings[
                "unicastXrEpLearnDisable"
            ],
            "enforce_subnet_check": enforce_subnet_check,
            "enforce_epg_vlan_validation": enforce_epg_vlan_validation,
            "enforce_domain_validation": fabric_wide_settings["domainValidation"],
            "spine_opflex_client_auth": fabric_wide_settings[
                "opflexpAuthenticateClients"
            ],
            "leaf_opflex_client_auth": leaf_opflex_client_auth,
            "spine_ssl_opflex": fabric_wide_settings["opflexpUseSsl"],
            "leaf_ssl_opflex": leaf_ssl_opflex,
            "ssl_opflex_versions": ssl_opflex_versions,
            "reallocate_gipo": fabric_wide_settings["reallocateGipo"],
            "restrict_infra_vlan_traffic": restrict_infra_vlan_traffic,
        }


class ISISPolicy(ChildExtractorBase):
    def _extract_config_(self) -> None:
        isis_config: dict = [
            child["isisDomPol"]
            for child in self.raw_configs["fabricInst"][0]["children"]
            if "isisDomPol" in child
        ][0]

        self.config = {
            "mtu": isis_config["attributes"]["mtu"],
            "redistribMetric": isis_config["attributes"]["redistribMetric"],
            "lspFastFlood": isis_config["children"][0]["isisLvlComp"]["attributes"][
                "lspFastFlood"
            ],
            "lspGenInitIntvl": isis_config["children"][0]["isisLvlComp"]["attributes"][
                "lspGenInitIntvl"
            ],
            "lspGenMaxIntvl": isis_config["children"][0]["isisLvlComp"]["attributes"][
                "lspGenMaxIntvl"
            ],
            "lspGenSecIntvl": isis_config["children"][0]["isisLvlComp"]["attributes"][
                "lspGenSecIntvl"
            ],
            "spfCompInitIntvl": isis_config["children"][0]["isisLvlComp"]["attributes"][
                "spfCompInitIntvl"
            ],
            "spfCompMaxIntvl": isis_config["children"][0]["isisLvlComp"]["attributes"][
                "spfCompMaxIntvl"
            ],
            "spfCompSecIntvl": isis_config["children"][0]["isisLvlComp"]["attributes"][
                "spfCompSecIntvl"
            ],
        }


class PortTracking(ChildExtractorBase):
    def _extract_config_(self) -> None:
        port_tracking: dict = [
            child["infraPortTrackPol"]["attributes"]
            for child in self.raw_configs["infraInfra"][0]["children"]
            if "infraPortTrackPol" in child
        ][0]

        # ATTEMPT TO SET ATTRIBUTES THAT MAY NOT EXIST ON OLDER VESIONS OF ACI
        includeApicPorts: str
        try:
            includeApicPorts = port_tracking["includeApicPorts"]
        except KeyError:
            includeApicPorts = "unsupported attribute"

        self.config = {
            "adminSt": port_tracking["adminSt"],
            "delay": port_tracking["delay"],
            "minlinks": port_tracking["minlinks"],
            "includeApicPorts": includeApicPorts,
        }


class MiscConfig(ChildExtractorBase):
    def _extract_config_(self) -> None:
        # APIC CONNECTIVITY PREFERENCES
        mgmt_prefs: dict = [
            child["mgmtConnectivityPrefs"]["attributes"]
            for child in self.raw_configs["fabricInst"][0]["children"]
            if "mgmtConnectivityPrefs" in child
        ][0]
        self.config["apic_conn_pref"] = mgmt_prefs["interfacePref"]

        # CONTROL PLANE MTU
        cp_mtu: dict = [
            child["infraCPMtuPol"]["attributes"]
            for child in self.raw_configs["infraInfra"][0]["children"]
            if "infraCPMtuPol" in child
        ][0]
        self.config["control_plane_mtu"] = cp_mtu["CPMtu"]

        # COOP GROUP TYPE
        coop_grp: dict = [
            child["coopPol"]["attributes"]
            for child in self.raw_configs["fabricInst"][0]["children"]
            if "coopPol" in child
        ][0]
        self.config["coop_group_type"] = coop_grp["type"]

        # FABRIC SECURITY - FIPS MODE
        fips_mode: dict = [
            child["aaaFabricSec"]["attributes"]
            for child in self.raw_configs["aaaUserEp"][0]["children"]
            if "aaaFabricSec" in child
        ][0]
        self.config["fips_mode"] = fips_mode["fipsMode"]

        # GLOBAL AES ENCRYPTION
        # This does not show up in the config files and will have to be gathered manually

        # SYSTEM GLOBAL GIPO POLICY
        glob_gipo_pol: dict = [
            child["fmcastSystemGIPoPol"]["attributes"]
            for child in self.raw_configs["infraInfra"][0]["children"]
            if "fmcastSystemGIPoPol" in child
        ][0]
        self.config["useConfiguredSystemGIPo"] = glob_gipo_pol[
            "useConfiguredSystemGIPo"
        ]
