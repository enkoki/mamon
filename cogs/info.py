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
        embed.add_field(name="Server Created", value=guild.created_at.strftime("%Y/%m/%d"))
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

        embed.set_footer(text=f"ID • {guild.id}")

        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="userinfo", description="Get details of a user")
    async def _userinfo(self, interaction: discord.Interaction, user: discord.User = None):
        user = user or interaction.user
        fetched_user = await interaction.client.fetch_user(user.id)

        embed = discord.Embed(
            color=fetched_user.accent_color or discord.Colour.from_str(DEFAULT_COLOR),
            timestamp=datetime.now()
        )
        embed.set_author(name=str(user), icon_url=user.display_avatar.url)
        embed.description = user.mention

        if user.avatar:
            embed.set_thumbnail(url=user.avatar.url)

        if isinstance(user, discord.Member):
            embed.add_field(name="Joined", value=user.joined_at.strftime("%a, %b %d, %Y %I:%M %p"), inline=True)

        embed.add_field(name="Registered", value=user.created_at.strftime("%a, %b %d, %Y %I:%M %p"), inline=True)

        parts = []
        if user.avatar:
            parts.append(f"[**Avatar**]({user.display_avatar.url})")
        if fetched_user.banner:
            parts.append(f"[**Banner**]({fetched_user.banner.url})")
        if user.avatar_decoration:
            parts.append(f"[**Frame**]({user.avatar_decoration.url})")
        embed.add_field(name="Profile", value="\n".join(parts), inline=False)

        if isinstance(user, discord.Member):
            roles = ", ".join(role.mention for role in user.roles[1:][::-1])
            if len(roles) > 1024:
                roles = "Too many roles to display"
            embed.add_field(name=f"Roles List ({len(user.roles)-1})", inline=False, value=roles)

        embed.set_image(url=fetched_user.banner.url if fetched_user.banner else discord.Embed.Empty)
        embed.set_footer(text=f"ID • {user.id}")
        await interaction.response.send_message(embed=embed)

        
async def setup(bot: commands.Bot):
    await bot.add_cog(Info(bot), guild=GUILD_ID)