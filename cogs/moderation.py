import discord
from discord.ext import commands
from discord import app_commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="kick", description="Kick a user from the server")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick_user(self, interaction: discord.Interaction, user: discord.Member, reason="No reason"):
        embed = discord.Embed(
            description=f"{user.name} has been kicked out | {reason}" 
        )
        await user.kick(reason = reason)
        await interaction.response.send_message
