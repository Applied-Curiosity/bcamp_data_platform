"""An Azure RM Python Pulumi program"""

import pulumi
import yaml
import json
from pulumi_azure_native import resources
from resources_dir.storage import StorageResource
from dto import ConfigDTO



# Create an Azure Resource Group
# Naming convention is
# rg = resource group
# ac = Applied Curiosity
# cus = Central US
# adb = Azure Databricks
# acclrtor = Accelerator


stack = pulumi.get_stack()
config_path = f'Pulumi.dev1.yaml'

with open(config_path, 'r') as file:
     config_data = yaml.safe_load(file)

config_dto = ConfigDTO.from_dict(config_data)

storage_resource = StorageResource(config_dto.storage)

pulumi.export('storage_resource_outputs', storage_resource.output_dto().outputs)
