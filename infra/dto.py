from dataclasses import dataclass, field
from typing import List, Dict, Optional

# defining storage
@dataclass
class StorageAccountConfig: # echoes the yaml file, but not sure this is correct
    name: str
    resource_group_name: str
    location: str
    account_tier: str
    replication_type: str
    outputs: str

@dataclass
class StorageConfigDTO:
    storage_accounts: List[StorageAccountConfig]
    outputs: Dict[str, List[str]] = field(default_factory=dict)

    @staticmethod
    def from_dict(config: dict) -> 'StorageConfigDTO':
        accounts = [StorageAccountConfig(**storage) for storage in config['storage']]
        outputs = config.get('outputs', {})
        return StorageConfigDTO(storage_accounts=accounts, outputs=outputs)

# defining key vault

@dataclass
class AccessPolicyEntry:
    tenant_id: str
    object_id: str
    permissions: Dict[str, List[str]]


@dataclass
class KeyvaultConfig:
    resource_name: str
    resource_group_name: str
    location: str
    sku_name: str
    tenant_id: str
    access_policies: List[AccessPolicyEntry]
    outputs: str

@dataclass
class KeyvaultConfigDTO:
    keyvaults: List[KeyvaultConfig]
    outputs: Dict[str, List[str]] = field(default_factory=dict)

    @staticmethod
    def from_dict(config: dict) -> 'KeyvaultConfigDTO':
        keyvault = [KeyvaultConfig(**keyvault) for keyvault in config['keyvault']]
        outputs = config.get('outputs', {})
        return KeyvaultConfigDTO(keyvaults=keyvault, outputs=outputs)

# defining security
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

@dataclass
class SubnetConfig:
    name: str
    address_prefix: str

@dataclass
class VirtualNetworkConfig:
    name: str
    location: str
    resource_group_name: str
    address_space: str
    subnets: List[SubnetConfig]

@dataclass
class BastionIpConfig:
    name: str
    subnet_id: str
    public_ip_address_id: str

@dataclass
class BastionHostConfig:
    resource_group_name: str
    location: str
    name: str
    ip_configuration: List[BastionIpConfig]

@dataclass
class ConfigDTO:
    storage: StorageAccountConfig
    keyvault: KeyvaultConfig
    nsg: SecurityRuleConfig
    vnet: VirtualNetworkConfig
    bastion: BastionHostConfig

    @staticmethod
    def from_dict(config: dict) -> 'ConfigDTO':
        return ConfigDTO(
            storage=StorageAccountConfig(**config['storage_account']),
            keyvault=KeyvaultConfig(**config['keyvault']),
            nsg=NSGConfig(**config['nsg_config']),
            vnet=VirtualNetworkConfig(**config['vnet']),
            bastion=BastionHostConfig(**config['bastion_host'])
        )
