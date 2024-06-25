"""
Deploys necessary storage, specifically the lakehouse and the landing zone.
Lakehouse contains multiple layers (blob, queue, table, fileshare, containers, and private endpoints).
Current objective is to ensure configurations are correct, fill out the layers with the correct coded configurations
and to adjust dev.yml file accordingly
"""

import sys
sys.path.append('/workspaces/bcamp_data_platform_azure/infra')

from dto import LakehouseConfig, LandingZoneConfig, StorageAccountConfig
from pulumi_azure_native import storage, resources
import pulumi

class StorageResource:
    def __init__(self, config: StorageAccountConfig):
        self.config = config
        self.create_lakehouse()
        self.create_landing_zone()

    def create_lakehouse(self):
        account = storage.StorageAccount(
            resource_name=self.config.lakehouse['account_name'],
            resource_group_name=self.config.lakehouse['resource_group_name'],
            access_tier=storage.AccessTier.HOT,
            sku=storage.SkuArgs(
                name=storage.SkuName.STANDARD_LRS,
            ),
            kind=storage.Kind.STORAGE_V2
        )

        blob_container = storage.BlobContainer(
            account_name=self.config.lakehouse['account_name'],
            resource_name=self.config.lakehouse['container_name'],
            resource_group_name=self.config.lakehouse['resource_group_name']
        )
        blob = storage.Blob(
            account_name=self.config.lakehouse['account_name'],
            resource_name=self.config.lakehouse['blob_name'],
            container_name= self.config.lakehouse['container_name'],
            resource_group_name=self.config.lakehouse['resource_group_name']
        )

        pe = storage.PrivateEndpointConnection('privateEndpointConnection',
                   account_name=self.config.lakehouse['account_name'],
                   private_endpoint_connection_name=self.config.lakehouse['private_endpoint_name'],
                   private_link_service_connection_state=storage.PrivateLinkServiceConnectionStateArgs(
                   description="Auto-Approved",
                   status=storage.PrivateEndpointServiceConnectionStatus.APPROVED,
    ),
    resource_group_name=self.config.lakehouse['resource_group_name'])


        pulumi.export("account_id", account.id)

    def create_landing_zone(self):
        account = storage.StorageAccount(
            resource_name=self.config.landing_zone['account_name'],
            resource_group_name=self.config.landing_zone['resource_group_name'],
            access_tier=storage.AccessTier.HOT,
            sku=storage.SkuArgs(
                name=storage.SkuName.STANDARD_LRS,
            ),
            kind=storage.Kind.STORAGE_V2
        )
        blob_container = storage.BlobContainer(
            resource_group_name=self.config.landing_zone['resource_group_name'],
            resource_name='lz-cont',
            account_name=self.config.landing_zone['account_name']
        )

        blob = storage.Blob(
                            account_name=self.config.landing_zone['account_name'],
                            resource_name='blob-lz',
                            container_name='lz-cont',
                            resource_group_name=self.config.landing_zone['resource_group_name']
        )

        local_user = storage.LocalUser(
            storage.LocalUser("localUserResource",
    storage_account_id=account.id,
    home_directory="string",
    name="string", # change
    permission_scopes=[storage.LocalUserPermissionScopeArgs(
        permissions=storage.LocalUserPermissionScopePermissionsArgs( # fix this because doesnt exist
            create=False,
            delete=False,
            list=False,
            read=False,
            write=False,
        ),
        resource_name="string", # change
        service="string",
    )],
    ssh_authorized_keys=[storage.LocalUserSshAuthorizedKeyArgs(
        key="string",
        description="string",
    )],
    ssh_key_enabled=False,
    ssh_password_enabled=False)

        )

        pulumi.export('account_id', account.id)

    def output_dto(self) -> StorageAccountConfig:
        return self.config
