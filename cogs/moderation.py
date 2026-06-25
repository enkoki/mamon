import discord
from discord.ext import commands
from discord import app_commands
from config import GUILD_ID
from datetime import timedelta
from utils import error_embed, success_embed, check_action


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
        err = check_action(
            interaction.guild, interaction.user, user, interaction.guild.me, "kick"
        )
        if err:
            return await interaction.response.send_message(embed=err, ephemeral=True)

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
        err = check_action(
            interaction.guild, interaction.user, user, interaction.guild.me, "ban"
        )
        if err:
            return await interaction.response.send_message(embed=err, ephemeral=True)

        await user.ban(reason=reason)
        await interaction.response.send_message(
            embed=success_embed(f"**{user} has been banned.** | {reason}")
        )

    @app_commands.command(name="unban", description="Unban a user from the server")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban_user(
        self,
        interaction: discord.Interaction,
        user_id: str,
        reason: str = "No reason",
    ):
        try:
            user = await self.bot.fetch_user(int(user_id))
        except (ValueError, discord.NotFound):
            return await interaction.response.send_message(
                embed=error_embed("Invalid user ID."),
                ephemeral=True,
            )

        try:
            await interaction.guild.unban(user, reason=reason)
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

    @app_commands.command(name="mute", description="Timeout a user")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def mute_user(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        minutes: app_commands.Range[int, 1, 40320],
        reason: str = "No reason",
    ):
        err = check_action(
            interaction.guild, interaction.user, user, interaction.guild.me, "mute"
        )
        if err:
            return await interaction.response.send_message(embed=err, ephemeral=True)

        if user.is_timed_out():
            return await interaction.response.send_message(
                embed=error_embed("User is already muted."),
                ephemeral=True,
            )

        await user.timeout(timedelta(minutes=minutes), reason=reason)
        await interaction.response.send_message(
            embed=success_embed(
                f"**{user} was muted for {minutes} minute(s)** | {reason}"
            )
        )

    @app_commands.command(name="unmute", description="Remove a user's timeout")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def unmute_user(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        reason: str = "No reason",
    ):
        guild = interaction.guild
        bot_member = guild.me
        invoker = interaction.user

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

        if not user.is_timed_out():
            return await interaction.response.send_message(
                embed=error_embed("User is not muted."),
                ephemeral=True,
            )

        await user.timeout(None, reason=reason)
        await interaction.response.send_message(
            embed=success_embed(f"**{user} was unmuted**")
        )

    @app_commands.command(name="purge", description="Delete a number of messages")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def purge_messages(
        self,
        interaction: discord.Interaction,
        amount: app_commands.Range[int, 1, 100],
    ):
        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=amount)
        await interaction.followup.send(
            embed=success_embed(f"**Deleted {len(deleted)} message(s)**"),
            ephemeral=True,
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))
