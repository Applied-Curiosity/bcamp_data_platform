import sys
sys.path.append('/workspaces/bcamp_data_platform_azure/infra')

import pulumi
from pulumi_azure_native import compute
from dto import BastionHostConfig, BastionIpConfig

class BastionHostResource:
    def __init__(self, config, BastionHostConfig):
        config = self.config
        self.create_bastion_host()

    def create_bastion_host(self):
        bastion = compute.BastionHost(
            name= self.config.name,
            resource_group_name=self.config.resource_group_name,
            location=self.config.location,
            ip_configuration=compute.BastionHostIpConfiguration(
                name=self.config.ip_configuration.name,
                subnet_id=self.config.ip_configuration.subnet_id,
                public_ip_address_id=self.config.ip_configuration.public_ip_address_id,
            )
        )

        pulumi.export('bastion_id', bastion.id)


    def output_dto(self) -> BastionHostConfig:
        return self.config
