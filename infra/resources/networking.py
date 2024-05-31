
import pulumi
from pulumi_azure_native import network

import sys
sys.path.append("/workspaces/bcamp_data_platform_azure/infra")

from dto import NetworkConfig, SubnetConfig, NSGRuleConfig


def create_network(config: NetworkConfig):
    # Create the Virtual Network
    vnet = network.VirtualNetwork(
        config.vnet_name,
        address_space=network.AddressSpaceArgs(
            address_prefixes=[config.address_space]
        ),
        subnets=[network.SubnetArgs(
            name=sub.name,
            address_prefix=sub.address_prefix
        ) for sub in config.subnets],
        resource_group_name=pulumi.Config().require("resource_group_name")
    )

    # Create Network Security Group with rules
    nsg = network.NetworkSecurityGroup(
        config.nsg[0].name,
        security_rules=[network.SecurityRuleArgs(
            name=rule.name,
            priority=rule.priority,
            direction=rule.direction,
            access=rule.access,
            protocol=rule.protocol,
            source_port_range=rule.source_port_range,
            destination_port_range=rule.destination_port_range,
            source_address_prefix=rule.source_address_prefix,
            destination_address_prefix=rule.destination_address_prefix
        ) for rule in config.nsg],
        resource_group_name=pulumi.Config().require("resource_group_name")
    )

    pulumi.export('vnet_id', vnet.id)
    pulumi.export('nsg_id', nsg.id)

# Assuming config is loaded from the YAML
config_data = NetworkConfig(
    vnet_name="example-vnet",
    address_space="10.0.0.0/16",
    subnets=[
        SubnetConfig(name="subnet1", address_prefix="10.0.1.0/24")
    ],
    nsg=[
        NSGRuleConfig(
            name="allow-ssh",
            priority=100,
            direction="Inbound",
            access="Allow",
            protocol="Tcp",
            source_port_range="*",
            destination_port_range="22",
            source_address_prefix="*",
            destination_address_prefix="*"
        )
    ]
)
create_network(config_data)
