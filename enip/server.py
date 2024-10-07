# A simple EtherNet/IP simulator for ColorTokens Xshield OT security demos
# You can run this directly on a VM.  For maximum benefit, run this in
# a docker container using bridge networking with an external DHCP server
#
#
# Use these MAC address prefixes when you spin up the container to ensure 
# the Gatekeeper will identify the PLC vendor correctly
#
#     Rockwell:  00:00:BC
#
# Sources:
#    1. EIP Stack Group, OpENer project (https://github.com/EIPStackGroup/OpENer/)
#    2. ODVA CIP Spec:
#       https://www.odva.org/wp-content/uploads/2020/06/PUB00123R1_Common-Industrial_Protocol_and_Family_of_CIP_Networks.pdf
#    3. Nmap enip-info source: https://github.com/nmap/nmap/blob/master/scripts/enip-info.nse
# 
# (C) 2024, ColorTokens Inc.
# Venky Raju

import socket
import struct
from random import random

def get_interface_ip_bytes():

    try:
        ip_address = socket.gethostbyname(socket.gethostname())
    except socket.gaierror:
        print('Error determining IP address, using localhost')
        ip_address = "127.0.0.1"

    return bytes(map(int, ip_address.split('.')))

# Generate a 9 digit serial number and return as bytes
def gen_serial_num_bytes():
    n = int(random()*1E9)
    return list(n.to_bytes(4, byteorder='little', signed=False))

def handle_cip_discovery(data, product_name):
    if len(data) >= 24 and data[0] == 0x63 and data[2:4] == b'\x00\x00':

        my_ip_bytes = get_interface_ip_bytes()
        product_name_bytes = product_name.encode(encoding="utf-8")
        serial_num_bytes = gen_serial_num_bytes()

        response = bytearray([
            0x63, 0x00,                 # Command: ListIdentity Response
            0xFF, 0x00,                 # Length: To be computed later
            0x00, 0x00, 0x00, 0x00,     # Session Handle
            0x00, 0x00, 0x00, 0x00,     # Status (0, success)
            0x00, 0x00, 0x00, 0x00,     # Sender Context
            0x00, 0x00, 0x00, 0x00,     # Sender Context
            0x00, 0x00, 0x00, 0x00,     # Options
            0x01, 0x00,                 # Item count
            0x0C, 0x00,                 # Type ID: ListIdentity Response
            0xFF, 0x00,                 # Length: To be computed later
            0x01, 0x00,                 # Protocol version 1
            0x00, 0x02,                 # Flags
            0xAF, 0x12,                 # Port 44818
        ])
        response.extend(my_ip_bytes)    # Set the IP address
        response.extend([
            0x00, 0x00, 0x00, 0x00,     # Zero padding
            0x00, 0x00, 0x00, 0x00,     # Zero padding           
            0x01, 0x00,                 # Vendor ID: Rockwell Automation/Allen-Bradley
            0x0E, 0x00,                 # Device Type: PLC
            0xE6, 0x06,                 # Product Code: 1766
            0x02, 0x01,                 # Revision: 2.1
            0x00, 0x00,                 # Status: 0
        ])
        response.extend(serial_num_bytes)           # Serial number (4 bytes)
        response.extend([len(product_name_bytes)])  # Product Name Length
        response.extend(product_name_bytes)         # Product Name
        response.extend([ 0xFF ])                   # State

        # Fill in the lengths
        response_len = len(response)
        response[2] = response_len - 24             # PDU length
        response[28] = response_len - 30            # Item length

        return response
    return None

def main():
    host = '0.0.0.0'  # Listen on all available interfaces
    port = 44818  # Standard port for CIP/EtherNet/IP
    product_name = 'MicroLogix 1400'

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Listening for CIP discovery requests on {host}:{port}")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                data = conn.recv(1024)
                if not data:
                    continue

                response = handle_cip_discovery(data, product_name)
                if response:
                    conn.sendall(response)
                    print(f"Sent CIP discovery response")
                else:
                    print("Received non-CIP discovery request")

if __name__ == "__main__":
    main()
