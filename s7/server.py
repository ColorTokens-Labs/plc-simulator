# A simple Siemens S7 simulator for ColorTokens Xshield OT security demos
# You can run this directly on a VM.  For maximum benefit, run this in
# a docker container using bridge networking with an external DHCP server
#
#
# Use these MAC address prefixes when you spin up the container to ensure 
# the Gatekeeper will identify the PLC vendor correctly
#
#     Siemens AG:  00:1B:1B
# 
# TODO: python-snap7 does not have a way to setup the device info for 
# the SZL query.  So this simulator will always return the same hardcoded 
# values for the model, CPU, serial number, etc.
# 
# (C) 2024, ColorTokens Inc.
# Venky Raju

from snap7.server import Server

def main():

    # Create an instance of the snap7 server
    server = Server()
    
    # Start the server (defaul port = 102/tcp)
    server.start()
    print("S7 Simulator started. Waiting for discovery requests...")

    try:
        while True:
            server.pick_event()  # Handle incoming requests
    except KeyboardInterrupt:
        print("Stopping S7 Simulator...")
        server.stop()
        server.destroy()

if __name__ == "__main__":
    main()

