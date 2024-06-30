import sys
sys.path.append('/workspaces/bcamp_data_platform_azure/infra')

import pulumi
from pulumi_azure_native import keyvault, network, resources
from dto import KeyvaultConfig, AccessPolicyEntry




class KeyvaultResource:
    def __init__(self, config: KeyvaultConfig):
        self.config = config # not sure why this isnt working, explains all self.config.____ in create_keyvault()
        self.create_keyvault()

    def create_keyvault(self): # see if importing self.config cleans up code
        kv = keyvault.Vault(
            resource_name=self.config.resource_name,
            resource_group_name=self.config.resource_group_name,
            location=self.config.location,
            properties=keyvault.VaultPropertiesArgs(
                tenant_id=self.config.tenant_id,
                sku=keyvault.SkuArgs(name=self.config.sku_name, family=keyvault.SkuFamily.A), # add this to yml?
                access_policies=[keyvault.AccessPolicyEntryArgs(
                    tenant_id=self.config.ap['tenant_id'],
                    object_id=self.config.ap['object_id'],
                    permissions=keyvault.PermissionsArgs(
                        keys=self.config.ap['permissions'].get('keys', []),
                        secrets=self.config.ap['permissions'].get('secrets', [])
                    )
                ) for self.config.ap in self.config.access_policies]
            )
        )


        pe = network.PrivateEndpoint('pe-kv',
                                     resource_group_name=self.config.resource_group_name,
                                     location=self.config.location,
                                     subnet=network.SubnetArgs(id=self.config.subnet_id),
                                    private_link_service_connections=[network.PrivateLinkServiceConnectionArgs(
                                                                    name="kvlink",
                                                                    private_link_service_id=kv.id,
                                                                    group_ids=["vault"],
                            private_link_service_connection_state=network.PrivateLinkServiceConnectionStateArgs(
                                status="Approved",
                        description="Auto-approved",
            ),
        )]
    )

        pulumi.export('keyvault_id', kv.id)

    def output_dto(self) -> KeyvaultConfig:
        return self.config
