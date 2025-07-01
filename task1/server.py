import socket # For socket programming
import sys # To access command-line arguments

def start_server(port):
    
    # Create a server (IPv4 TCP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the server to localhost on the given port
    server_socket.bind(('', port))
    server_socket.listen(1) # Allow 1 client connection at a time
    print(f"[SERVER] Listening on port {port}")

    # Accept connection from a client
    client_socket, client_address = server_socket.accept()
    print(f"[SERVER] Connected to client at {client_address[0]}:{client_address[1]}")

    # Start receiving messages from client
    while 1:
        message = client_socket.recv(2048).decode('utf-8')
        if message != '':
            print(f"[CLIENT] {message}")

            # Terminate connection if 'terminate' is received
            if message.strip().lower() == "terminate":
                print("[SERVER] Termination signal received. Closing connection.")
                break
        else:
            print("[SERVER] Received empty message. Closing connection.")
            break

    # Close connections (after exiting while loop due to break)
    client_socket.close()
    server_socket.close()

def main():
    #  Expect exactly one command-line argument: the port number
    if len(sys.argv) != 2:
        print("Usage: python server.py <PORT>")
    else:
        start_server(int(sys.argv[1])) # Convert the port number into an integer and pass as an argument to start_server() function

if __name__ == '__main__':
    main()