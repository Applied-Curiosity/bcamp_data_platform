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
                    id=self.config.public_ip_address_id)

            )]
        )


        pulumi.export('bastion_id', bastion.id)


    def output_dto(self) -> BastionHostConfig:
        return self.config
