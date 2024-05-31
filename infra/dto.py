from dataclasses import dataclass, field
from typing import List, Dict, Optional

# defining storage
@dataclass
class StorageAccountConfig: # echoes the yaml file, but not sure this is correct
    name: str
    type: str
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


@dataclass
class ConfigDTO:
    storage: StorageAccountConfig

    @staticmethod
    def from_dict(config: dict) -> 'ConfigDTO':
        return ConfigDTO(
            storage=StorageAccountConfig(**config['storage'])
        )
