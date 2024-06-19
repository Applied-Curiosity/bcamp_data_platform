import sys
sys.path.append('/workspaces/bcamp_data_platform_azure/infra')

import pulumi
from pulumi_azure_native import network
from dto import VirtualNetworkConfig, NSGConfig, SubnetConfig


class VirtualNetworkResource:
    def __init__(self, config: VirtualNetworkConfig):
        self.config = config
        self.create_virtual_network()

    def create_virtual_network(self): # currently working on this
        vnet = network.VirtualNetwork(
            resource_group_name=self.config.resource_group_name,
            name=self.config.name,
            location=self.config.location,
            address_space=self.config.address_prefix,
            subnets=[network.VirtualNetworkSubnetArgs( # error right here
                    name=self.config.sn['name'],
                    address_prefix=self.config.sn['address_prefix']
                ) for self.config.sn in self.config.subnets]
        )

        pulumi.export('vnet_id', vnet.id)

    def output_dto(self) -> VirtualNetworkConfig:
        return self.config
