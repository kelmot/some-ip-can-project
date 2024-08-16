#SOME/IP CLIENT


import socket
import struct
import can


can_interface = 'can0'

# Setup CAN interface
bus = can.interface.Bus(can_interface, bustype='socketcan', bitrate=500000)

# Define the service ID, instance ID, method ID, and other fields
SERVICE_ID = 0x1234
INSTANCE_ID = 0x5678
METHOD_ID = 0x9ABC
CLIENT_ID = 0x0001
SESSION_ID = 0x0001
PROTOCOL_VERSION = 0x01
INTERFACE_VERSION = 0x01
MESSAGE_TYPE = 0x00  # Request
RETURN_CODE = 0x00   # OK

# Define the server IP address and port
SERVER_IP = '10.20.0.43'
SERVER_PORT = 30490

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    while True:
        # Wait for a message from the CAN bus
        message = bus.recv()
        
        
        if message:
            # Encode the CAN message data to bytes (assuming data is in message.data)
            if(message.arbitration_id==0x200):
                payload= b'BUTTON PRESSED'
            else:
                payload=b'BUTTON RELEASED'
            # Calculate the payload length
            payload_length = len(payload)
            
            # Create the SOME/IP header
            someip_header = struct.pack(
                '!HHHHBBBxI',  # Format: network byte order
                SERVICE_ID,
                METHOD_ID,
                CLIENT_ID,
                SESSION_ID,
                PROTOCOL_VERSION,
                INTERFACE_VERSION,
                MESSAGE_TYPE,
                payload_length
            )
            
            # Combine the header and payload
            someip_message = someip_header + payload
            
            #Send the SOME/IP message to the server
            sock.sendto(someip_message, (SERVER_IP, SERVER_PORT))
            
            response, addr = sock.recvfrom(1024)
            # Buffer size is 1024 bytes
            response_message = response.decode('utf-8')

            print(f"Received response from {addr}: {response.decode('utf-8')}")
            if response_message == "LED ON":
                response_can_message = can.Message(arbitration_id=0x300, data=b'\x01')
            else:
                response_can_message = can.Message(arbitration_id=0x400, data=b'\x00')

            bus.send(response_can_message)
            print(f"CAN message sent with ID: {response_can_message.arbitration_id}")


finally:
    # Close the socket
    sock.close()