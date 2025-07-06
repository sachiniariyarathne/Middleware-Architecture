import socket 
import sys 
def start_client(server_ip, server_port):
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((server_ip, server_port))
        print(f"[CLIENT] Connected to server at {server_ip}:{server_port}")
    except:
        print(f"[CLIENT] Unable to connect to {server_ip}:{server_port}")
    
    while 1:
        message = input("You: ")
        if message != '':
            client_socket.sendall(message.encode()) 
            if message.strip().lower() == "terminate":
                print("[CLIENT] Termination signal sent. Disconnecting.")
                break
        else:
            print("Empty message. Try again.")

    client_socket.close()

def main():

    if len(sys.argv) != 3:
        print("Usage: python client.py <SERVER_IP> <PORT>")
    else:
        start_client(sys.argv[1], int(sys.argv[2])) 

if __name__ == '__main__':
    main()