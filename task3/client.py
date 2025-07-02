import socket
import sys
import threading

def receive_messages(client_socket):
    while 1:
        try:
            message = client_socket.recv(2048).decode()
            if message:
                print(f"[MESSAGE] {message}")
            else:
                break
        except:
            break

def start_client(ip, port, role, topic):

    role = role.upper()
    if role not in ["PUBLISHER", "SUBSCRIBER"]:
        print("Role must be PUBLISHER or SUBSCRIBER.")
        return
    topic=topic.upper()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((ip, port))

    except:
        print("Failed to connect to server.")
        return

    #Send role and topic to server
    client_socket.sendall(f"{role},{topic}".encode())

    if role == "PUBLISHER":
        print(f"You are a Publisher on topic '{topic}'. Type messages to send. Type 'terminate' to exit.")
        while 1:
            message = input()
            client_socket.sendall(message.encode())
            if message.strip().lower() == "terminate":
                break

    elif role == "SUBSCRIBER":
        print(f"You are a Subsciber to topic '{topic}'. Waiting for messages...")
        receive_messages(client_socket)

    client_socket.close()

def main():
    if len(sys.argv) != 5:
        print("Usage: python client.py <SERVER_IP> <PORT> <PUBLISHER>|<SUBSCRIBER> <TOPIC>")
    else:
        start_client(sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4])

if __name__ == '__main__':
    main()