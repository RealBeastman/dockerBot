import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import socket
import threading
import asyncio
import subprocess

# Discord bot setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
intents.message_content = True

# Server setup to listen for docker processes
HOST = "0.0.0.0" # Bind to all available interfaces
PORT = 5000      # Port to host server

# Channel ID to send messages to
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# Handle connections from docker container
def handle_docker(client_socket, address):
    print(f"New connection from {address}")
    with client_socket:
        while True:
            try:
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                print(f"Received from {address}: {data}")
                asyncio.run_coroutine_threadsafe(send_to_discord(data), bot.loop) # I don't know what this does...
            except ConnectionResetError:
                break
        print(f"Connection closed: {address}")

async def send_to_discord(message):
    channel = bot.get_channel(CHANNEL_ID)
    if channel is None:
        print(f"Error: Could not find channel with ID {CHANNEL_ID}. Verify channel ID.")
        return
    
    try:
        # Attempt to send the message to the channel
        await channel.send(message)
        print(f"Message sent to discord channel: {message}")
    except Exception as e:
        print(f"Error sending message to discord: {str(e)}")

# Start TCP server to begin listening for connections from docker container on same port
def start_server():
    print(f"Starting server on {HOST}:{PORT}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # allows multi-access to same port
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print("Server is listening for connections...")
        while True:
            client_socket, address = server_socket.accept()
            threading.Thread(target=handle_docker, args=(client_socket, address), daemon=True).start()

# Start the server in a separate thread
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()

# Check if CHANNEL_ID exists on startup
@bot.event
async def on_ready():
    print(f"Bot is logged in as {bot.user}")
    channel = bot.get_channel(CHANNEL_ID)

    if channel:
        print(f"Found channel: {channel}")
    else:
        print(f"Could not find channel ID: {channel}")

# Run a basic docker app, then remove container when app is finished
@bot.command(name="run_docker")
async def run_docker(ctx):
    channel = bot.get_channel(CHANNEL_ID)
    command = "docker run --rm client-app"

    try:
        subprocess.run(command, shell=True, text=True, capture_output=True)
    except Exception as e:
        await channel.send(f"Error running command: {str(e)}")

# Run the bot
bot.run(TOKEN)