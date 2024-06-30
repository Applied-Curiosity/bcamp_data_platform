
# import sys
# sys.path.append('/workspaces/bcamp_data_platform_azure/infra')

import pulumi
from pulumi_azure_native import compute
from dto import VirtualMachineConfig


class VirtualMachineResource:
    def __init__(self, config:VirtualMachineConfig):
        self.config = config
        self.create_vm()

    def create_vm(self):
        # config = self.config
        virtual_machine = compute.VirtualMachine("virtualMachine",
        hardware_profile=compute.HardwareProfileArgs(
            vm_size=compute.VirtualMachineSizeTypes.STANDARD_D2S_V3,
        ),
        location=self.config.location,
        network_profile=compute.NetworkProfileArgs(
            network_interfaces=[compute.NetworkInterfaceReferenceArgs(
                id="/subscriptions/{subscription-id}/resourceGroups/rg-ac-cus-adb-acclrtor/providers/Microsoft.Network/networkInterfaces/",
                primary=True,
            )],
        ),
        os_profile=compute.OSProfileArgs(
            admin_password=self.config.pw,
            admin_username=self.config.user,
            computer_name=self.config.os_computer_name
        ),
        resource_group_name=self.config.resource_group_name,
        storage_profile=compute.StorageProfileArgs(
            image_reference=compute.ImageReferenceArgs(
                offer="windows-11",
                publisher="microsoftwindowsdesktop"
            ),
            os_disk=compute.OSDiskArgs(
                caching=compute.CachingTypes.READ_WRITE,
                create_option=compute.DiskCreateOptionTypes.FROM_IMAGE,
                managed_disk=compute.ManagedDiskParametersArgs(
                    storage_account_type=compute.StorageAccountTypes.PREMIUM_LRS,
                ),
                name=self.config.os_disk_name,
            ),
        ),
        vm_name="myVM"
        )




        pulumi.export('vm_id', virtual_machine.id)



    def output_dto(self) -> VirtualMachineConfig:
        return self.config
