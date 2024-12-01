import socket
import asyncio

# Docker config
DOCKER_HOST = "host.docker.internal"
PORT = 5000

# Discord/Server config
SERVER_HOST = "0.0.0.0"

# Message queue
message_queue = asyncio.Queue()

def send_message_to_bot(message):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((DOCKER_HOST, PORT))
            client_socket.sendall(message.encode())
            print(f"Message sent to bot: {message}")
    except Exception as e:
        print(f"Error sending message: {str(e)}")

async def add_to_queue(message):
    await message_queue.put(message)


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((SERVER_HOST, PORT))
        server_socket.listen()
        print(f"Server listening on {SERVER_HOST}:{PORT}")

        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"Connected through {addr}")
                data = conn.recv(1024)
                if not data:
                    break
                message = data.decode("utf-8")
                print(f"Received Message: {message}")
                asyncio.run(add_to_queue(message))