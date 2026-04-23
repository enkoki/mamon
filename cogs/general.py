import discord
from discord.ext import commands
from discord import app_commands
from config import GUILD_ID

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="hello", description="Say Hello!")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hi there!")

    @app_commands.command(name="say", description="Repeat text")
    async def say(self, interaction: discord.Interaction, string: str):
        await interaction.response.send_message(string)

async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot), guild=GUILD_ID)