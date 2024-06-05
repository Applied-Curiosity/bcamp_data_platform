
import sys
sys.path.append('/workspaces/bcamp_data_platform_azure/infra')

from dto import StorageAccountConfig
from pulumi_azure_native import storage, resources
import pulumi



class StorageResource:
    def __init__(self, config: StorageAccountConfig):
        self.config = config
        self.create_storage()

    def create_storage(self):
        account = storage.StorageAccount(
            resource_name="sa", # change this so its not hard coded
            resource_group_name=self.config.resource_group_name,
            sku=storage.SkuArgs(
                name=storage.SkuName.STANDARD_LRS,
            ),
            kind=storage.Kind.STORAGE_V2,
        )

       # primary_key = (
        #    pulumi.Output.all(resource_group.name, account.name)
         #   .apply(lambda args: storage.list_storage_account_keys(
          #      resource_group_name=args[0], account_name=args[1]
         #   ))
         #   .apply(lambda account_keys: account_keys.keys[0].value)
        #)

        # Necessary pulumi exports
        pulumi.export("account_id", account.id)

    def output_dto(self) -> StorageAccountConfig:
        return self.config
