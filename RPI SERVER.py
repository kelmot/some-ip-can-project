#SOME/IP SERVER

import socket
import struct

# Define the server IP address and port
SERVER_IP = '0.0.0.0'  # Listen on all interfaces
SERVER_PORT = 30490

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the server IP and port
sock.bind((SERVER_IP, SERVER_PORT))

print(f"Listening on {SERVER_IP}:{SERVER_PORT}...")

try:
    while True:
        # Receive data from the client
        data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
        
        # Extract SOME/IP header (16 bytes)
        someip_header = data[:16]
        payload = data[16:]

        # Unpack the SOME/IP header
        SERVICE_ID, METHOD_ID, CLIENT_ID, SESSION_ID, PROTOCOL_VERSION, INTERFACE_VERSION, MESSAGE_TYPE, payload_length = struct.unpack(
            '!HHHHBBBxI', someip_header
        )

        # Print received message details
        print(f"Received message from {addr}:")
        print(f"  Service ID: {SERVICE_ID}")
        print(f"  Method ID: {METHOD_ID}")
        print(f"  Client ID: {CLIENT_ID}")
        print(f"  Session ID: {SESSION_ID}")
        print(f"  Protocol Version: {PROTOCOL_VERSION}")
        print(f"  Interface Version: {INTERFACE_VERSION}")
        print(f"  Message Type: {MESSAGE_TYPE}")
        print(f"  Payload Length: {payload_length}")
        try:
            payload_string = payload.decode('utf-8')
            print(f"  Payload: {payload_string}")
        except UnicodeDecodeError:
            payload_string = "<Unable to decode payload as UTF-8>"
            print(f"  Payload: {payload_string}")

        # Determine the response based on the payload
        if payload_string == "BUTTON PRESSED":
            response_payload = "LED ON".encode('utf-8')
        else:
            response_payload = "LED OFF".encode('utf-8')

        # Send the response back to the client
        sock.sendto(response_payload, addr)
        print(f"Response sent to {addr}: {response_payload.decode('utf-8')}")
        
finally:
    # Close the socket
    sock.close()