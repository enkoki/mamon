import discord
from discord.ext import commands
from discord import app_commands
from config import GUILD_ID

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="kick", description="Kick a user from the server")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick_user(self, interaction: discord.Interaction, user: discord.Member, reason: str ="No reason"):
        if isinstance(user, discord.Member):
            embed = discord.Embed(
                description=f"{user.name} has been kicked out | {reason}",
                color = discord.Colour.from_str("#03cb6a"),
            )
            await user.kick(reason = reason)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                description="Failed to find the user in the server",
                color = discord.Colour.from_str("#c33233"),
            )
            await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot), guild=GUILD_ID)
