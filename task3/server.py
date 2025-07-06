import socket
import threading
import sys

topic_subscribers = {} 
lock = threading.Lock() 

def handle_client(client_socket, client_address):
    try:

        initial_data = client_socket.recv(2048).decode().strip()
        if ',' not in initial_data:
            print(f"🛑 [{client_address}] Invalid format. Expected 'ROLE,TOPIC'. Closing connection.")
            client_socket.close()
            return

        client_role, client_topic = initial_data.split(',', 1)
        client_role = client_role.strip().upper()
        client_topic = client_topic.strip().upper()

        print(f"[{client_address}] Role: {client_role}, Topic: {client_topic}")


        with lock:
            if client_role == "SUBSCRIBER":
                if client_topic not in topic_subscribers:
                    topic_subscribers[client_topic] = []
                topic_subscribers[client_topic].append(client_socket)

            elif client_role != "PUBLISHER":
                print(f"🛑 [{client_address}] Invalid role. Closing connection.")
                client_socket.close()
                return

        if client_role == "PUBLISHER":

            while True:
                message = client_socket.recv(2048).decode()
                if not message or message.strip().lower() == "terminate":
                    print(f"[PUBLISHER {client_address}] Disconnected.")
                    break

                print(f"[PUBLISHER {client_address}] [{client_topic}] {message.strip()}")


                with lock:
                    subscribers = topic_subscribers.get(client_topic, [])
                    for sub in subscribers:
                        try:
                            formatted_message = f"[{client_topic}] {message.strip()}"
                            sub.sendall(formatted_message.encode())
                        except:
                            continue

        elif client_role == "SUBSCRIBER":

            while True:
                try:
                    data = client_socket.recv(2048)
                    if not data:
                        break
                except:
                    break

    except Exception as e:
        print(f"[ERROR] {e}")

    finally:
        # Cleanup on client disconnect
        with lock:
            if client_role == "SUBSCRIBER":
                if client_topic in topic_subscribers:
                    if client_socket in topic_subscribers[client_topic]:
                        topic_subscribers[client_topic].remove(client_socket)

        client_socket.close()
        print(f"[DISCONNECTED] {client_address}")

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen(10)
    print(f"✅ [SERVER] Listening on port {port}")

    while True:
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
