import discord
from discord.ext import commands
from discord import app_commands 
from config import BOT_TOKEN, GUILD_ID, OWNER_ID

from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=";", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged In Successfully! Online as: {bot.user}")
    try:
        synced = await bot.tree.sync(guild=GUILD_ID)
        print(f'Synced {len(synced)} commands to guild {GUILD_ID.id}')
    except Exception as e:
        print(f'Error syncing commands: {e}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    content: str = message.content.lower()
    if content.startswith('bye'):
        await message.channel.send(f"Goodbye, {message.author.display_name}")
        await bot.process_commands(message)

@bot.tree.command(name="hello", description="Say Hello!", guild=GUILD_ID)
async def say_hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hi there!")
    
@bot.tree.command(name="say", description="Repeat the given words.", guild=GUILD_ID)    
async def say(interaction: discord.Interaction, string: str):
    await interaction.response.send_message(f'{string}')

@bot.tree.command(name="github", description="The Github Repository of the Bot..", guild=GUILD_ID)    
async def github(interaction: discord.Interaction):
    owner = await bot.fetch_user(OWNER_ID)    
    embed = discord.Embed(
        title="GitHub Repository | Mamon",
        url="https://github.com/enkoki/mamon",
        description=(
            "A Discord bot built using discord.py, created for learning the basics of bot development. "
            "This project is currently in early development and is mainly focused on learning and experimenting with Discord bot fundamentals."
        ),
        color=discord.Color.from_str("#000000")
    )

    embed.set_thumbnail(url="https://uxwing.com/wp-content/themes/uxwing/download/brands-and-social-media/github-white-icon.png")

    embed.add_field(
        name="Commands",
        value=(
            "`/hello`\n"
            "`/say <text>`\n"
            "`/github`\n"
        ),
        inline = False
    )

    embed.add_field(
        name="Features",
        value=(
            "- Leveling\n"
            "- Moderation\n"
            "- Logs"
        )
    )

    embed.set_footer(text="Make sure to Star the Repository!")
    embed.set_author(
        name=owner.name,
        icon_url=owner.display_avatar.url
    )
    embed.set_image(url="https://i.imgur.com/IBrUrab.png")
    embed.timestamp = datetime.now()

    await interaction.response.send_message(embed=embed)

if __name__ == '__main__':
    bot.run(BOT_TOKEN)