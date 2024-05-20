yamlCopy code
networking:
  vnet_name: dev-vnet
  address_space: "10.0.0.0/16"
  subnets:
    - name: subnet1
      address_prefix: "10.0.1.0/24"
    - name: subnet2
      address_prefix: "10.0.2.0/24"
  nsg:
    - name: dev-nsg
      rules:
        - name: allow-ssh
          priority: 100
          direction: Inbound
          access: Allow
          protocol: Tcp
          source_port_range: "*"
          destination_port_range: "22"
          source_address_prefix: "*"
          destination_address_prefix: "*"
