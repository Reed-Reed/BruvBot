"""
Discord Bot
Author: Reed Murray

This program joins a discord bot to the bruv village discord server. It uses asynchronous functions to
respond to messages and track data.

Current features:
    - Movie list: tracks a list of movies to watch in the discord chat together
"""

import discord

# Setup for the discord connection and permissions.
intents = discord.Intents.default()
intents.message_content = True


client = discord.Client(intents=intents)

# Provides indication in the console that the bot is connected.
@client.event
async def on_ready():
    print(f'{client.user} is operational')

""" 
The following section is the Movie list tracker. 
The first branch adds a movie when '$addmovie' is the message prefix. It adds a movie to the list.
The file is kept in the format of movie names separated by newlines. 
"""
@client.event
async def on_message(message):
    if message.author == client.user:   # This ensures the bot doesn't respond to itself
        return

    movie_list = []

    if message.content.startswith('$addmovie'):   # populate list with movie names from file
        with open('movie_list.txt', 'r') as mf:
            for line in mf:
                movie_list.append(line.strip())

        movie = message.content[10:]   # parse movie name and reference against list to avoid duplicates
        print(movie)
        if movie in movie_list:
            return

        with open('movie_list.txt', 'a') as mf:     # add the movie to the end of the file, then a newline.
            mf.write(movie)
            mf.write('\n')

        await message.channel.send('Added to list')

# This branch deletes a movie when prefixed with $deletemovie.
    if message.content.startswith('$deletemovie'):
        with open('movie_list.txt', 'r') as mf:
            movie_list = []
            for line in mf:
                movie_list.append(line.strip())

        print(movie_list)

        movie = message.content[13:]     # parse movie name and reference against list to avoid duplicates
        if movie not in movie_list:
            return
        else:
            movie_list.remove(movie)

        with open('movie_list.txt', 'w') as mf:
            for movie in movie_list:
                mf.write(movie)
                mf.write('\n')

        await message.channel.send('Deleted from list')

# This branch lists the movies via message in discord chat. The message is in a crude format currently.
    if message.content.startswith('$movielist'):
        with open('movie_list.txt', 'r') as mf:
            movie_list = []
            for line in mf:
                movie_list.append(line.strip('\n'))

        embed = discord.Embed(title='Movies', description='Movie list', color=0x00ff00)

        embed.add_field(name='Movies', value=movie_list, inline=False)

        await message.channel.send(embed=embed)  # TODO: format this to look like a cleaner and organized list

client.run('MTE4MjM4NjE2ODgzMTE2NDUxNw.GO7pnx.qIe2MeRRbonRNqFB_1uBKvcYw41CQcd5mVKhlk')
