import asyncio
import discord
from discord.ext import commands
import config
import time

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

cogs: list = ["cogs.general", "cogs.github", "cogs.info"]

bot = commands.Bot(command_prefix=";", intents=intents)

async def setup_hook():
    log.info("Loading cogs...")
    bot.start_time = time.time()
    for cog in cogs:
        try:
            await bot.load_extension(cog)
            log.info(f"Loaded {cog}")
        except Exception as e:
            log.error(f"Failed to load {cog}: {e}")
    synced = await bot.tree.sync(guild=config.GUILD_ID)
    log.info(f"Synced {len(synced)} commands")
    log.info("Starting the bot...")

bot.setup_hook = setup_hook

@bot.event
async def on_ready():
    log.info(f"Logged in successfully! Online as {bot.user}")
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(config.BOT_STATUS)
    )

async def main():
    async with bot:
        await bot.start(config.BOT_TOKEN)

asyncio.run(main())
