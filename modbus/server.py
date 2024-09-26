# A simple modbus simulator for ColorTokens Xshield OT security demos
# You can run this directly on a VM.  For maximum benefit, run this in
# a docker container using bridge networking with an external DHCP server
#
# Config files are provided for Rockwell/Allen Bradley and Schneider PLCs
#
# Use these MAC address prefixes when you spin up the container to ensure 
# the Gatekeeper will identify the PLC vendor correctly
#
#     Rockwell:  00:00:BC
#     Schneider: 00:00:54
# 
# (C) 2024, ColorTokens Inc.
# Venky Raju

from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
import sys
import os

def load_config(file_path):
    config = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            config[key] = value
    return config

# Dummy data - we may use this later
def initialize_data_store():

    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [17] * 10),  # Discrete inputs
        co=ModbusSequentialDataBlock(0, [21] * 10),  # Coils
        hr=ModbusSequentialDataBlock(0, [33] * 10),  # Holding registers
        ir=ModbusSequentialDataBlock(0, [45] * 10),  # Input registers
    )
    context = ModbusServerContext(slaves=store, single=True)
    return context

# Device identification response
def initialize_device_identity(config):
    identity = ModbusDeviceIdentification()
    identity.VendorName = config['VendorName']
    identity.ProductCode = config['ProductCode']
    identity.MajorMinorRevision = config['Revision']
    identity.VendorUrl = config['VendorUrl']
    identity.ProductName = config['ProductName']
    identity.ModelName = config['ModelName']
    return identity

# Start the server
def run_server(config):
    context = initialize_data_store()
    identity = initialize_device_identity(config)

    # Modbus server listening on 502
    StartTcpServer(context=context, identity=identity, address=("0.0.0.0", 502))

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: server.py <plc_name>")
        sys.exit(1)

    plc_name = sys.argv[1]

    # The config file is ./config/<plc_name>
    script_dir = os.path.dirname(os.path.abspath(__file__))  
    config_dir = os.path.join(script_dir, 'config')  
    file_path = os.path.join(config_dir, plc_name)  

    config = load_config(file_path)
    run_server(config)
