#!/usr/bin/python3

# region MODULE IMPORTS
import discord
from discord.ext import tasks, commands
import requests
import sqlite3
# endregion

# region CONFIGURE BOT AND ON_READY()
intents = discord.Intents.default()
intents.message_content = True
Bot = commands.Bot(command_prefix="bruv ", intents=intents)

@Bot.event
async def on_ready():
    print(f'{Bot.user} is online.')
    # Begin the update to broadcast steam game updates
    if not steamupdates.is_running():
        steamupdates.start()

    # Create the movie file if it doesn't exit yet
    try:
        with open('movie_list.txt', 'x') as mf:
            pass
    except FileExistsError:
        print("movie_list file already exists")

# endregion

# region MESSAGE REPLIES
@Bot.event
async def on_message(message):
    # Avoid bot responding to itself
    if message.author == Bot.user:
        return
    # get the sender's nickname
    display_name = message.author.display_name

    if "payday" in message.content.lower():
        await message.channel.send(
            f"{display_name}, bruh"
            )
    elif "tarkov" in message.content.lower():
        await message.channel.send(
            f"{display_name}, tarkov bad"
        )

    # continue processing commands
    await Bot.process_commands(message)

# endregion

#  region MOVIE LIST
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

# endregion

# region STEAM GAME NEWS
def GetSteamNews(appid: int, count: int = 5):
    steam_url = f"https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/"
    params = {
        "appid": appid,
        "count": count,
        "maxlength": 0
    }
    response = requests.get(steam_url, params=params)
    response.raise_for_status()
    news_data = response.json()
    return news_data["appnews"]["newsitems"]

@tasks.loop(hours=24)
async def steamupdates():
    # add game appids here
    game_id_dict = {
        'valheim' : 892970,
        # 'bf6' : 2807960,
        'kf3' : 1430190,
        'bf6' : 2807960
    }   
    games_to_check = [val for val in game_id_dict.values()]

    TARGET_CHANNEL = 1410092590732148737
    channel = Bot.get_channel(TARGET_CHANNEL)
    if channel is None:
        channel = await Bot.fetch_channel(TARGET_CHANNEL)

    for game in games_to_check:
        news_items = GetSteamNews(appid=game)
        latest_post = news_items[0]

        title = latest_post['title']
        url = latest_post['url']

        Bot.sql_cursor.execute("SELECT 1 FROM news WHERE url = ?", (url,))
        old_posts = Bot.sql_cursor.fetchone()

        if not old_posts:
            await channel.send(f"** {title} **\n{url}")
            print(f"Insering app id {game} news title {title} into /home/reed/game_news.db\n")
            Bot.sql_cursor.execute("INSERT INTO news (appid, title, url) VALUES (?, ?, ?)",
                               (game, title, url))
            Bot.sql_connect.commit()
        
@steamupdates.before_loop
async def before():
    await Bot.wait_until_ready()

        # Database connect and check
    Bot.sql_connect = sqlite3.connect("/home/reed/game_news.db")
    Bot.sql_cursor = Bot.sql_connect.cursor()

    Bot.sql_cursor.execute("""
        CREATE TABLE IF NOT EXISTS news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        appid INTEGER NOT NULL,
        title TEXT NOT NULL,
        url TEXT NOT NULL UNIQUE,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP               
    );
    """)
    
@steamupdates.after_loop
async def after():
    print("Closing DB connection\n")
    Bot.sql_connect.close()

# endregion
