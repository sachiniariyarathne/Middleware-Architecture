import socket 
import sys 
def start_server(port):
    
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind(('', port))
    server_socket.listen(1) 
    print(f"✅ [SERVER] Listening on port {port}")

    client_socket, client_address = server_socket.accept()
    print(f"✅ [SERVER] Connected to client at {client_address[0]}:{client_address[1]}")

    while 1:
        message = client_socket.recv(2048).decode('utf-8')
        if message != '':
            print(f"[CLIENT] {message}")

            if message.strip().lower() == "terminate":
                print("🛑 [SERVER] Termination signal received. Closing connection.")
                break
        else:
            print("🛑 [SERVER] Received empty message. Closing connection.")
            break

    client_socket.close()
    server_socket.close()

def main():

    if len(sys.argv) != 2:
        print("Usage: python server.py <PORT>")
    else:
        start_server(int(sys.argv[1])) 

if __name__ == '__main__':
    main()