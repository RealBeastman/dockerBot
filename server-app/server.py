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

# Discord Token and Channel ID for bot channel
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# Message queue to prevent rate limiting on sent messages
message_queue = asyncio.Queue() # FIFO

# Process message queue
async def process_message_queue():
    while True:
        # get message from the queue
        channel_id, message = await message_queue.get()
        try:
            channel = bot.get_channel(channel_id)
            if channel:
                await channel.send(message) # send message to discord channel
            else:
                print(f"Channel with ID {channel_id} not found.")
        except discord.errors.HTTPexception as e:
            print(f"Failed to send message: {e}")
        finally:
            await asyncio.sleep(0.2) # throttle to 5 message/sec (200ms * 5 = 1000ms = 1s)


async def add_to_queue(channel_id, message):
    await message_queue.put((channel_id, message))

# Start server to begin listening on defined host/port
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Server listening on {HOST}:{PORT}")

        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"Connected through {addr}")
                data = conn.recv(1024)
                if not data:
                    break
                message = data.decode("utf-8")
                print(f"Received message: {message}")
                asyncio.run_coroutine_threadsafe(add_to_queue(CHANNEL_ID, message), bot.loop)

# Run server in separate thread
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()

@bot.event
async def on_ready():
    print(f"Bot is logged in as {bot.user}")

    # Process message queue on startup
    bot.loop.create_task(process_message_queue())

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