from .base import ChildExtractorBase, dict_extractor


class AccessPoliciesSwitch(ChildExtractorBase):
    def _extract_config_(self) -> None:
        # 802.1X NODE AUTHENTICATION POLICIES
        self.config["dot1x_node_auth"] = dict_extractor(
            self.raw_configs, "infraInfra", "l2NodeAuthPol"
        )

        # BFD IPV4 POLICIES
        self.config["bfd_ipv4"] = dict_extractor(
            self.raw_configs, "infraInfra", "bfdIpv4InstPol"
        )

        # BFD IPV6 POLICIES
        self.config["bfd_ipv6"] = dict_extractor(
            self.raw_configs, "infraInfra", "bfdIpv6InstPol"
        )

        # BFD MULTIHOP IPV4 POLICIES
        self.config["bfd_multihop_ipv4"] = dict_extractor(
            self.raw_configs, "infraInfra", "bfdMhIpv4InstPol"
        )

        # BFD MULTIHOP IPV6 POLICIES
        self.config["bfd_multihop_ipv6"] = dict_extractor(
            self.raw_configs, "infraInfra", "bfdMhIpv6InstPol"
        )

        # COPP LEAF POLICIES
        self.config["leaf_copp"] = dict_extractor(
            self.raw_configs, "infraInfra", "coppLeafProfile"
        )

        # COPP LEAF PRE-FILTER POLICIES
        self.config["leaf_copp_prefilter"] = dict_extractor(
            self.raw_configs, "infraInfra", "iaclLeafProfile"
        )

        # COPP SPINE POLICIES
        self.config["spine_copp"] = dict_extractor(
            self.raw_configs, "infraInfra", "coppSpineProfile"
        )

        # COPP SPINE PRE-FILTER POLICIES
        self.config["spine_copp_prefilter"] = dict_extractor(
            self.raw_configs, "infraInfra", "iaclSpineProfile"
        )

        # EQUIPMENT FLASH CONFIG POLICIES
        self.config["equipment_flash_conf"] = dict_extractor(
            self.raw_configs, "infraInfra", "equipmentFlashConfigPol"
        )

        # FAST LINK FAILOVER POLICIES
        self.config["fast_link_failover"] = dict_extractor(
            self.raw_configs, "infraInfra", "topoctrlFastLinkFailoverInstPol"
        )

        # FIBRE CHANNEL NODE POLICIES
        self.config["fibre_channel_node"] = dict_extractor(
            self.raw_configs, "infraInfra", "fcInstPol"
        )

        # FIBRE CHANNEL SAN POLICIES
        self.config["fibre_channel_san"] = dict_extractor(
            self.raw_configs, "infraInfra", "fcFabricPol"
        )

        # FORWARDING SCALE PROFILE POLICIES
        self.config["forwarding_scale_profile"] = dict_extractor(
            self.raw_configs, "infraInfra", "topoctrlFwdScaleProfilePol"
        )

        # NETFLOW NODE POLICIES
        self.config["netflow_node"] = dict_extractor(
            self.raw_configs, "infraInfra", "netflowNodePol"
        )

        # POE NODE POLICIES
        self.config["poe_node"] = dict_extractor(
            self.raw_configs, "infraInfra", "poeInstPol"
        )

        # PTP NODE PROFILE POLICIES
        self.config["ptp_node_profile"] = dict_extractor(
            self.raw_configs, "infraInfra", "ptpInstPol"
        )

        # SPANNING TREE POLICIES
        self.config["stp"] = dict_extractor(
            self.raw_configs, "infraInfra", "stpInstPol"
        )

        # SYNCHRONOUS ETHERNET MODE POLICIES
        self.config["sync_eth_node"] = dict_extractor(
            self.raw_configs, "infraInfra", "synceInstPol"
        )

        # USB CONFIGURATION POLICIES
        self.config["usb_config"] = dict_extractor(
            self.raw_configs, "infraInfra", "topoctrlUsbConfigProfilePol"
        )

        # VPC PROTECTION GROUPS
        self.config["vpc_protection_group"] = dict_extractor(
            self.raw_configs, "fabricInst", "fabricProtPol"
        )

        # VPC DOMAIN POLICIES
        self.config["vpc_domain"] = dict_extractor(
            self.raw_configs, "fabricInst", "vpcInstPol"
        )


class AccessPoliciesInterface(ChildExtractorBase):
    def _extract_config_(self) -> None:
        # 802.1X PORT AUTH POLICIES
        self.config["dot1x_auth"] = dict_extractor(
            self.raw_configs, "infraInfra", "l2PortAuthPol"
        )

        # CDP POLICIES
        self.config["cdp"] = dict_extractor(self.raw_configs, "infraInfra", "cdpIfPol")

        # COPP POLICIES
        self.config["copp"] = dict_extractor(
            self.raw_configs, "infraInfra", "coppIfPol"
        )

        # DATA PLANE POLICING POLICIES
        self.config["data_plane_policing"] = dict_extractor(
            self.raw_configs, "infraInfra", "qosDppPol"
        )

        # DWDM POLICIES
        self.config["dwdm"] = dict_extractor(
            self.raw_configs, "infraInfra", "dwdmIfPol"
        )

        # FIBER CHANNEL INTERFACE POLICIES
        self.config["fiberchannel_interface"] = dict_extractor(
            self.raw_configs, "infraInfra", "fcIfPol"
        )

        # FIREWALL POLICIES
        self.config["firewall"] = dict_extractor(
            self.raw_configs, "infraInfra", "nwsFwPol"
        )

        # L2 INTERFACE POLICIES
        self.config["l2_interface"] = dict_extractor(
            self.raw_configs, "infraInfra", "l2IfPol"
        )

        # LINK FLAP POLICIES
        self.config["link_flap"] = dict_extractor(
            self.raw_configs, "infraInfra", "fabricLinkFlapPol"
        )

        # LINK LEVEL POLICIES
        self.config["link_level"] = dict_extractor(
            self.raw_configs, "infraInfra", "fabricHIfPol"
        )

        # LINK LEVEL FLOW CONTROL POLICIES
        self.config["link_level_flow_control"] = dict_extractor(
            self.raw_configs, "infraInfra", "qosLlfcIfPol"
        )

        # LLDP POLICIES
        self.config["lldp"] = dict_extractor(
            self.raw_configs, "infraInfra", "lldpIfPol"
        )

        # MCP POLICIES
        self.config["mcp"] = dict_extractor(self.raw_configs, "infraInfra", "mcpIfPol")

        # POE POLICIES
        self.config["poe"] = dict_extractor(self.raw_configs, "infraInfra", "poeIfPol")

        # PORT CHANNEL POLICIES
        self.config["port_channel"] = dict_extractor(
            self.raw_configs, "infraInfra", "lacpLagPol"
        )

        # PORT CHANNEL MEMBER POLICIES
        self.config["port_channel_member"] = dict_extractor(
            self.raw_configs, "infraInfra", "lacpIfPol"
        )

        # PORT SECURITY POLICIES
        self.config["port_security"] = dict_extractor(
            self.raw_configs, "infraInfra", "l2PortSecurityPol"
        )

        # PRIORITY FLOW CONTROL POLICIES
        self.config["priority_flow_control"] = dict_extractor(
            self.raw_configs, "infraInfra", "qosPfcIfPol"
        )

        # SLOW DRAIN POLICIES
        self.config["slow_drain"] = dict_extractor(
            self.raw_configs, "infraInfra", "qosSdIfPol"
        )

        # SPANNING TREE POLICIES
        self.config["spanning_tree"] = dict_extractor(
            self.raw_configs, "infraInfra", "stpIfPol"
        )

        # STORM CONTROL POLICIES
        self.config["storm_control"] = dict_extractor(
            self.raw_configs, "infraInfra", "stormctrlIfPol"
        )

        # SYNCHRONOUS ETHERNET INTERFACES POLICIES
        self.config["sync_eth_interface"] = dict_extractor(
            self.raw_configs, "infraInfra", "synceEthIfPol"
        )

        # ZR TRANSCEIVER POLICIES
        self.config["zr_transceiver"] = dict_extractor(
            self.raw_configs, "infraInfra", "xcvrZRIfPol"
        )

        # ZRP TRANSCEIVER POLICIES
        self.config["zrp_transceiver"] = dict_extractor(
            self.raw_configs, "infraInfra", "xcvrZRPIfPol"
        )

        # MACSEC POLICIES
        self.config["macsec"] = {}

        # MACSEC PARAMETERS POLICIES
        self.config["macsec"]["parameters"] = dict_extractor(
            self.raw_configs, "infraInfra", "macsecPolCont", "macsecParamPol"
        )

        # MACSEC KEYCHAIN POLICIES
        self.config["macsec"]["keychain"] = dict_extractor(
            self.raw_configs, "infraInfra", "macsecPolCont", "macsecKeyChainPol"
        )

        # MACSEC INTERFACES POLICIES
        self.config["macsec"]["interfaces"] = dict_extractor(
            self.raw_configs, "infraInfra", "macsecIfPol"
        )

        # NETFLOW POLICIES
        self.config["netflow"] = {}

        # NETFLOW RECORDS POLICIES
        self.config["netflow"]["record"] = dict_extractor(
            self.raw_configs, "infraInfra", "netflowRecordPol"
        )

        # NETFLOW EXPORTERS POLICIES
        self.config["netflow"]["exporter"] = dict_extractor(
            self.raw_configs, "infraInfra", "netflowExporterPol"
        )

        # NETFLOW VM EXPORTERS POLICIES
        self.config["netflow"]["vm_exporter"] = dict_extractor(
            self.raw_configs, "infraInfra", "netflowVmmExporterPol"
        )

        # NETFLOW MONITOR POLICIES
        self.config["netflow"]["monitor"] = dict_extractor(
            self.raw_configs, "infraInfra", "netflowMonitorPol"
        )


class AccessPoliciesGlobal(ChildExtractorBase):
    def _extract_config_(self) -> None:
        # DHCP RELAY POLICIES
        self.config["dhcp"] = dict_extractor(
            self.raw_configs, "infraInfra", "dhcpRelayP"
        )

        # MCP INSTANCE POLICY
        self.config["mcp"] = dict_extractor(
            self.raw_configs, "infraInfra", "mcpInstPol"
        )

        # ATTACHABLE ACCESS ENTITY PROFILES
        self.config["aaep"] = dict_extractor(
            self.raw_configs, "infraInfra", "infraAttEntityP"
        )

        # ERROR DISABLE RECOVERY POLICIES
        self.config["err_disable_recovery"] = dict_extractor(
            self.raw_configs, "infraInfra", "edrErrDisRecoverPol"
        )

        # QOS CLASSES
        self.config["qos"] = dict_extractor(
            self.raw_configs, "infraInfra", "qosInstPol", "qosClass"
        )


class AccessInterfaces(ChildExtractorBase):
    def _extract_config_(self) -> None:
        # LEAF ACCESS PORT POLICY GROUPS
        self.config["leaf_access_polgrp"] = dict_extractor(
            self.raw_configs, "infraInfra", "infraFuncP", "infraAccPortGrp"
        )

        # LEAF PC INTERFACE POLICY GROUPS
        lf_pc_polgrp: list = dict_extractor(
            self.raw_configs, "infraInfra", "infraFuncP", "infraAccBndlGrp"
        )
        self.config["leaf_pc_polgrp"] = [
            item for item in lf_pc_polgrp if item["attributes"]["lagT"] == "link"
        ]

        # LEAF VPC INTERFACE POLICY GROUPS
        lf_vpc_polgrp: list = dict_extractor(
            self.raw_configs, "infraInfra", "infraFuncP", "infraAccBndlGrp"
        )
        self.config["leaf_vpc_polgrp"] = [
            item for item in lf_vpc_polgrp if item["attributes"]["lagT"] == "node"
        ]

        # LEAF INTERFCE PROFILES
        self.config["leaf_intpro"] = dict_extractor(
            self.raw_configs, "infraInfra", "infraAccPortP"
        )

        # FEX INTERFACE PROFILES
        self.config["fex_intpro"] = dict_extractor(
            self.raw_configs, "infraInfra", "infraFexP"
        )

        # SPINE ACCESS PORT POLICY GROUPS
        self.config["spine_access_polgrp"] = dict_extractor(
            self.raw_configs, "infraInfra", "infraFuncP", "infraSpAccPortGrp"
        )

        # SPINE INTERFCE PROFILES
        self.config["spine_intpro"] = dict_extractor(
            self.raw_configs, "infraInfra", "infraSpAccPortP"
        )


class AccessSwitches(ChildExtractorBase):
    def _extract_config_(self) -> None:
        # LEAF SWITCH POLICY GROUPS
        self.config["leaf_polgrp"] = dict_extractor(
            self.raw_configs, "infraInfra", "infraFuncP", "infraAccNodePGrp"
        )

        # LEAF SWITCH PROFILES
        self.config["leaf_swpro"] = dict_extractor(
            self.raw_configs, "infraInfra", "infraNodeP"
        )

        # SPINE SWITCH POLICY GROUPS
        self.config["spine_polgrp"] = dict_extractor(
            self.raw_configs, "infraInfra", "infraFuncP", "infraSpineAccNodePGrp"
        )

        # SPINE SWITCH PROFILES
        self.config["spine_swpro"] = dict_extractor(
            self.raw_configs, "infraInfra", "infraSpineP"
        )


class AccessPhyExtDomains(ChildExtractorBase):
    def _extract_config_(self) -> None:
        # EXTERNAL BRIDGED (L2) DOMAINS
        self.config["ext_l2"] = self.raw_configs["l2extDomP"]

        # FIBRE CHANNEL DOMAINS
        self.config["fibre_channel"] = self.raw_configs["fcDomP"]

        # L3 DOMAINS
        self.config["ext_l3"] = self.raw_configs["l3extDomP"]

        # PHYSICAL DOMAINS
        self.config["physical"] = self.raw_configs["physDomP"]


class AccessPools(ChildExtractorBase):
    def _extract_config_(self) -> None:
        # VLAN POOLS
        self.config["vlan"] = dict_extractor(
            self.raw_configs, "infraInfra", "fvnsVlanInstP"
        )

        # VSAN POOLS
        self.config["vsan"] = dict_extractor(
            self.raw_configs, "infraInfra", "fvnsVsanInstP"
        )

        # VSAN ATTRIBUTES
        self.config["vsan_attributes"] = dict_extractor(
            self.raw_configs, "infraInfra", "fcVsanAttrP"
        )

        # VXLAN POOLS
        self.config["vxlan"] = dict_extractor(
            self.raw_configs, "infraInfra", "fvnsVxlanInstP"
        )
