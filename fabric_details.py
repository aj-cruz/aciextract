# Built-In Imports
import json

# Custom Imports
from .base import ChildExtractorBase, dict_extractor


def safe_json_load(s: str) -> dict:
    """
    A wrapper for json.loads() to return an empty dictionary if json.loads()
    raises an exception (invalid input)
    
    :param s: Input string to attempt the conversion to json
    :type s: str
    :return: Returns the string converted to a dictionary, or an empty dictionary ({})
    :rtype: dict
    """
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        return {}


class FabricInitialization(ChildExtractorBase):
    def _extract_config_(self) -> None:
        if len(self.raw_configs["ctrlrInst"]) > 1:
            print(
                "\nWARNING: ctrlrInst has more than one entry for APIC controllers. This is unexpected and should be investigated!!!!!"
            )

        # Extract cluster information from the raw configs
        cluster_data: list = [
            each["tagAnnotation"]["attributes"]["value"]
            for each in self.raw_configs["ctrlrInst"][0]["children"]
            if "tagAnnotation" in each
            and each["tagAnnotation"]["attributes"]["key"] == "bootx.cluster"
        ]
        if len(cluster_data) > 1:
            print(
                "\nWARNING: cluster data has more than one entry for APIC clusters (bootx.cluster). This is unexpected and should be investigated!!!!!"
            )
        cluster_data = json.loads(cluster_data[0])

        # Populate the model with extracted data        
        self.config["fabric_name"] = cluster_data["cluster"]["fabricName"]
        self.config["fabric_id"] = cluster_data["cluster"]["fabricId"]
        self.config["cluster_size"] = cluster_data["cluster"]["clusterSize"]
        self.config["pod_id"] = cluster_data["pods"][0]["podId"]
        self.config["tep_pool"] = cluster_data["pods"][0]["tepPool"]
        self.config["infra_vlan"] = cluster_data["cluster"]["infraVlan"]
        self.config["gipo_pool"] = cluster_data["cluster"]["gipoPool"]


class APICCluster(ChildExtractorBase):
    def _extract_config_(self) -> None:
        # Extract APIC serial numbers from the raw configs (ctrlrInst > fabricNodeIdentPol > children > fabricCtrlrIdentP)
        controller_serials: list = [
            another["fabricCtrlrIdentP"]["attributes"]["serial"]
            for each in self.raw_configs["ctrlrInst"][0]["children"]
            if "fabricNodeIdentPol" in each
            for another in each["fabricNodeIdentPol"]["children"]
            if "fabricCtrlrIdentP" in another
        ]

        # Get the APIC data for those serial numbers (ctrlInst > children > tagAnnotation)
        controller_data: list = sorted([
                item["tagAnnotation"]["attributes"]
                for item in self.raw_configs["ctrlrInst"][0]["children"]
                if safe_json_load(item.get("tagAnnotation", {}).get("attributes", {}).get("value", "")).get("serialNumber", "") in controller_serials
            ],
            key=lambda d: safe_json_load(d["value"])["nodeId"]
        )
        
        # Updated config model with APIC data
        for controller in controller_data:
            attributes = safe_json_load(controller["value"])
            cimc_ip: str = safe_json_load([
                item["tagAnnotation"]["attributes"]
                for item in self.raw_configs["ctrlrInst"][0]["children"]
                if item.get("tagAnnotation", {}).get("attributes", {}).get("key", "") == f"{controller['key']}.cimc"
            ][0]["value"])["address4"]

            self.config[attributes["nodeName"]] = {
                "id": attributes["nodeId"],
                "serial": attributes["serialNumber"],
                "oob_ip": attributes["activeNodeAddr"],
                "cimc_ip": cimc_ip,
                "pod": attributes["podId"],
            }


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
        # NOTE: "fabricNodeIdentP" indicates the node is a switch, not an APIC
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
