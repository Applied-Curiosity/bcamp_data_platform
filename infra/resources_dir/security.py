"""
Multiple NSGs, look at Azure Portal
"""

import sys
sys.path.append('/workspaces/bcamp_data_platform_azure/infra') # see how I can avoid this

import pulumi
from pulumi_azure_native import network
from dto import NSGConfig, SecurityRuleConfig

class SecurityResource:
    def __init__(self, config: NSGConfig):
        self.config = config
        self.create_nsg()


    def create_nsg(self):
        nsg = network.NetworkSecurityGroup(
            self.config.name,
            resource_group_name=self.config.resource_group_name,
            location=self.config.location,
            security_rules=[network.SecurityRuleArgs(
                name=self.config.rule['name'],
                priority=self.config.rule['priority'],
                direction=self.config.rule['direction'],
                access=self.config.rule['access'],
                protocol=self.config.rule['protocol'],
                source_port_range=self.config.rule['source_port_range'],
                destination_port_range=self.config.rule['destination_port_range'],
                source_address_prefix=self.config.rule['source_address_prefix'],
                destination_address_prefix=self.config.rule['destination_address_prefix'],
            ) for self.config.rule in self.config.security_rules]
        )
        pulumi.export('nsg_id', nsg.id)
