pythonCopy code
from dataclasses import dataclass, field
from typing import List

@dataclass
class SubnetConfig:
    name: str
    address_prefix: str

@dataclass
class NSGRuleConfig:
    name: str
    priority: int
    direction: str
    access: str
    protocol: str
    source_port_range: str
    destination_port_range: str
    source_address_prefix: str
    destination_address_prefix: str

@dataclass
class NetworkConfig:
    vnet_name: str
    address_space: str
    subnets: List[SubnetConfig]
    nsg: List[NSGRuleConfig]

pythonCopy code
from dataclasses import dataclass, field
from typing import List

@dataclass
class SecurityRuleConfig:
    name: str
    priority: int
    direction: str
    access: str
    protocol: str
    source_port_range: str
    destination_port_range: str
    source_address_prefix: str
    destination_address_prefix: str

@dataclass
class NSGConfig:
    name: str
    location: str
    resource_group_name: str
    security_rules: List[SecurityRuleConfig]
