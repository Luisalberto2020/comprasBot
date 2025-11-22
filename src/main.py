import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
from WebScrapping import WebScraper
import asyncio


load_dotenv()

intents = discord.Intents.default()  # Enable the message content intent

bot = commands.Bot(command_prefix='!', intents=intents)

bot.remove_command('help')

async def daily_task():
    user = await bot.fetch_user(int(os.getenv('DISCORD_USER_ID')))
    user2 = await bot.fetch_user(int(os.getenv('DISCORD_USER_ID2')))
    scraper = WebScraper()
    await scraper.scrape_fenixsim(lambda message:  (
        asyncio.create_task(user.send(message)),
        asyncio.create_task(user2.send(message))
    ))

#shutdown afer 1 minute
async def shutdown():
    await asyncio.sleep(60)
    await bot.close()




@bot.event
async def on_ready():
    await daily_task()
    print(f'Logged in as {bot.user}')
    asyncio.create_task(shutdown())
    
    
    

bot.run(str(os.getenv('DISCORD_TOKEN')))