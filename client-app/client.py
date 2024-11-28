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
    markdown_list = [
        "# Big Header", 
        "## Smaller Header", 
        "### Even Smaller Header", 
        "-# Subtext", 
        "**BOLD**",
        ]
    i = 0
    while i < len(markdown_list):
        send_message_to_bot(markdown_list[i])
        i += 1

# Send string to discord bot listener
send_message_to_bot(f"# Hello, this is a message from Docker!")
something_complex()

# add message to queue with timestamp (wrapper)
# FIFO