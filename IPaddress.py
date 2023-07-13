import ipaddress

def calculate_network_info(ip_address, subnet_mask):
    network = ipaddress.ip_network(f"{ip_address}/{subnet_mask}")
    subnet_address = network.network_address
    broadcast_address = network.broadcast_address

    first_host = subnet_address + 1
    last_host = broadcast_address - 1

    return subnet_address, broadcast_address, first_host, last_host
while True:
    ip_address_input = input("Enter the IP address in CIDR notation (e.g., 192.168.0.0/24): ")
    ip_address, subnet_mask = ip_address_input.split("/")

    subnet_address, broadcast_address, first_host, last_host = calculate_network_info(ip_address, subnet_mask)
    print("Subnet Address:", subnet_address)
    print("Broadcast Address:", broadcast_address)
    print("Valid Host Range:", first_host, "-", last_host)

