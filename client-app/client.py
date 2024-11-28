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

def something_complex():
    i = 0
    while i < 20:
        i = i + 1
        send_message_to_bot(f"Added 1 to {i -1}. Your new number is {i}")

# Send string to discord bot listener
send_message_to_bot("Hello, this is a message from Docker!")
something_complex()

# add message to queue with timestamp (wrapper)
# FIFO