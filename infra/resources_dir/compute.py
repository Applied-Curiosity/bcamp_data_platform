import sys
sys.path.append('/workspaces/bcamp_data_platform_azure/infra')

import pulumi
from pulumi_azure_native import compute
from dto import VirtualMachineConfig


class VirtualMachineResource:
    def __init__(self, config:VirtualMachineConfig):
        self.config = config
        self.create_vm()

    def create_vm(self):
        virtual_machine = compute.VirtualMachine("virtualMachine",
        hardware_profile=compute.HardwareProfileArgs(
            vm_size=compute.VirtualMachineSizeTypes.STANDARD_D2S_V3,
        ),
        location=config.location,
        network_profile=compute.NetworkProfileArgs(
            network_interfaces=[compute.NetworkInterfaceReferenceArgs(
                id="/subscriptions/{subscription-id}/resourceGroups/myResourceGroup/providers/Microsoft.Network/networkInterfaces/{existing-nic-name}",
                primary=True,
            )],
        ),
        os_profile=compute.OSProfileArgs(
            admin_password=config.pw,
            admin_username=config.user,
            computer_name=config.os_computer_name
        ),
        resource_group_name="myResourceGroup",
        storage_profile=compute.StorageProfileArgs(
            image_reference=compute.ImageReferenceArgs(
                offer="UbuntuServer",
                publisher="Canonical",
                sku="16.04-LTS",
                version="latest",
            ),
            os_disk=compute.OSDiskArgs(
                caching=compute.CachingTypes.READ_WRITE,
                create_option=compute.DiskCreateOptionTypes.FROM_IMAGE,
                managed_disk=compute.ManagedDiskParametersArgs(
                    storage_account_type=compute.StorageAccountTypes.PREMIUM_LRS,
                ),
                name=config.os_disk_name,
            ),
        ),
        vm_name="myVM")

        pulumi.export('vm_id', virtual_machine.id)



    def output_dto(self) -> VirtualMachineConfig:
        return self.config
