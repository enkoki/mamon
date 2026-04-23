import os
import discord
from dotenv import load_dotenv
load_dotenv()

# Bot Configurations
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_STATUS = os.getenv("BOT_STATUS")

# Others
GUILD_ID = discord.Object(id=os.getenv("GUILD_ID"))
OWNER_ID = os.getenv("OWNER_ID")
