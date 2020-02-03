import discord 
from discord.ext import commands
from dotenv import load_dotenv
import os
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)

client = commands.Bot(command_prefix = "$")

@client.event
async def on_ready():
    print("Bot ready.")
    await client.change_presence(activity=discord.Game("I love you."))

client.run(os.getenv("TOKEN"))

