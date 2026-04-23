import os
import discord
from dotenv import load_dotenv
load_dotenv()

# Bot Configurations
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Others
ID = os.getenv("GUILD_ID")
GUILD_ID = discord.Object(id=ID)
OWNER_ID = os.getenv("OWNER_ID")
