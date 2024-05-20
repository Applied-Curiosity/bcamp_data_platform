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

# The Data Transfer Object (DTO) helps ensure that data passed from the configuration to the Pulumi script is structured and type-safe.

**dto.py:**
pythonCopy code
from dataclasses import dataclass

@dataclass
class PrivateEndpointConfig:
    name: str
    subnet_id: str

@dataclass
class StorageAccountConfig:
    name: str
    resource_group_name: str
    location: str
    account_tier: str
    replication_type: str
    private_endpoint: PrivateEndpointConfig
