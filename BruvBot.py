#!/usr/bin/python3

import discord
from discord.ext import tasks, commands
import asyncio

# Configure Bot
intents = discord.Intents.default()
intents.message_content = True
Bot = commands.Bot(command_prefix="bruv ", intents=intents)

@Bot.event
async def on_ready():
    print(f'{Bot.user} is online.')

# Create the movie file if it doesn't exit yet
try:
    with open('movie_list.txt', 'x') as mf:
        pass
except FileExistsError:
    print("movie_list file already exists")

@Bot.event
async def on_message(message):
    # Avoid bot responding to itself
    if message.author == Bot.user:
        return
    # get the sender's nickname
    display_name = message.author.display_name

    if "payday" in message.content.lower():
        await message.channel.send(
            f"Ayo {display_name} I heard payday had an update JK GO TOUCH GRASS"
            )
    # continue processing commands
    await Bot.process_commands(message)

#################################
#     Movie List Commands       #
#################################
@Bot.command()
async def addmovie(ctx, *, movie: str):
    with open('movie_list.txt', 'a+') as mf:
        mf.seek(0)
        mf_content = mf.read()
        if movie.lower() in mf_content:
            await ctx.send(f"```{movie} is already in the list```")
        else:
            mf.write(movie.lower())
            mf.write("\n")
            await ctx.send('```Movie added to List```')

@Bot.command()
async def showmovies(ctx):
    with open('movie_list.txt', 'r') as mf:
        mf.seek(0)
        mf_content = mf.read()
        await ctx.send("Complete list of movies:\n" + mf_content)

@Bot.command()
async def deletemovie(ctx, *, movie: str):
    with open('movie_list.txt', 'w+') as mf:
        movie_list = [line for line in mf if line != movie.lower() + "\n"]
        mf.writelines(movie_list)
    await ctx.send(f"{movie} deleted from list")
