import discord
from discord.ext import commands
from discord import app_commands
from config import GUILD_ID

def error_embed(message: str) -> discord.Embed:
    return discord.Embed(description=message, color=discord.Colour.from_str("#c33233"))

def success_embed(message: str) -> discord.Embed:
    return discord.Embed(description=message, color=discord.Colour.from_str("#03cb6a"))

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="kick", description="Kick a user from the server")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick_user(self, interaction: discord.Interaction, user: discord.Member, reason: str = "No reason"): 
        guild = interaction.guild
        invoker = interaction.user
        bot_member = guild.get_member(self.bot.user.id)

        if user.id == invoker.id:
            return await interaction.response.send_message(embed=error_embed("Cannot kick yourself."), ephemeral=True,)

        if user.id == guild.owner_id:
            return await interaction.response.send_message(embed=error_embed("Cannot kick the  Server Owner"), ephemeral=True,)

        if user.guild_permissions.administrator:
            return await interaction.response.send_message(embed=error_embed("User has Administrator permissions."), ephemeral=True,)

        if bot_member.top_role <= user.top_role:
            return await interaction.response.send_message(embed=error_embed("Not enough permissions"), ephemeral=True,)

        if invoker.top_role <= user.top_role:
            return await interaction.response.send_message(embed=error_embed("Not enough permissions"), ephemeral=True,)

        await user.kick(reason=reason)
        await interaction.response.send_message(embed=success_embed(f"**{user.name} has been kicked** | {reason}"))


async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot), guild=GUILD_ID)
