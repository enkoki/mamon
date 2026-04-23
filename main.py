import asyncio

import discord
from discord.ext import commands
import config

intents = discord.Intents.default()
intents.message_content = True

cogs: list = ["cogs.general", "cogs.github"]

bot = commands.Bot(command_prefix=";", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged In Successfully! Online as: {bot.user}")

async def main():
    async with bot:
        print("Loading cogs...")
        for cog in cogs:
            await bot.load_extension(cog)
        print("Starting the bot...")
        await bot.start(config.BOT_TOKEN)

asyncio.run(main())