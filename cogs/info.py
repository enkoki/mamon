import discord
from discord.ext import commands
from discord import app_commands
from config import GUILD_ID, OWNER_ID, BOT_INVITE
from settings import BOT_NAME, VERSION, DEFAULT_COLOR
from core.uptime import get_uptime
from datetime import datetime

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="info", description="Learn about ${BOT_NAME}")
    async def info(self, interaction: discord.Interaction):
        owner = await self.bot.fetch_user(OWNER_ID)
        embed = discord.Embed(
            color=discord.Colour.from_str(DEFAULT_COLOR),
            timestamp=datetime.now(),
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.display_avatar.url)
        embed.add_field(name="Version", value=VERSION)
        embed.add_field(name="Library", value="discord.py")
        embed.add_field(name="Developer", value=owner.name)
        embed.add_field(name="Ping", value=f'{round(self.bot.latency * 1000)}ms')
        embed.add_field(name="Servers", value=len(self.bot.guilds))
        embed.add_field(name="Commands", value=len(self.bot.tree.get_commands())) # guild scope
        embed.add_field(name="Invite", value=f"[Click here]({BOT_INVITE})")
        embed.set_footer(text=f'{self.bot.user.id} • Uptime {get_uptime(self.bot)}')
        
        await interaction.response.send_message(embed=embed)
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Info(bot), guild=GUILD_ID)