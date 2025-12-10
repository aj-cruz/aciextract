from .base import ChildExtractorBase, dict_extractor


class FabricInitialization(ChildExtractorBase):
    def _extract_config_(self) -> None:
        # TEP POOL
        self.config["tep_pool"] = [
            tep_pool["attributes"]["tepPool"]
            for tep_pool in self.raw_configs["fabricSetupP"]
            if tep_pool["attributes"]["podId"] == "1"
        ][0]

        # FABRIC ID
        # The only place fabric id is found in the config files is attached to nodes, so we pull from the first node found
        try:
            self.config["fabric_id"] = self.raw_configs["fabricNodeIdentPol"][0][
                "children"
            ][0]["fabricNodeIdentP"]["attributes"]["fabricId"]
        except KeyError:
            # This happens when there are no nodes added to the fabric (brand new or clean cluster)
            self.config["fabric_id"] = "unknown"

        # CONTROLLER QUANTITY
        self.config["ctrl_count"] = dict_extractor(
            self.raw_configs, "ctrlrInst", "infraClusterPol"
        )[0]["attributes"]["size"]


class FabricInventory(ChildExtractorBase):
    def _extract_config_(self) -> None:
        """
        The inventory data is spread across three different json structures (trees):
        fabricNodeIdentPol, dhcpClient, and mgmtMgmtP.
        So we need to extract data from each of those, cross-reference (using hostname
        and node id), and merge them together to build a dict that looks like this:
        {
            "[Hostname]": {
                "id": "[Node ID]",
                "serial": "[Serial #]",
                "role": "[Switch Role (leaf/spine)]",
                "model": "[Switch Model]",
                "version": "[Switch Code Version]",
                "ip": "[Switch OOB Mgmt IP Address]",
                "pod": "[Switch Pod ID"
            }
        }

        """

        # SEARCH THE 1ST TREE (fabricNodeIdentPol) FOR HOSTNAME, NODE ID, & SERIAL NUMBER
        # NOTE: "fabricNOdeIdentP" indicates the node is a switch, not an APIC
        fabric_nodes: list
        try:
            fabric_nodes = sorted(
                [
                    v
                    for each in self.raw_configs["fabricNodeIdentPol"]
                    for node in each["children"]
                    for k, v in node.items()
                    if k == "fabricNodeIdentP"
                ],
                key=lambda d: d["attributes"]["nodeId"],
            )
        except KeyError:
            # No nodes in the fabric
            fabric_nodes = []

        for node in fabric_nodes:
            # Initialize the new record with data from the 1st tree
            self.config.update(
                {
                    node["attributes"]["name"]: {
                        "id": node["attributes"]["nodeId"],
                        "serial": node["attributes"]["serial"],
                        "role": "unknown",
                        "model": "unknown",
                        "version": "unknown",
                        "ip": "NA",
                        "pod": "unknown",
                    }
                }
            )

        # SEARCH THE 2ND TREE (dhcpClient) FOR MODEL NUMBER, VERSION, AND NODE ROLE
        """
        There are several weird roles that don't have data we need, so only
        operate on "leaf" or "spine" roles.
        Also, I have seen cases (from the ACI simulator) where the name is
        empty, but the roles are "leaf" or "spine." Not sure what that is about
        but skip those .
        """
        fabric_nodes = [
            node
            for node in self.raw_configs["dhcpClient"]
            if node["attributes"]["nodeRole"] in ["leaf", "spine"]
            and node["attributes"]["name"]
        ]
        # Update the record with data from the 2nd tree
        for node in fabric_nodes:
            self.config[node["attributes"]["name"]]["model"] = node["attributes"][
                "model"
            ]
            self.config[node["attributes"]["name"]]["version"] = node["attributes"][
                "runningVer"
            ]
            self.config[node["attributes"]["name"]]["role"] = node["attributes"][
                "nodeRole"
            ]

        # SEARCH THE 3RD TREE (mgmtMgmtP) FOR OOB MGMT IP ADDRESS AND POD ID
        fabric_nodes = [
            node["mgmtRsOoBStNode"]["attributes"]
            for each in self.raw_configs["mgmtMgmtP"]
            for child in each["children"]
            for k, v in child.items()
            if k == "mgmtOoB"
            for node in v["children"]
            if "mgmtRsOoBStNode" in node
        ]
        # We don't have the node name in mgmtMgmtP so we need to loop through both records and cross-reference using the node ID.
        for node in self.config:
            for oob_node in fabric_nodes:
                if self.config[node]["id"] == oob_node["tDn"].split("/")[-1].lstrip(
                    "node-"
                ):
                    self.config[node]["ip"] = oob_node["addr"]
                    self.config[node]["pod"] = (
                        oob_node["tDn"].split("/")[1].lstrip("pod-")
                    )


class FabricTEPPools(ChildExtractorBase):
    def _extract_config_(self) -> None:
        # PHYSICAL TEP POOLS
        try:
            self.config["phys_tep_pools"] = [
                pool
                for pool in self.raw_configs["fabricSetupP"]
                if pool["attributes"]["podType"] == "physical"
            ]
        except KeyError:
            # This is an older version of ACI that doesn't use the "podType" key in the TEP config
            self.config["phys_tep_pools"] = [
                pool for pool in self.raw_configs["fabricSetupP"]
            ]
