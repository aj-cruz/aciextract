# aciextract
Extract and parse a Cisco ACI backup archive file, create an object with the extracted configurations.  
Useful for projects where offline (from backup file) review of an ACI configuration is required, such as:
- Generating As-Built documentation
- Generating Best-Practice Assessment documentation

# REQUIREMENTS
- Python >= 3.11 (Tested on 3.11.4, may work on other 3.x versions)
- ACI Configuration Backup (JSON): XML currently not supported
    - Tested on backups from following versions of ACI
        - 3.0(1k)
        - 5.2(7f)

# USAGE
Clone aciextract into your project folder.  
From your project do:
```python
from aciextract import ACIConfig

config = ACIConfig("path_to_backup_file")
```

The resulting object closely follows the APIC GUI.  
The root object attributes that hold configuration are:
- fabric_details
- system_settings
- fabric_policies
- access_policies
- tenants

The root attributes are dictionaries (except tenants, which is a list of dictionaries) that have the following structures:  


**fabric_details**  
```python
{
    "fabric_initialization": {
        "tep_pool": "",
        "fabridc_id": "",
        "ctrl_count": ""
    },
    "fabric_inventory": {},
    "tep_pools": {
        "phys_tep_pools": []
    }
}
```

**system_settings**  
```python
{
    "bgp": {
        "bgp_policy_name": "",
        "bgp_asn": "",
        "bgp_route_reflectors": []
    },
    "endpoint_controls": {
        "ep_loop_protection": {},
        "rogue_ep_control": {},
        "ip_aging": {},
    },
    "fabric_wide_settings": {},
    "isis_policy": {},
    "port_tracking": {},
    "misc": {}
}
```

**fabric_policies**  
```python
{
    "policies_pod": {
        "date_time": [],
        "snmp": [],
    },
    "policies_interface": {
        "l3_interface": [],
        "link_level": [],
        "dwdm": [],
        "link_flap": [],
        "zr_transceiver": [],
        "zrp_transceiver": [],
    },
    "policies_global": {
        "dns_profile": [],
        "fabric_l2_mtu": [],
    },
    "policies_monitoring": {
        "fabric_node_control": [],
    },
    "policies_macsec": {
        "interface": [],
        "parameter": [],
        "keychain": [],
    },
    "pods_policy_groups": {
        "groups": [],
    },
    "pods_profiles": {
        "profile": [],
    },
    "interfaces": {
        "spine_policy_group": [],
        "spine_profile": [],
        "leaf_policy_group": [],
        "leaf_profile": [],
    }
}
```

**access_policies**  
```python
{
    "policies_interface": {
        "dot1x_auth": [],
        "cdp": [],
        "copp": [],
        "data_plane_policing": [],
        "dwdm": [],
        "fiberchannel_interface": [],
        "firewall": [],
        "l2_interface": [],
        "link_flap": [],
        "link_level": [],
        "link_level_flow_control": [],
        "lldp": [],
        "mcp": [],
        "poe": [],
        "port_channel": [],
        "port_channel_member": [],
        "port_security": [],
        "priority_flow_control": [],
        "slow_drain": [],
        "spanning_tree": [],
        "storm_control": [],
        "sync_eth_interface": [],
        "zr_transceiver": [],
        "zrp_transceiver": [],
        "macsec": {
            "parameters": [],
            "keychain": [],
            "interfaces": [],
        },
        "netflow": {
            "record": [],
            "exporter": [],
            "vm_exporter": [],
            "monitor": [],
        },
    },
    "policies_global": {
        "dhcp": [],
        "mcp": [],
        "aaep": [],
        "err_disable_recovery": [],
        "qos": [],
    },
    "policies_switch": {
        "dot1x_node_auth": [],
        "bfd_ipv4": [],
        "bfd_ipv6": [],
        "bfd_multihop_ipv4": [],
        "bfd_multihop_ipv6": [],
        "leaf_copp": [],
        "leaf_copp_prefilter": [],
        "spine_copp": [],
        "spine_copp_prefilter": [],
        "equipment_flash_conf": [],
        "fast_link_failover": [],
        "fibre_channel_node": [],
        "fibre_channel_san": [],
        "forwarding_scale_profile": [],
        "netflow_node": [],
        "poe_node": [],
        "ptp_node_profile": [],
        "stp": [],
        "sync_eth_node": [],
        "usb_config": [],
        "vpc_protection_group": [],
        "vpc_domain": [],
    },
    "interfaces": {
        "leaf_access_polgrp": [],
        "leaf_pc_polgrp": [],
        "leaf_vpc_polgrp": [],
        "leaf_intpro": [],
        "fex_intpro": [],
        "spine_access_polgrp": [],
        "spine_intpro": [],
    },
    "switches": {
        "leaf_polgrp": [],
        "leaf_swpro": [],
        "spine_polgrp": [],
        "spine_swpro": [],
    },
    "phys_ext_domains": {
        "ext_l2": [],
        "fibre_channel": [],
        "ext_l3": [],
        "physical": [],
    },
    "pools": {
        "vlan": [],
        "vsan": [],
        "vsan_attributes": [],
        "vxlan": [],
    }
}
```

**tenants**  
This is just a list of all the tenants (complete tenant config).


If you want to see the contents of a specific configuration item for debugging you have a couple options:  
1. ```config.pretty_print(optional_object)```

Without the optional object it will pretty print the entire config structure.  
So to print the access policy pools you would do: ```config.pretty_print(config.access_policies['pools'])```

2. ```config.write(optional_object)```

Same as pretty_print except it writes the output to a file: ```config.json```