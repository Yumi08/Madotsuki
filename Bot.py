import discord 
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import logging
from Data import Data
import pickle

## Begin setup
load_dotenv()
logging.basicConfig(level=logging.INFO)

client = commands.Bot(command_prefix = "$")

data = Data()

# Load data
if os.path.exists("data.pkl"):
    with open("data.pkl", "rb") as file:
        data = pickle.load(file)
## End setup

def is_developer(ctx):
    return ctx.author.id == int(os.getenv("OWNERID"))

## Begin events
@client.event
async def on_ready():
    autosave.start()
    await client.change_presence(activity=discord.Game("I love you."))
    print("Bot ready.")

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

    await ctx.send(error)
## End events

## Begin tasks
@tasks.loop(minutes=15)
async def autosave():
    print("Autosaving...")
    
    # Save data
    with open("data.pkl", "wb") as output:
        pickle.dump(data, output, pickle.HIGHEST_PROTOCOL)
## End tasks

## Begin commands
@client.command()
@commands.check(is_developer)
async def load(ctx, extension):
    client.load_extension(f"Cogs.{extension}")
    await ctx.send(f"Loaded {extension}.")

@client.command()
@commands.check(is_developer)
async def unload(ctx, extension):
    client.unload_extension(f"Cogs.{extension}")
    await ctx.send(f"Unloaded {extension}.")

@client.command()
@commands.check(is_developer)
async def reload(ctx, extension):
    client.reload_extension(f"Cogs.{extension}")
    await ctx.send (f"Reloaded {extension}.")

@client.command()
@commands.check(is_developer)
async def logout(ctx):
    await ctx.send("Logging out...")

    # Save data
    with open("data.pkl", "wb") as output:
        pickle.dump(data, output, pickle.HIGHEST_PROTOCOL)

    await client.logout()
## End commands

## Begin finalization
print("Loading cogs.")
for filename in os.listdir("./Cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"Cogs.{filename[:-3]}")

client.run(os.getenv("TOKEN"))
## End finalization
