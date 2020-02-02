import discord 
from discord.ext import commands
from dotenv import load_dotenv
import os
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)

client = commands.Bot(command_prefix = "$")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please pass in all required arguments!")
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("Check error!")
    else:
        await ctx.send("Error!")

@client.command()
async def load(ctx, extension):
    client.load_extension(f"Cogs.{extension}")
    await ctx.send(f"Loaded {extension}.")

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"Cogs.{extension}")
    await ctx.send(f"Unloaded {extension}.")

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f"Cogs.{extension}")
    client.load_extension(f"Cogs.{extension}")
    await ctx.send (f"Reloaded {extension}.")

print("Loading cogs.")
for filename in os.listdir("./Cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"Cogs.{filename[:-3]}")

@client.event
async def on_ready():
    print("Bot ready.")
    await client.change_presence(activity=discord.Game("I love you."))

client.run(os.getenv("TOKEN"))

