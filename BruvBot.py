import discord

intents = discord.Intents.default()
intents.message_content = True


client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} is operational')

@client.event
async def on_message(message):
    if message.author == client.user:   # This ensures the bot doesn't respond to itself
        return

    movie_list = []
    if message.content.startswith('$addmovie'):   # add movie to list
        with open('movie_list.txt', 'r') as mf:
            for line in mf:
                movie_list.append(line)

        movie = message.content[10:]    # parse movie name and reference against list to avoid duplicates
        if movie in movie_list:
            return

        with open('movie_list.txt', 'a') as mf:
            mf.write(movie)
            mf.write('\n')

        await message.channel.send('Added to list')

    '''if message.content.startswith('$deletemovie'):
        with open('movie_list.txt', 'r') as mf:
            movie_list = []
            for line in mf:
                movie_list.append(line.strip())

        movie = message.content[13:]   # parse movie name
        if movie not in movie_list:
            return
        else:
            movie_list.remove(movie)

        with open('movie_list.txt', 'a') as mf:
            mf.write(movie)
            mf.write('\n')

        await message.channel.send('Deleted from list')'''    # FIXME not working to delete yet

    if message.content.startswith('$movielist'):   # show list of movies. TODO: format this with embed
        with open('movie_list.txt', 'r') as mf:
            movie_list = []
            for line in mf:
                movie_list.append(line.strip('\n'))

        embed = discord.Embed(title='Movies', description='Movie list', color=0x00ff00)

        embed.add_field(name='Movies', value=movie_list, inline=False)

        await message.channel.send(embed=embed)

client.run('MTE4MjM4NjE2ODgzMTE2NDUxNw.GO7pnx.qIe2MeRRbonRNqFB_1uBKvcYw41CQcd5mVKhlk')
