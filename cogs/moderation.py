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
    async def kick_user(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        reason: str = "No reason",
    ):
        guild = interaction.guild
        invoker = interaction.user
        bot_member = guild.get_member(self.bot.user.id)

        if user.id == invoker.id:
            return await interaction.response.send_message(
                embed=error_embed("Cannot kick yourself."),
                ephemeral=True,
            )

        if user.id == guild.owner_id:
            return await interaction.response.send_message(
                embed=error_embed("Cannot kick the  Server Owner"),
                ephemeral=True,
            )

        if user.guild_permissions.administrator:
            return await interaction.response.send_message(
                embed=error_embed("User has Administrator permissions."),
                ephemeral=True,
            )

        if bot_member.top_role <= user.top_role:
            return await interaction.response.send_message(
                embed=error_embed("Not enough permissions"),
                ephemeral=True,
            )

        if invoker.top_role <= user.top_role:
            return await interaction.response.send_message(
                embed=error_embed("Not enough permissions"),
                ephemeral=True,
            )

        await user.kick(reason=reason)
        await interaction.response.send_message(
            embed=success_embed(f"**{user.name} has been kicked** | {reason}")
        )

    @app_commands.command(name="ban", description="Ban a user from the server")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban_user(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        reason: str = "No reason",
    ):
        guild = interaction.guild
        invoker = interaction.user
        bot_member = guild.me

        if user == invoker:
            return await interaction.response.send_message(
                embed=error_embed("Cannot ban yourself."),
                ephemeral=True,
            )

        if user.id == guild.owner_id:
            return await interaction.response.send_message(
                embed=error_embed("Cannot ban the Server Owner."),
                ephemeral=True,
            )

        if user.guild_permissions.administrator:
            return await interaction.response.send_message(
                embed=error_embed("User has Administrator permissions."),
                ephemeral=True,
            )

        if not bot_member.guild_permissions.ban_members:
            return await interaction.response.send_message(
                embed=error_embed("I don't have the Ban Members permission."),
                ephemeral=True,
            )

        if bot_member.top_role <= user.top_role:
            return await interaction.response.send_message(
                embed=error_embed("My role is not high enough."),
                ephemeral=True,
            )

        if invoker.top_role <= user.top_role:
            return await interaction.response.send_message(
                embed=error_embed("Your role is not high enough."),
                ephemeral=True,
            )

        await user.ban(reason=reason)
        await interaction.response.send_message(
            embed=success_embed(f"**{user} has been banned.** | {reason}")
        )

    @app_commands.command(name="unban", description="Unban a user from the server")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban_user(
        self, interaction: discord.Interaction, user_id: str, reason: str = "No reason"
    ):
        guild = interaction.guild
        bot_member = guild.me

        if not bot_member.guild_permissions.ban_members:
            return await interaction.response.send_message(
                embed=error_embed("I don't have the **Ban Members** permission."),
                ephemeral=True,
            )

        try:
            user = await self.bot.fetch_user(int(user_id))
        except (ValueError, discord.NotFound):
            return await interaction.response.send_message(
                embed=error_embed("Invalid user ID."),
                ephemeral=True,
            )

        try:
            await guild.unban(user, reason=reason)
        except discord.NotFound:
            return await interaction.response.send_message(
                embed=error_embed("That user is not banned."),
                ephemeral=True,
            )
        except discord.Forbidden:
            return await interaction.response.send_message(
                embed=error_embed("I don't have permission to unban users."),
                ephemeral=True,
            )

        await interaction.response.send_message(
            embed=success_embed(f"**{user} has been unbanned.** | {reason}")
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot), guild=GUILD_ID)
