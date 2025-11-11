import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
from datetime import time
from zoneinfo import ZoneInfo
from WebScrapping import WebScraper
import asyncio


load_dotenv()

intents = discord.Intents.default()  # Enable the message content intent

bot = commands.Bot(command_prefix='!', intents=intents)

bot.remove_command('help')

@tasks.loop(time=time(11, 0, tzinfo=ZoneInfo("Europe/Madrid")))
async def daily_task():
    user = await bot.fetch_user(int(os.getenv('DISCORD_USER_ID')))
    user2 = await bot.fetch_user(int(os.getenv('DISCORD_USER_ID2')))
    scraper = WebScraper()
    await scraper.scrape_fenixsim(lambda message: asyncio.create_task(user.send(message), user2.send(message)))

   

@bot.event
async def on_ready():
    if not daily_task.is_running():
        daily_task.start()
    print(f'Logged in as {bot.user}')
    status = discord.Status.online
    await bot.change_presence(status=status)

bot.run(os.getenv('DISCORD_TOKEN'))