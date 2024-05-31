
import sys
sys.path.append('/workspaces/bcamp_data_platform_azure/infra')

from dto import StorageAccountConfig
from pulumi_azure_native import storage, resources
import pulumi

resource_group = resources.ResourceGroup('rg-ac-cus-adb-acclrtor') # I reckon I need to put this in its own python file


class StorageResource:
    def __init__(self, config: StorageAccountConfig):
        self.config = config
        self.create_storage()

    def create_storage(self):
        for storage_config in self.config.type:
            account = storage.StorageAccount(
                f"sa-{storage_config}",  # this line giving me some trouble I think, giving the error while deploying
                resource_group_name=resource_group.name,
                sku=storage.SkuArgs(
                    name=storage.SkuName.STANDARD_LRS,
                ),
                kind=storage.Kind.STORAGE_V2,
            )

            primary_key = (
                pulumi.Output.all(resource_group.name, account.name)
                .apply(
                    lambda args: storage.list_storage_account_keys(
                        resource_group_name=args[0], account_name=args[1]
                    )
                )
                .apply(lambda account_keys: account_keys.keys[0].value)
            )

        # storing the outputs
        self.config.outputs['storage_primary_key'] = primary_key

        # necessary pulumi exports
        pulumi.export(primary_key, 'storage_primary_key')


    def output_dto(self) -> StorageAccountConfig:
        return self.config
