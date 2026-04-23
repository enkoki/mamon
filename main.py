import asyncio
import discord
from discord.ext import commands
import config

from rich.logging import RichHandler
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="%H:%M:%S",
    handlers=[RichHandler()]
)
# # If you want to remove the warning related to PyNaCl and davey
# logging.getLogger("discord").setLevel(logging.ERROR) 

log = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True

cogs: list = ["cogs.general", "cogs.github"]

bot = commands.Bot(command_prefix=";", intents=intents)

@bot.event
async def on_ready():
    log.info(f"Logged in successfully! Online as {bot.user}")

async def main():
    async with bot:
        log.info("Loading cogs...")
        for cog in cogs:
            try:
                await bot.load_extension(cog)
                log.info(f"Loaded {cog}")
            except Exception as e:
                log.error(f"Failed to load {cog}: {e}")
        log.info("Starting the bot...")
        await bot.start(config.BOT_TOKEN)

asyncio.run(main())
