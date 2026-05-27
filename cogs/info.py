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
    
    @app_commands.command(name="info", description=f"Learn about {BOT_NAME}")
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
        
    @app_commands.command(name="serverinfo", description="Get details of the server")
    async def _serverinfo(self, interaction: discord.Interaction):
        guild = interaction.guild

        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        categories = len(guild.categories)

        bots = sum(1 for m in guild.members if m.bot)
        humans = guild.member_count - bots

        embed = discord.Embed(
            title=guild.name,
            color=discord.Colour.from_str(DEFAULT_COLOR),
            timestamp=datetime.now()
        )

        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        embed.add_field(name="Owner", value=f"<@{guild.owner_id}>")
        # embed.add_field(name="Created", value=f"<t:{int(guild.created_at.timestamp())}:R>")
        embed.add_field(name="ID", value=guild.id)
        embed.add_field(name="Members", value=f"{humans} ({bots})")
        embed.add_field(name="Categories", value=f"{categories}")
        embed.add_field(name="Text Channels", value=f"{text_channels}")
        embed.add_field(name="Voice Channels", value=f"{voice_channels}")
        embed.add_field(name="Boost", value=f"Level {guild.premium_tier} ({guild.premium_subscription_count} boosts)")
        embed.add_field(name="Roles", value=len(guild.roles))
        roles = ", ".join(role.mention for role in guild.roles[::-1])
        if len(roles) > 1024:
            roles = "Too many roles to display"
        embed.add_field(name="Roles List", inline=False, value=roles)

        embed.set_footer(text=f"Server Created • {guild.created_at.strftime("%Y/%m/%d")}")

        await interaction.response.send_message(embed=embed)
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Info(bot), guild=GUILD_ID)