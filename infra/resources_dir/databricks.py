import sys
sys.path.append('/workspaces/bcamp_data_platform_azure/infra')

import pulumi
from pulumi_azure_native import databricks, network
from dto import DatabricksConfig


class DatabricksResource:

    def __init__(self, config: DatabricksConfig):
        self.config = config
        self.create_workspace()

    def create_workspace(self):
        lakehouse_access_connector = databricks.AccessConnector(
            resource_name=self.config.access_connector_name,
            resource_group_name=self.config.resource_group_name,
            location=self.config.location,
            identity=databricks.ManagedServiceIdentityArgs(
                type='UserAssigned',
                user_assigned_identities=[]
            )
        )

        landing_zone_access_connector = databricks.AccessConnector(
            resource_name=self.config.landing_zone_access_connector_name,
            resource_group_name=self.config.resource_group_name,
            location=self.config.location,
            identity=databricks.ManagedServiceIdentityArgs(
                type='UserAssigned',
                user_assigned_identities=[]
            )
        )

        workspace = databricks.Workspace(
            resource_name=self.config.workspace_name,
            location=self.config.location,
            resource_group_name=self.config.resource_group_name,
            sku=databricks.SkuArgs(name='premium'),
            parameters=databricks.WorkspaceCustomParametersArgs(
                custom_private_subnet_name=self.config.private_subnet_name,
                custom_public_subnet_name=self.config.public_subnet_name,
                prepare_encryption=False,
                enable_no_public_ip=True,
                require_infrastructure_encryption=False,
                storage_account_sku_name='Standard_GRS',
                vnet_address_prefix='10.139'
            )

        )

        private_endpoint = network.PrivateEndpoint(
            resource_name=self.config.private_endpoint_name,
            resource_group_name=self.config.resource_group_name,
            location=self.config.location,
            subnet=network.SubnetArgs(id=self.config.subnet_id),
            private_link_service_connections=[network.PrivateLinkServiceConnectionArgs(
            name="databricks-pe-connection",
            private_link_service_id=workspace.id,
            group_ids=["databricks_workspace"])])





        oid_private_endpoint = network.PrivateEndpoint(
            # args here
        )



        pulumi.export(workspace.id)

    def output_dto(self) -> DatabricksConfig:
        return self.config
