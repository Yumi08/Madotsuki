import discord 
from discord.ext import commands
from dotenv import load_dotenv
import os
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)

client = commands.Bot(command_prefix = "$")

@client.command()
async def load(ctx, extension):
    client.load_extension(f"Cogs.{extension}")

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"Cogs.{extension}")

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f"Cogs.{extension}")
    client.load_extension(f"Cogs.{extension}")

for filename in os.listdir("./Cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"Cogs.{filename[:-3]}")

@client.event
async def on_ready():
    print("Bot ready.")
    await client.change_presence(activity=discord.Game("I love you."))

client.run(os.getenv("TOKEN"))

