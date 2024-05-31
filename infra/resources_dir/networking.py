# this code can deploy a vnet and other network related resources, works out of __main__, ignore for now

from pulumi_azure_native import resource, compute, network
import pulumi
from pulumi_azure_native import resources, storage, network, compute
import pulumi_tls as tls
from pulumi_random import random_string
import base64

# Import the program's configuration settings
config = pulumi.Config()
vm_name = config.get("vmName", "my-server")
vm_size = config.get("vmSize", "Standard_A1_v2")
os_image = config.get("osImage", "Debian:debian-11:11:latest")
admin_username = config.get("adminUsername", "pulumiuser")
service_port = config.get("servicePort", "80")

os_image_publisher, os_image_offer, os_image_sku, os_image_version = os_image.split(":")

# Create an SSH key
ssh_key = tls.PrivateKey(
    "ssh-key",
    algorithm = "RSA",
    rsa_bits = 4096,
)


# Create a virtual network

config = pulumi.Config()
vm_name = config.get("vmName", "my-server")
vm_size = config.get("vmSize", "Standard_A1_v2")
os_image = config.get("osImage", "Debian:debian-11:11:latest")
admin_username = config.get("adminUsername", "pulumiuser")
service_port = config.get("servicePort", "80")

os_image_publisher, os_image_offer, os_image_sku, os_image_version = os_image.split(":")







virtual_network = network.VirtualNetwork(
    "network",
    resource_group_name=resource_group.name,
    address_space=network.AddressSpaceArgs(
        address_prefixes=[
            "10.0.0.0/16",
        ],
    ),
    subnets=[
        network.SubnetArgs(
            name=f"{vm_name}-subnet",
            address_prefix="10.0.1.0/24",
        ),
    ],
)
# Use a random string to give the VM a unique DNS name
domain_name_label = random_string.RandomString(
    "domain-label",
    length=8,
    upper=False,
    special=False,
).result.apply(lambda result: f"{vm_name}-{result}")

# Create a public IP address for the VM
public_ip = network.PublicIPAddress(
    "public-ip",
    resource_group_name=resource_group.name,
    public_ip_allocation_method=network.IpAllocationMethod.DYNAMIC,
    dns_settings=network.PublicIPAddressDnsSettingsArgs(
        domain_name_label=domain_name_label,
    ),
)

# Create a security group allowing inbound access over ports 80 (for HTTP) and 22 (for SSH)
security_group = network.NetworkSecurityGroup(
    "security-group",
    resource_group_name=resource_group.name,
    security_rules=[
        network.SecurityRuleArgs(
            name=f"{vm_name}-securityrule",
            priority=1000,
            direction=network.AccessRuleDirection.INBOUND,
            access="Allow",
            protocol="Tcp",
            source_port_range="*",
            source_address_prefix="*",
            destination_address_prefix="*",
            destination_port_ranges=[
                service_port,
                "22",
            ],
        ),
    ],
)

# Create a network interface with the virtual network, IP address, and security group
network_interface = network.NetworkInterface(
    "network-interface",
    resource_group_name=resource_group.name,
    network_security_group=network.NetworkSecurityGroupArgs(
        id=security_group.id,
    ),
    ip_configurations=[
        network.NetworkInterfaceIPConfigurationArgs(
            name=f"{vm_name}-ipconfiguration",
            private_ip_allocation_method=network.IpAllocationMethod.DYNAMIC,
            subnet=network.SubnetArgs(
                id=virtual_network.subnets.apply(lambda subnets: subnets[0].id),
            ),
            public_ip_address=network.PublicIPAddressArgs(
                id=public_ip.id,
            ),
        ),
    ],
)
