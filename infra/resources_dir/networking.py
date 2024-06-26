import sys
sys.path.append('/workspaces/bcamp_data_platform_azure/infra')

import pulumi
from pulumi_azure_native import network
from dto import VirtualNetworkConfig, NSGConfig, SubnetConfig


class VirtualNetworkResource:
    def __init__(self, config: VirtualNetworkConfig):
        self.config = config
        self.create_virtual_network()

    def create_virtual_network(self):
        vnet = network.VirtualNetwork(self.config.name,
            resource_group_name=self.config.resource_group_name,
            location=self.config.location,
            address_space=network.AddressSpaceArgs(
                address_prefixes=[self.config.address_prefix]))

        subnets = []
        for self.config.subnet in self.config.subnets:
            subnet = network.Subnet(self.config.subnet['name'],
                                    resource_group_name=self.config.resource_group_name,
                                    virtual_network_name=vnet.name,
                                    address_prefix=self.config.subnet['address_prefix'])
            subnets.append(subnet)




        pulumi.export('vnet_id', vnet.id)

    def output_dto(self) -> VirtualNetworkConfig:
        return self.config
