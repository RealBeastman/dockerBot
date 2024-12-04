import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import subprocess
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
            else:
                print("Channel not found!")
        except discord.errors.HTTPexception as e:
            print(f"Failed to send message: {e}")
        finally:
            await asyncio.sleep(0.2) # throttle to 5 message/sec (200ms * 5 = 1000ms = 1s)

@bot.event
async def on_ready():
    print(f"Bot is logged in as {bot.user}")
    # Start socket server and message processor
    bot.loop.create_task(relayService.start_server())
    bot.loop.create_task(process_message_queue())

@bot.command(name="run_docker", help="Enter command with two numbers, lower number first. Ex: !run_docker 1 100")
async def run_docker_app(ctx, low_num = 1, high_num = 10):
    print(f'docker run -e LOW={low_num} -e HIGH={high_num} --rm docker-app')
    subprocess.Popen(f'docker run -e LOW={low_num} -e HIGH={high_num} --rm docker-app', shell=True)

# Run the bot
bot.run(TOKEN)