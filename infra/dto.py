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
    def from_dict(config: dict) -> 'StorageConfigDTO':
        keyvault = [KeyvaultConfig(**keyvault) for keyvault in config['keyvault']]
        outputs = config.get('outputs', {})
        return KeyvaultConfigDTO(keyvaults=keyvault)




@dataclass
class ConfigDTO:
    storage: StorageAccountConfig
    keyvault: KeyvaultConfig

    @staticmethod
    def from_dict(config: dict) -> 'ConfigDTO':
        return ConfigDTO(
            storage=StorageAccountConfig(**config['storage_account']),
            keyvault=KeyvaultConfig(**config['keyvault'])
        )
