"""An Azure RM Python Pulumi program"""

import pulumi
import yaml
import json
from pulumi_azure_native import resources
from resources_dir.storage import StorageResource
from resources_dir.keyvault import KeyvaultResource
from resources_dir.security import SecurityResource
from resources_dir.networking import VirtualNetworkResource
from resources_dir.bastion import BastionHostResource
from resources_dir.compute import VirtualMachineResource
from dto import ConfigDTO



# Create an Azure Resource Group
# Naming convention is
# rg = resource group
# ac = Applied Curiosity
# cus = Central US
# adb = Azure Databricks
# acclrtor = Accelerator


resource_group = resources.ResourceGroup(resource_name='rg-ac-cus-adb-acclrtor',
                                         resource_group_name='rg-ac-cus-adb-acclrtor')
config_path = 'config/dev.yml'

with open(config_path, 'r') as file:
     config_data = yaml.safe_load(file)

config_dto = ConfigDTO.from_dict(config_data)

storage_resource = StorageResource(config_dto.storage)
# keyvault_resource = KeyvaultResource(config_dto.keyvault)
# nsg_resource = SecurityResource(config_dto.nsg)
# vnet_resource = VirtualNetworkResource(config_dto.vnet)
# vm_resource = VirtualMachineResource(config_dto.vm)
# bastion_resource = BastionHostResource(config_dto.bastion)



# exporting pulumi resources
