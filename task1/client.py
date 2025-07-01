import socket # For socket programming
import sys # To access command-line arguments

def start_client(server_ip, server_port):
    
    # Create a client (IPv4 TCP)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((server_ip, server_port))
        print(f"[CLIENT] Connected to server at {server_ip}:{server_port}")
    except:
        print(f"[CLIENT] Unable to connect to {server_ip}:{server_port}")
    
    # Keep sending messages until 'terminate' is typed
    while 1:
        message = input("You: ")
        if message != '':
            client_socket.sendall(message.encode()) # Send encoded message to server
            if message.strip().lower() == "terminate":
                print("[CLIENT] Termination signal sent. Disconnecting.")
                break
        else:
            print("Empty message. Try again.")
    
     # Close connections (after exiting while loop due to break)
    client_socket.close()

def main():
    
    # Expect exactly two arguments: server IP and port
    if len(sys.argv) != 3:
        print("Usage: python client.py <SERVER_IP> <PORT>")
    else:
        start_client(sys.argv[1], int(sys.argv[2])) 
        # IP address is sent as a string sys.argv[1]
        # Port is sent as an integer int(sys.argv[2])

if __name__ == '__main__':
    main()