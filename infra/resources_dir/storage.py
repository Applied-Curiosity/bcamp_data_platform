"""
Deploys necessary storage, specifically the lakehouse and the landing zone.
Lakehouse contains multiple layers (blob, queue, table, fileshare, containers, and private endpoints).
Current objective is to ensure configurations are correct, fill out the layers with the correct coded configurations
and to adjust dev.yml file accordingly
"""

import sys
sys.path.append('/workspaces/bcamp_data_platform_azure/infra') # need to see if this is a fixable issue

from dto import StorageAccountConfig
from pulumi_azure_native import storage, resources
import pulumi

class StorageResource:
    def __init__(self, config: StorageAccountConfig):
        self.config = config
        self.create_lakehouse()
        self.create_landing_zone()

    def create_lakehouse(self):
        account = storage.StorageAccount(
            resource_name=self.config.lakehouse.account_name,
            resource_group_name=self.config.resource_group_name,
            access_tier=storage.AccessTier.HOT,
            sku=storage.SkuArgs(
                name=storage.SkuName.STANDARD_LRS,
            ),
            kind=storage.Kind.STORAGE_V2
        )

        blob = storage.Blob('blobResource',
            storage_account_name=self.config.lakehouse.account_name,
            # more configurations
        )

        file_service = storage.FileShare(
            storage_account_name=self.config.lakehouse.account_name
            # more configurations
        )

        pe = storage.PrivateEndpointConnection(
            # code here, also going to require a loop as there is multiple private endpoints
        )

        queue = storage.Queue(
            # code here
        )

        table = storage.Table(
            # code here
        )

        blob_container = storage.BlobContainer(
            # code here, and make loop as there is multiple blob containers in the lakehouse
        )

        pulumi.export(account.id, "account_id")

    def create_landing_zone(self):
        account = storage.StorageAccount(
            resource_name=self.config.name,
            resource_group_name=self.config.resource_group_name,
            access_tier=storage.AccessTier.HOT,
            sku=storage.SkuArgs(
                name=storage.SkuName.STANDARD_LRS,
            ),
            kind=storage.Kind.STORAGE_V2
        )

        blob = storage.Blob(
            # code here
        )

        file_service = storage.FileShare(
            # code here
        )

        queue = storage.Queue(
            # code here
        )

        table = storage.Table(
            # code here
        )

        blob_container = storage.BlobContainer(
            # code here, and make loop as there is multiple blob containers in the lakehouse
        )

        local_user = storage.LocalUser(
            # code here
        )

    def output_dto(self) -> StorageAccountConfig:
        return self.config
