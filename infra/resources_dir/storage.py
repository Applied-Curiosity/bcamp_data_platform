"""
Deploys necessary storage, specifically the lakehouse and the landing zone.
Lakehouse contains multiple layers (blob, queue, table, fileshare, containers, and private endpoints).
Current objective is to ensure configurations are correct, fill out the layers with the correct coded configurations
and to adjust dev.yml file accordingly
"""

import sys
sys.path.append('/workspaces/bcamp_data_platform_azure/infra')

from dto import LakehouseConfig, LandingZoneConfig, StorageAccountConfig
from pulumi_azure_native import storage, network
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
            account_name=account.name,
            resource_name=self.config.lakehouse['container_name'],
            resource_group_name=self.config.lakehouse['resource_group_name']
        )
        blob = storage.Blob(
            account_name=account.name,
            resource_name=self.config.lakehouse['blob_name'],
            container_name= self.config.lakehouse['container_name'],
            resource_group_name=self.config.lakehouse['resource_group_name']
         )

        pe = network.PrivateEndpoint(self.config.lakehouse['private_endpoint_name'],
                                     resource_group_name=self.config.lakehouse['resource_group_name'],
                                     location=self.config.lakehouse['location'],
                                     subnet=network.SubnetArgs(id=self.config.lakehouse['subnet_id']),
                                    private_link_service_connections=[network.PrivateLinkServiceConnectionArgs(
                                                                    name="connection1",
                                                                    private_link_service_id=account.id,
                                                                    group_ids=["blob"],
                            private_link_service_connection_state=network.PrivateLinkServiceConnectionStateArgs(
                                status="Approved",
                        description="Auto-approved",
            ),
        )]
    )

        dfs_pe = network.PrivateEndpoint('dfs-pe', # fix this and include in the configuration
                                     resource_group_name=self.config.lakehouse['resource_group_name'],
                                     location=self.config.lakehouse['location'],
                                     subnet=network.SubnetArgs(id=self.config.lakehouse['subnet_id']),
                                    private_link_service_connections=[network.PrivateLinkServiceConnectionArgs(
                                                                    name="connection2",
                                                                    private_link_service_id=account.id,
                                                                    group_ids=["dfs"],
                            private_link_service_connection_state=network.PrivateLinkServiceConnectionStateArgs(
                                status="Approved",
                        description="Auto-approved",
            ),
        )]
    )


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
            resource_name=self.config.landing_zone['container_name'],
            account_name=account.name
        )

        blob = storage.Blob(
                            account_name=account.name,
                            resource_name=self.config.landing_zone['blob_name'],
                            container_name=self.config.landing_zone['container_name'],
                            resource_group_name=self.config.landing_zone['resource_group_name']
        )

        local_user = storage.LocalUser(
            resource_group_name=self.config.landing_zone['resource_group_name'],
            resource_name=self.config.landing_zone['local_user_name'],
            account_name=account.name,
            has_shared_key=False,
            has_ssh_key=False,
            has_ssh_password=True,
            permission_scopes=[storage.PermissionScopeArgs(
                permissions='rwlc',
                service="blob",
                resource_name=self.config.landing_zone['container_name'])]
            )

        pe = network.PrivateEndpoint(self.config.landing_zone['private_endpoint_name'],
                                     resource_group_name=self.config.landing_zone['resource_group_name'],
                                     location=self.config.landing_zone['location'],
                                     subnet=network.SubnetArgs(id=self.config.landing_zone['subnet_id']),
                                    private_link_service_connections=[network.PrivateLinkServiceConnectionArgs(
                                                                    name="connection1",
                                                                    private_link_service_id=account.id,
                                                                    group_ids=["blob"],
                            private_link_service_connection_state=network.PrivateLinkServiceConnectionStateArgs(
                                status="Approved",
                        description="Auto-approved",
            ),
        )]
    )

        dfs_pe = network.PrivateEndpoint('dfs-pe-lz', # fix this and include in the configuration
                                     resource_group_name=self.config.landing_zone['resource_group_name'],
                                     location=self.config.landing_zone['location'],
                                     subnet=network.SubnetArgs(id=self.config.landing_zone['subnet_id']),
                                    private_link_service_connections=[network.PrivateLinkServiceConnectionArgs(
                                                                    name="connection2",
                                                                    private_link_service_id=account.id,
                                                                    group_ids=["dfs"],
                            private_link_service_connection_state=network.PrivateLinkServiceConnectionStateArgs(
                                status="Approved",
                        description="Auto-approved",
            ),
        )]
    )



        pulumi.export('account_id', account.id)

    def output_dto(self) -> StorageAccountConfig:
        return self.config
