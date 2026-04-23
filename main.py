import discord
from discord.ext import commands
from discord import app_commands 
from config import BOT_TOKEN, GUILD_ID

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
    
if __name__ == '__main__':
    bot.run(BOT_TOKEN)