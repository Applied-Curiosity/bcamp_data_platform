from dataclasses import dataclass, field
from typing import List, Dict, Optional

# defining storage

@dataclass
class LakehouseConfig:
    account_name: str
    resource_group_name: str
    container_name: str
    blob_name: str
    private_endpoint_name: str
    private_link_name: str
    dfs_private_endpoint_name: str
    dfs_private_link_name: str
    subnet_id: str
    location: str
    account_tier: str
    replication_type: str

@dataclass
class LandingZoneConfig:
    account_name: str
    resource_group_name: str
    location: str
    container_name: str
    blob_name: str
    private_endpoint_name: str
    private_link_name: str
    dfs_private_endpoint_name: str
    dfs_private_link_name: str
    account_tier: str
    replication_type: str

@dataclass
class StorageAccountConfig:
    lakehouse: List[LakehouseConfig]
    landing_zone: List[LandingZoneConfig]

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
    subnet_id: str

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
    address_prefix: str
    subnets: List[SubnetConfig]

@dataclass
class BastionHostConfig:
    resource_group_name: str
    location: str
    name: str
    ip_config_name: str
    subnet_id: str
    public_ip_address_name: str


@dataclass
class VirtualMachineConfig: # might be missing a large amount of compute configurations
    resource_group_name: str
    location: str
    vm_name: str
    user: str
    pw: str
    network_interface_name: str
    subnet_id: str
    os_computer_name: str
    os_disk_name: str

@dataclass
class DatabricksConfig:
    resource_group_name: str
    location: str
    lakehouse_access_connector_name: str
    landing_zone_access_connector_name: str
    workspace_name: str
    private_subnet_name: str
    public_subnet_name: str
    subnet_id: str






@dataclass
class ConfigDTO:
    storage: StorageAccountConfig
    keyvault: KeyvaultConfig
    nsg: SecurityRuleConfig
    vnet: VirtualNetworkConfig
    bastion: BastionHostConfig
    vm: VirtualMachineConfig
    databricks: DatabricksConfig

    @staticmethod
    def from_dict(config: dict) -> 'ConfigDTO':
        return ConfigDTO(
            storage=StorageAccountConfig(**config['storage_account']),
            keyvault=KeyvaultConfig(**config['keyvault']),
            nsg=NSGConfig(**config['nsg_config']),
            vnet=VirtualNetworkConfig(**config['vnet']),
            bastion=BastionHostConfig(**config['bastion_host']),
            vm=VirtualMachineConfig(**config['virtual_machine']),
            databricks=DatabricksConfig(**config['databricks'])
        )
