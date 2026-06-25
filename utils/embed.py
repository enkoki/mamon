import discord

def error_embed(message: str) -> discord.Embed:
    return discord.Embed(description=message, color=discord.Colour.from_str("#c33233"))


def success_embed(message: str) -> discord.Embed:
    return discord.Embed(description=message, color=discord.Colour.from_str("#03cb6a"))