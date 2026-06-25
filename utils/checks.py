import discord

def check_action(guild: discord.Guild, invoker: discord.Member, target: discord.Member, bot_member: discord.Member, action: str,) -> discord.Embed | None:
    if target == invoker:
        return error_embed(f"Cannot {action} yourself.")
    if target.id == guild.owner_id:
        return error_embed(f"Cannot {action} the Server Owner.")
    if target.guild_permissions.administrator:
        return error_embed("User has Administrator permissions.")
    if bot_member.top_role <= target.top_role:
        return error_embed("My role is not high enough.")
    if invoker.top_role <= target.top_role:
        return error_embed("Your role is not high enough.")
    return None