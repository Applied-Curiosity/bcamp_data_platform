import sys
sys.path.append('/workspaces/bcamp_data_platform_azure/infra')

import pulumi
from pulumi_azure_native import network
from dto import BastionHostConfig

class BastionHostResource:
    def __init__(self, config: BastionHostConfig):
        self.config = config
        self.create_bastion_host()

    def create_bastion_host(self):

        public_ip = network.PublicIPAddress(self.config.public_ip_address_name,
                resource_group_name=self.config.resource_group_name,
                location=self.config.location,
                public_ip_allocation_method="Static",
                sku=network.PublicIPAddressSkuArgs(
                            name="Standard"))

        bastion = network.BastionHost(
            resource_name= self.config.name,
            resource_group_name=self.config.resource_group_name,
            location=self.config.location,
            ip_configurations=[network.BastionHostIPConfigurationArgs(
                name=self.config.ip_config_name,
                subnet=network.SubResourceArgs(
                    id=self.config.subnet_id)
                    ,
                public_ip_address=network.SubResourceArgs(
                    id=public_ip.id)

            )]
        )


        pulumi.export('bastion_id', bastion.id)


    def output_dto(self) -> BastionHostConfig:
        return self.config
