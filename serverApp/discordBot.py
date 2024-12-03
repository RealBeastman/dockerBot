import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import threading
import asyncio
import relayService

# Discord bot setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
intents.message_content = True

# Discord Token and Channel ID for bot channel
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# Process message queue
async def process_message_queue():
    while True:
        # get message from the queue
        message = await relayService.message_queue.get()
        try:
            channel = bot.get_channel(CHANNEL_ID)
            if channel:
                await channel.send(message) # send message to discord channel
        except discord.errors.HTTPexception as e:
            print(f"Failed to send message: {e}")
        finally:
            await asyncio.sleep(0.2) # throttle to 5 message/sec (200ms * 5 = 1000ms = 1s)

# Run listener server in separate thread
server_thread = threading.Thread(target=relayService.start_server, daemon=True)
server_thread.start()

@bot.event
async def on_ready():
    print(f"Bot is logged in as {bot.user}")
    # Process message queue on startup
    bot.loop.create_task(process_message_queue())

# Run the bot
bot.run(TOKEN)