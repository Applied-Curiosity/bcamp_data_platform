pythonCopy code
import pulumi
from pulumi_azure_native import network
from dto import NSGConfig, SecurityRuleConfig

def create_nsg(config: NSGConfig):
    nsg = network.NetworkSecurityGroup(
        config.name,
        resource_group_name=config.resource_group_name,
        location=config.location,
        security_rules=[network.SecurityRuleArgs(
            name=rule.name,
            priority=rule.priority,
            direction=rule.direction,
            access=rule.access,
            protocol=rule.protocol,
            source_port_range=rule.source_port_range,
            destination_port_range=rule.destination_port_range,
            source_address_prefix=rule.source_address_prefix,
            destination_address_prefix=rule.destination_address_prefix,
        ) for rule in config.security_rules]
    )
    pulumi.export('nsg_id', nsg.id)

# Example usage
nsg_config = NSGConfig(
    name="main-nsg",
    location="eastus",
    resource_group_name="pulumi-resources",
    security_rules=[
        SecurityRuleConfig(
            name="allow-http",
            priority=100,
            direction="Inbound",
            access="Allow",
            protocol="Tcp",
            source_port_range="*",
            destination_port_range="80",
            source_address_prefix="*",
            destination_address_prefix="*"
        ),
        SecurityRuleConfig(
            name="allow-https",
            priority=110,
            direction="Inbound",
            access="Allow",
            protocol="Tcp",
            source_port_range="*",
            destination_port_range="443",
            source_address_prefix="*",
            destination_address_prefix="*"
        )
    ]
)
create_nsg(nsg_config)
