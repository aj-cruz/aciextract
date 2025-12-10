from .base import ChildExtractorBase, dict_extractor


class PoliciesPOD(ChildExtractorBase):
    def _extract_config_(self) -> None:
        # DATE AND TIME POD POLICIES
        self.config["date_time"] = dict_extractor(
            self.raw_configs, "fabricInst", "datetimePol"
        )

        # SNMP POD POLICIES
        self.config["snmp"] = dict_extractor(self.raw_configs, "fabricInst", "snmpPol")


class PoliciesInterface(ChildExtractorBase):
    def _extract_config_(self) -> None:
        # L3 INTERFACE INTERFACE POLICIES
        self.config["l3_interface"] = dict_extractor(
            self.raw_configs, "fabricInst", "l3IfPol"
        )

        # LINK LEVEL INTERFACE POLICIES
        self.config["link_level"] = dict_extractor(
            self.raw_configs, "fabricInst", "fabricFIfPol"
        )

        # DWDM INTERFACE POLICIES
        self.config["dwdm"] = dict_extractor(
            self.raw_configs, "fabricInst", "dwdmFabIfPol"
        )

        # LINK FLAP INTERFACE POLICIES
        self.config["link_flap"] = dict_extractor(
            self.raw_configs, "fabricInst", "fabricFLinkFlapPol"
        )

        # ZR TRANSCEIVER INTERFACE POLICIES
        self.config["zr_transceiver"] = dict_extractor(
            self.raw_configs, "fabricInst", "xcvrZRFabIfPol"
        )

        # ZRP TRANSCEIVER INTERFACE POLICIES
        self.config["zrp_transceiver"] = dict_extractor(
            self.raw_configs, "fabricInst", "xcvrZRPFabIfPol"
        )


class PoliciesGlobal(ChildExtractorBase):
    def _extract_config_(self) -> None:
        # DNS PROFILES
        self.config["dns_profile"] = dict_extractor(
            self.raw_configs, "fabricInst", "dnsProfile"
        )

        # FABRIC L2 MTU
        self.config["fabric_l2_mtu"] = dict_extractor(
            self.raw_configs, "fabricInst", "l2InstPol"
        )


class PoliciesMonitoring(ChildExtractorBase):
    def _extract_config_(self) -> None:
        # FABRIC NODE CONTROLS POLICIES
        self.config["fabric_node_control"] = dict_extractor(
            self.raw_configs, "fabricInst", "fabricNodeControl"
        )


class PoliciesMACSec(ChildExtractorBase):
    def _extract_config_(self) -> None:
        # MACSEC INTERFACE POLICIES
        self.config["interface"] = dict_extractor(
            self.raw_configs, "fabricInst", "macsecFabIfPol"
        )

        # MACSEC PARAMETER POLICIES
        self.config["parameter"] = dict_extractor(
            self.raw_configs, "fabricInst", "macsecFabPolCont", "macsecFabParamPol"
        )

        # MACSEC KEYCHAINS
        self.config["keychain"] = dict_extractor(
            self.raw_configs, "fabricInst", "macsecFabPolCont", "macsecKeyChainPol"
        )


class PodsPolicyGroup(ChildExtractorBase):
    def _extract_config_(self) -> None:
        # POD POLICY GROUPS
        self.config["groups"] = dict_extractor(
            self.raw_configs, "fabricInst", "fabricFuncP", "fabricPodPGrp"
        )


class PodsProfiles(ChildExtractorBase):
    def _extract_config_(self) -> None:
        # POD PROFILES
        self.config["profile"] = dict_extractor(
            self.raw_configs, "fabricInst", "fabricPodP"
        )


class FabricInterfaces(ChildExtractorBase):
    def _extract_config_(self) -> None:
        # SPINE POLICY GROUPS
        self.config["spine_policy_group"] = dict_extractor(
            self.raw_configs, "fabricInst", "fabricFuncP", "fabricSpPortPGrp"
        )

        # SPINE PROFILES
        self.config["spine_profile"] = dict_extractor(
            self.raw_configs, "fabricInst", "fabricSpPortP"
        )

        # LEAF POLICY GROUPS
        self.config["leaf_policy_group"] = dict_extractor(
            self.raw_configs, "fabricInst", "fabricFuncP", "fabricLePortPGrp"
        )

        # LEAF PROFILES
        self.config["leaf_profile"] = dict_extractor(
            self.raw_configs, "fabricInst", "fabricLePortP"
        )
