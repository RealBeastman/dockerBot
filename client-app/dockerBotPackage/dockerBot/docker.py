import socket

# Server config
HOST = "host.docker.internal"
PORT = 5000

def send_message_to_bot(message):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((HOST, PORT))
            client_socket.sendall(message.encode())
            print(f"Message sent to bot: {message}")
    except Exception as e:
        print(f"Error sending message: {str(e)}")