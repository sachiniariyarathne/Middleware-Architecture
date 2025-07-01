import socket
import threading
import sys

subscribers_list = [] # List of subscriber sockets
publishers_list = [] # List of publisher sockets
lock = threading.Lock() # Thread-safe access to lists

def handle_client(client_socket, client_address):
    try:
        # Receive role: PUBLISHER or SUBSCRIBER
        client_role = client_socket.recv(2048).decode().strip().upper()
        print(f"[{client_address}] Role: {client_role}")

        # Register client
        with lock:
            if client_role == "PUBLISHER":
                publishers_list.append(client_socket)
            elif client_role == "SUBSCRIBER":
                subscribers_list.append(client_socket)
            else:
                print(f"[{client_address}] Invalid role. Closing connection.")
                client_socket.close()
                return

        if client_role == "PUBLISHER":
            # Listen for messages from the publisher
            while 1:
                message = client_socket.recv(2048).decode()

                if not message or message.strip().lower() == "terminate":
                    print(f"[PUBLISHER {client_address}] Disconnected.")
                    break

                print(f"[PUBLISHER {client_address}] {message.strip()}")

                # Forward the message from the publisher to all subscribers
                with lock:
                    for sub in subscribers_list:
                        try:
                            formatted_message = f"[PUBLISHER {client_address}]" + message
                            sub.sendall(formatted_message.encode())
                        except:
                            continue
        
        elif client_role == "SUBSCRIBER":
            # Subscriber does nothing but wait to receive
            while 1:
                try:
                    data = client_socket.recv(2048)
                    if not data:
                        break
                except:
                    break

    except Exception as e:
        print(f"[ERROR] {e}")
    
    finally:
        # Remove client on exit
        with lock:
            if client_socket in publishers_list:
                publishers_list.remove(client_socket)
            if client_socket in subscribers_list:
                subscribers_list.remove(client_socket)
        
        client_socket.close()

def start_server(port):
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen(10)
    print(f"[SERVER] Listening on port {port}")

    while 1:
        client_socket, client_address = server_socket.accept()
        print(f"[NEW CONNECTION] {client_address}")
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

def main():
    if len(sys.argv) != 2:
        print("Usage: python server.py <PORT>")
    else:
        start_server(int(sys.argv[1]))

if __name__ == '__main__':
    main()